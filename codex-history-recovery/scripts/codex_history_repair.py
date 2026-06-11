#!/usr/bin/env python3
"""Inspect and repair Codex Desktop history metadata after account/API switches.

The repair is intentionally narrow: it syncs provider/model metadata only.
It never rewrites thread cwd/project ownership.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CurrentConfig:
    provider: str | None
    model: str | None


def json_print(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{key}: {json.dumps(value, ensure_ascii=False)}")
            else:
                print(f"{key}: {value}")


def codex_home_from_args(args: argparse.Namespace) -> Path:
    if args.codex_home:
        return Path(args.codex_home).expanduser()
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def read_current_config(home: Path, provider_arg: str | None, model_arg: str | None) -> CurrentConfig:
    config_path = home / "config.toml"
    text = config_path.read_text(encoding="utf-8", errors="replace")
    provider = provider_arg or _match_toml_string(text, "model_provider")
    model = model_arg or _match_toml_string(text, "model")
    return CurrentConfig(provider=provider, model=model)


def require_sync_targets(current: CurrentConfig, fields: set[str]) -> None:
    missing = []
    if "provider" in fields and not current.provider:
        missing.append("--provider")
    if "model" in fields and not current.model:
        missing.append("--model")
    if missing:
        raise SystemExit(
            "Could not determine target " + "/".join(sorted(fields)) + ". "
            "Pass " + " and ".join(missing) + " explicitly."
        )


def _match_toml_string(text: str, key: str) -> str | None:
    match = re.search(rf'(?m)^\s*{re.escape(key)}\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else None


def connect_sqlite_ro(path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30)


def ensure_state_db(home: Path) -> Path:
    db = home / "state_5.sqlite"
    if not db.exists():
        raise SystemExit(f"Codex state database not found: {db}")
    return db


def ensure_threads_table(conn: sqlite3.Connection) -> set[str]:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "threads" not in tables:
        raise SystemExit("state_5.sqlite does not contain a threads table.")
    return {row[1] for row in conn.execute("PRAGMA table_info(threads)")}


def fetch_threads(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    cols = ensure_threads_table(conn)
    required = {
        "id",
        "rollout_path",
        "model_provider",
        "model",
        "cwd",
        "archived",
        "created_at",
        "updated_at",
        "archived_at",
    }
    missing = sorted(required - cols)
    if missing:
        raise SystemExit(f"threads table missing expected columns: {', '.join(missing)}")
    rows = conn.execute(
        """
        SELECT id, rollout_path, model_provider, model, cwd, COALESCE(archived, 0),
               created_at, updated_at, archived_at
        FROM threads
        ORDER BY updated_at_ms DESC
        """
    )
    return [
        {
            "id": thread_id,
            "rollout_path": rollout_path,
            "model_provider": provider,
            "model": model,
            "cwd": cwd,
            "archived": bool(archived),
            "created_at": created_at,
            "updated_at": updated_at,
            "archived_at": archived_at,
        }
        for thread_id, rollout_path, provider, model, cwd, archived, created_at, updated_at, archived_at in rows
    ]


def top_counts(values: list[Any], limit: int = 20) -> list[dict[str, Any]]:
    counter = collections.Counter("(null)" if value is None else value for value in values)
    return [{"value": value, "count": count} for value, count in counter.most_common(limit)]


def detect_codex_processes() -> list[str]:
    try:
        result = subprocess.run(
            ["pgrep", "-fl", r"Codex|codex app-server"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return []
    current_pid = str(os.getpid())
    lines = []
    for line in result.stdout.splitlines():
        if line.startswith(current_pid + " "):
            continue
        if "codex_history_repair.py" in line:
            continue
        if "pgrep -fl Codex|codex app-server" in line:
            continue
        pid = line.split(maxsplit=1)[0] if line.split(maxsplit=1) else "unknown"
        if "/Applications/Codex.app/" in line:
            lines.append(f"{pid} Codex.app")
        elif "codex app-server" in line:
            lines.append(f"{pid} codex app-server")
    return lines


def scan_rollouts(paths: list[Path], current: CurrentConfig | None = None) -> dict[str, Any]:
    session_meta_provider_counts: collections.Counter[str] = collections.Counter()
    turn_context_model_counts: collections.Counter[str] = collections.Counter()
    cwd_counts: collections.Counter[str] = collections.Counter()
    missing_paths: list[str] = []
    parse_errors: list[dict[str, Any]] = []
    files_scanned = 0
    files_needing_provider = 0
    files_needing_model = 0

    for path in paths:
        if not path.exists():
            missing_paths.append(str(path))
            continue
        files_scanned += 1
        file_needs_provider = False
        file_needs_model = False
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, raw in enumerate(handle, start=1):
                try:
                    obj = json.loads(raw)
                except Exception as exc:  # noqa: BLE001 - keep scan resilient.
                    if len(parse_errors) < 10:
                        parse_errors.append({"path": str(path), "line": line_no, "error": str(exc)})
                    continue
                payload = obj.get("payload")
                if not isinstance(payload, dict):
                    continue
                if obj.get("type") == "session_meta":
                    provider = payload.get("model_provider")
                    session_meta_provider_counts["(null)" if provider is None else str(provider)] += 1
                    cwd = payload.get("cwd")
                    cwd_counts["(null)" if cwd is None else str(cwd)] += 1
                    if current and current.provider and provider != current.provider:
                        file_needs_provider = True
                elif obj.get("type") == "turn_context":
                    model = payload.get("model")
                    turn_context_model_counts["(null)" if model is None else str(model)] += 1
                    if current and current.model and model != current.model:
                        file_needs_model = True
        files_needing_provider += int(file_needs_provider)
        files_needing_model += int(file_needs_model)

    return {
        "files_scanned": files_scanned,
        "missing_paths_count": len(missing_paths),
        "missing_paths_sample": missing_paths[:10],
        "parse_errors_count": len(parse_errors),
        "parse_errors_sample": parse_errors,
        "session_meta_provider_counts": [
            {"value": value, "count": count}
            for value, count in session_meta_provider_counts.most_common(20)
        ],
        "turn_context_model_counts": [
            {"value": value, "count": count}
            for value, count in turn_context_model_counts.most_common(20)
        ],
        "cwd_counts_top": [{"value": value, "count": count} for value, count in cwd_counts.most_common(20)],
        "files_needing_provider": files_needing_provider,
        "files_needing_model": files_needing_model,
    }


def status(args: argparse.Namespace) -> int:
    home = codex_home_from_args(args)
    db = ensure_state_db(home)
    current = read_current_config(home, args.provider, args.model)
    with connect_sqlite_ro(db) as conn:
        threads = fetch_threads(conn)

    db_mismatches = []
    for item in threads:
        provider_mismatch = current.provider is not None and item["model_provider"] != current.provider
        model_mismatch = current.model is not None and item["model"] != current.model
        if provider_mismatch or model_mismatch:
            db_mismatches.append(item)
    rollouts = scan_rollouts(
        [Path(item["rollout_path"]) for item in threads if item["rollout_path"]],
        current,
    )
    json_print(
        {
            "codex_home": str(home),
            "current_provider": current.provider,
            "current_model": current.model,
            "total_threads": len(threads),
            "db_provider_counts": top_counts([item["model_provider"] for item in threads]),
            "db_model_counts": top_counts([item["model"] for item in threads]),
            "db_cwd_counts_top": top_counts([item["cwd"] for item in threads]),
            "db_archived_counts": top_counts([item["archived"] for item in threads]),
            "db_provider_or_model_mismatches": len(db_mismatches),
            "rollout_scan": rollouts,
            "codex_processes_detected": detect_codex_processes(),
        },
        args.json,
    )
    return 0


def backup_sqlite(db: Path, backup_dir: Path, label: str) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"state_5.sqlite.{label}.{timestamp()}.bak"
    with connect_sqlite_ro(db) as src, sqlite3.connect(str(backup_path), timeout=30) as dst:
        src.backup(dst)
    return backup_path


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def sync(args: argparse.Namespace) -> int:
    home = codex_home_from_args(args)
    db = ensure_state_db(home)
    current = read_current_config(home, args.provider, args.model)
    fields = sync_fields(args)
    require_sync_targets(current, fields)

    with connect_sqlite_ro(db) as conn:
        threads = fetch_threads(conn)

    rollout_paths = sorted({Path(item["rollout_path"]) for item in threads if item["rollout_path"]})
    db_rows_to_update = [
        item
        for item in threads
        if thread_needs_sync(item, current, fields, args)
    ]
    rollout_scan = scan_rollouts(rollout_paths, current)

    if not args.apply:
        json_print(
            {
                "dry_run": True,
                "message": "No changes made. Re-run sync with --apply to update selected metadata.",
                "fields": sorted(fields),
                "current_provider": current.provider,
                "current_model": current.model,
                "from_provider": args.from_provider,
                "from_model": args.from_model,
                "db_rows_to_update": len(db_rows_to_update),
                "rollout_scan": rollout_scan,
                "codex_processes_detected": detect_codex_processes(),
            },
            args.json,
        )
        return 0

    processes = detect_codex_processes()
    if processes and not args.allow_running:
        raise SystemExit(
            "Codex appears to be running. Close Codex Desktop first, or re-run with --allow-running "
            "if you intentionally want to repair while it is open."
        )

    backup_dir = home / "history_sync_backups"
    sqlite_backup = backup_sqlite(db, backup_dir, "pre-provider-model-sync")
    metadata_backup = backup_dir / f"rollout-provider-model-lines.pre-sync.{timestamp()}.jsonl.gz"

    changed_files = 0
    changed_lines = 0
    session_meta_changed = 0
    turn_context_changed = 0
    parse_errors: list[dict[str, Any]] = []
    missing_paths: list[str] = []

    with gzip.open(metadata_backup, "wt", encoding="utf-8") as backup:
        for path in rollout_paths:
            if not path.exists():
                missing_paths.append(str(path))
                continue
            file_changed, file_stats = rewrite_rollout_provider_model(
                path=path,
                current=current,
                fields=fields,
                from_provider=args.from_provider,
                from_model=args.from_model,
                backup_handle=backup,
                parse_errors=parse_errors,
            )
            changed_files += int(file_changed)
            changed_lines += file_stats["changed_lines"]
            session_meta_changed += file_stats["session_meta_changed"]
            turn_context_changed += file_stats["turn_context_changed"]

    with sqlite3.connect(str(db), timeout=30) as conn:
        conn.execute("PRAGMA busy_timeout = 30000")
        db_updated = update_thread_metadata(conn, current, fields, args)
        conn.commit()
        checkpoint = conn.execute("PRAGMA wal_checkpoint(FULL)").fetchone()

    with connect_sqlite_ro(db) as conn:
        final_threads = fetch_threads(conn)

    json_print(
        {
            "dry_run": False,
            "fields": sorted(fields),
            "current_provider": current.provider,
            "current_model": current.model,
            "from_provider": args.from_provider,
            "from_model": args.from_model,
            "sqlite_backup": str(sqlite_backup),
            "metadata_backup": str(metadata_backup),
            "changed_files": changed_files,
            "changed_lines": changed_lines,
            "session_meta_changed": session_meta_changed,
            "turn_context_changed": turn_context_changed,
            "sqlite_rows_updated": db_updated,
            "checkpoint": {
                "busy": checkpoint[0],
                "log_frames": checkpoint[1],
                "checkpointed_frames": checkpoint[2],
            },
            "final_provider_counts": top_counts([item["model_provider"] for item in final_threads]),
            "final_model_counts": top_counts([item["model"] for item in final_threads]),
            "final_cwd_counts_top": top_counts([item["cwd"] for item in final_threads]),
            "missing_paths_count": len(missing_paths),
            "missing_paths_sample": missing_paths[:10],
            "parse_errors_count": len(parse_errors),
            "parse_errors_sample": parse_errors[:10],
        },
        args.json,
    )
    return 0


def rewrite_rollout_provider_model(
    path: Path,
    current: CurrentConfig,
    fields: set[str],
    from_provider: str | None,
    from_model: str | None,
    backup_handle: Any,
    parse_errors: list[dict[str, Any]],
) -> tuple[bool, dict[str, int]]:
    changed = False
    stats = {"changed_lines": 0, "session_meta_changed": 0, "turn_context_changed": 0}
    original_stat = path.stat()
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as out:
            with path.open("r", encoding="utf-8", errors="replace", newline="") as inp:
                for line_no, raw in enumerate(inp, start=1):
                    line = raw.rstrip("\n")
                    newline = "\n" if raw.endswith("\n") else ""
                    try:
                        obj = json.loads(line)
                    except Exception as exc:  # noqa: BLE001 - preserve unreadable line.
                        if len(parse_errors) < 10:
                            parse_errors.append({"path": str(path), "line": line_no, "error": str(exc)})
                        out.write(raw)
                        continue

                    payload = obj.get("payload")
                    did_change = False
                    if "provider" in fields and obj.get("type") == "session_meta" and isinstance(payload, dict):
                        provider_matches_source = from_provider is None or payload.get("model_provider") == from_provider
                        if provider_matches_source and payload.get("model_provider") != current.provider:
                            payload["model_provider"] = current.provider
                            did_change = True
                        if did_change:
                            stats["session_meta_changed"] += 1
                    elif "model" in fields and obj.get("type") == "turn_context" and isinstance(payload, dict):
                        model_matches_source = from_model is None or payload.get("model") == from_model
                        if model_matches_source and payload.get("model") != current.model:
                            payload["model"] = current.model
                            did_change = True
                        if did_change:
                            stats["turn_context_changed"] += 1

                    if did_change:
                        backup_handle.write(
                            json.dumps(
                                {"path": str(path), "line": line_no, "old": line},
                                ensure_ascii=False,
                                separators=(",", ":"),
                            )
                            + "\n"
                        )
                        out.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + newline)
                        changed = True
                        stats["changed_lines"] += 1
                    else:
                        out.write(raw)
        if changed:
            os.replace(tmp_name, path)
            os.utime(path, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
        else:
            os.unlink(tmp_name)
        return changed, stats
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def sync_fields(args: argparse.Namespace) -> set[str]:
    if args.provider_only and args.model_only:
        raise SystemExit("Use only one of --provider-only or --model-only.")
    if args.provider_only:
        return {"provider"}
    if args.model_only:
        return {"model"}
    return {"provider", "model"}


def thread_needs_sync(
    item: dict[str, Any],
    current: CurrentConfig,
    fields: set[str],
    args: argparse.Namespace,
) -> bool:
    if "provider" in fields:
        provider_matches_source = args.from_provider is None or item["model_provider"] == args.from_provider
        if provider_matches_source and item["model_provider"] != current.provider:
            return True
    if "model" in fields:
        model_matches_source = args.from_model is None or item["model"] == args.from_model
        if model_matches_source and item["model"] != current.model:
            return True
    return False


def update_thread_metadata(
    conn: sqlite3.Connection,
    current: CurrentConfig,
    fields: set[str],
    args: argparse.Namespace,
) -> int:
    if fields == {"provider"}:
        where = "model_provider IS NULL OR model_provider <> ?"
        params: list[Any] = [current.provider, current.provider]
        if args.from_provider is not None:
            where = "model_provider = ? AND model_provider <> ?"
            params = [current.provider, args.from_provider, current.provider]
        return conn.execute(
            f"UPDATE threads SET model_provider = ? WHERE {where}",
            params,
        ).rowcount
    if fields == {"model"}:
        where = "model IS NULL OR model <> ?"
        params = [current.model, current.model]
        if args.from_model is not None:
            where = "model = ? AND model <> ?"
            params = [current.model, args.from_model, current.model]
        return conn.execute(
            f"UPDATE threads SET model = ? WHERE {where}",
            params,
        ).rowcount

    where_parts = []
    params = [current.provider, current.model]
    if args.from_provider is None:
        where_parts.append("(model_provider IS NULL OR model_provider <> ?)")
        params.append(current.provider)
    else:
        where_parts.append("(model_provider = ? AND model_provider <> ?)")
        params.extend([args.from_provider, current.provider])
    if args.from_model is None:
        where_parts.append("(model IS NULL OR model <> ?)")
        params.append(current.model)
    else:
        where_parts.append("(model = ? AND model <> ?)")
        params.extend([args.from_model, current.model])
    return conn.execute(
        f"UPDATE threads SET model_provider = ?, model = ? WHERE {' OR '.join(where_parts)}",
        params,
    ).rowcount


def backup(args: argparse.Namespace) -> int:
    home = codex_home_from_args(args)
    db = ensure_state_db(home)
    backup_path = backup_sqlite(db, home / "history_sync_backups", "manual")
    json_print({"sqlite_backup": str(backup_path)}, args.json)
    return 0


def delete_archived(args: argparse.Namespace) -> int:
    home = codex_home_from_args(args)
    db = ensure_state_db(home)
    with connect_sqlite_ro(db) as conn:
        threads = fetch_threads(conn)

    archived = [item for item in threads if item["archived"]]
    selected = filter_archived_threads(archived, args)
    thread_rollout_paths = {
        normalized_path(item["rollout_path"])
        for item in threads
        if item["rollout_path"]
    }
    archived_files, archived_file_parse_errors = scan_archived_session_files(home)
    orphan_archived_files = [
        item for item in archived_files if normalized_path(item["path"]) not in thread_rollout_paths
    ]
    selected_orphan_files = filter_archived_file_records(orphan_archived_files, args)
    missing_paths = [
        str(Path(item["rollout_path"]))
        for item in selected
        if item["rollout_path"] and not Path(item["rollout_path"]).exists()
    ]

    if not args.apply:
        json_print(
            {
                "dry_run": True,
                "message": "No changes made. Re-run delete-archived with --apply to move archived JSONL files and delete SQLite rows.",
                "total_threads": len(threads),
                "archived_threads": len(archived),
                "selected_archived_threads": len(selected),
                "archived_session_files": len(archived_files),
                "orphan_archived_session_files": len(orphan_archived_files),
                "selected_orphan_archived_session_files": len(selected_orphan_files),
                "filters": archived_delete_filters(args),
                "selected_cwd_counts_top": top_counts(
                    [item["cwd"] for item in selected] + [item["cwd"] for item in selected_orphan_files]
                ),
                "missing_paths_count": len(missing_paths),
                "missing_paths_sample": missing_paths[:10],
                "rollout_paths_sample": [
                    item["rollout_path"] for item in selected[:10] if item["rollout_path"]
                ]
                + [item["path"] for item in selected_orphan_files[:10]],
                "archived_file_parse_errors_count": len(archived_file_parse_errors),
                "archived_file_parse_errors_sample": archived_file_parse_errors[:10],
                "codex_processes_detected": detect_codex_processes(),
            },
            args.json,
        )
        return 0

    if not args.all and not any([args.cwd, args.before, args.older_than_days, args.rollout_path]):
        raise SystemExit(
            "Refusing to delete every archived thread without --all. "
            "Use filters, or pass --all if you intentionally want all archived records deleted."
        )

    processes = detect_codex_processes()
    if processes and not args.allow_running:
        raise SystemExit(
            "Codex appears to be running. Close Codex Desktop first, or re-run with --allow-running "
            "if you intentionally want to delete archived records while it is open."
        )

    backup_dir = home / "history_sync_backups"
    sqlite_backup = backup_sqlite(db, backup_dir, "pre-archived-delete")
    rollout_backup_dir = backup_dir / f"archived-rollouts.pre-delete.{timestamp()}"
    rollout_backup_dir.mkdir(parents=True, exist_ok=True)

    moved_files = 0
    moved_rollouts: list[dict[str, str]] = []
    move_errors: list[dict[str, str]] = []
    paths_to_move = unique_existing_paths(
        [item["rollout_path"] for item in selected if item["rollout_path"]]
        + [item["path"] for item in selected_orphan_files]
    )
    for src in paths_to_move:
        if not src.exists():
            continue
        dst = unique_backup_path(rollout_backup_dir, home, src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(src), str(dst))
        except Exception as exc:  # noqa: BLE001 - report file-level failures.
            if len(move_errors) < 10:
                move_errors.append({"path": str(src), "error": str(exc)})
            continue
        moved_files += 1
        if len(moved_rollouts) < 10:
            moved_rollouts.append({"from": str(src), "to": str(dst)})

    selected_ids = [item["id"] for item in selected]
    sqlite_rows_deleted = 0
    checkpoint = None
    if selected_ids:
        placeholders = ",".join("?" for _ in selected_ids)
        with sqlite3.connect(str(db), timeout=30) as conn:
            conn.execute("PRAGMA busy_timeout = 30000")
            sqlite_rows_deleted = conn.execute(
                f"DELETE FROM threads WHERE archived = 1 AND id IN ({placeholders})",
                selected_ids,
            ).rowcount
            conn.commit()
            checkpoint = conn.execute("PRAGMA wal_checkpoint(FULL)").fetchone()

    json_print(
        {
            "dry_run": False,
            "sqlite_backup": str(sqlite_backup),
            "rollout_backup_dir": str(rollout_backup_dir),
            "selected_archived_threads": len(selected),
            "selected_orphan_archived_session_files": len(selected_orphan_files),
            "moved_files": moved_files,
            "sqlite_rows_deleted": sqlite_rows_deleted,
            "filters": archived_delete_filters(args),
            "missing_paths_count": len(missing_paths),
            "missing_paths_sample": missing_paths[:10],
            "archived_file_parse_errors_count": len(archived_file_parse_errors),
            "archived_file_parse_errors_sample": archived_file_parse_errors[:10],
            "move_errors_count": len(move_errors),
            "move_errors_sample": move_errors,
            "moved_rollouts_sample": moved_rollouts,
            "checkpoint": None
            if checkpoint is None
            else {
                "busy": checkpoint[0],
                "log_frames": checkpoint[1],
                "checkpointed_frames": checkpoint[2],
            },
        },
        args.json,
    )
    return 0


def scan_archived_session_files(home: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    archived_dir = home / "archived_sessions"
    if not archived_dir.exists():
        return [], []
    records: list[dict[str, Any]] = []
    parse_errors: list[dict[str, str]] = []
    for path in sorted(archived_dir.glob("rollout-*.jsonl")):
        cwd = None
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for raw in handle:
                    obj = json.loads(raw)
                    if obj.get("type") != "session_meta":
                        continue
                    payload = obj.get("payload")
                    if isinstance(payload, dict):
                        cwd = payload.get("cwd")
                    break
        except Exception as exc:  # noqa: BLE001 - keep deletion preview resilient.
            if len(parse_errors) < 10:
                parse_errors.append({"path": str(path), "error": str(exc)})
        records.append(
            {
                "path": str(path),
                "cwd": cwd,
                "archived_at": int(path.stat().st_mtime),
            }
        )
    return records, parse_errors


def filter_archived_threads(threads: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    selected = list(threads)
    if args.cwd:
        selected = [item for item in selected if item["cwd"] == args.cwd]
    if args.rollout_path:
        wanted = {str(Path(path).expanduser()) for path in args.rollout_path}
        selected = [
            item
            for item in selected
            if item["rollout_path"] and str(Path(item["rollout_path"]).expanduser()) in wanted
        ]
    if args.older_than_days is not None:
        cutoff = datetime.now() - timedelta(days=args.older_than_days)
        selected = [
            item
            for item in selected
            if thread_archived_datetime(item) is not None and thread_archived_datetime(item) < cutoff
        ]
    if args.before:
        cutoff_date = parse_iso_date(args.before)
        selected = [
            item
            for item in selected
            if thread_archived_date(item) is not None and thread_archived_date(item) < cutoff_date
        ]
    return selected


def filter_archived_file_records(records: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    selected = list(records)
    if args.cwd:
        selected = [item for item in selected if item["cwd"] == args.cwd]
    if args.rollout_path:
        wanted = {normalized_path(path) for path in args.rollout_path}
        selected = [item for item in selected if normalized_path(item["path"]) in wanted]
    if args.older_than_days is not None:
        cutoff = datetime.now() - timedelta(days=args.older_than_days)
        selected = [
            item
            for item in selected
            if thread_archived_datetime(item) is not None and thread_archived_datetime(item) < cutoff
        ]
    if args.before:
        cutoff_date = parse_iso_date(args.before)
        selected = [
            item
            for item in selected
            if thread_archived_date(item) is not None and thread_archived_date(item) < cutoff_date
        ]
    return selected


def archived_delete_filters(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "all": bool(args.all),
        "cwd": args.cwd,
        "before": args.before,
        "older_than_days": args.older_than_days,
        "rollout_path_count": len(args.rollout_path or []),
    }


def normalized_path(path: str | Path) -> str:
    return str(Path(path).expanduser().resolve(strict=False))


def unique_existing_paths(paths: list[str]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser()
        norm = normalized_path(path)
        if norm in seen:
            continue
        seen.add(norm)
        result.append(path)
    return result


def thread_archived_datetime(item: dict[str, Any]) -> datetime | None:
    ts = item.get("archived_at") or item.get("updated_at") or item.get("created_at")
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(int(ts))
    except (OSError, OverflowError, TypeError, ValueError):
        return None


def thread_archived_date(item: dict[str, Any]) -> date | None:
    dt = thread_archived_datetime(item)
    return dt.date() if dt else None


def parse_iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid date for --before: {value!r}. Use YYYY-MM-DD.") from exc


def unique_backup_path(backup_root: Path, home: Path, src: Path) -> Path:
    try:
        rel = src.relative_to(home)
    except ValueError:
        rel = Path(src.name)
    dst = backup_root / rel
    if not dst.exists():
        return dst
    stem = dst.stem
    suffix = dst.suffix
    for idx in range(1, 10_000):
        candidate = dst.with_name(f"{stem}.{idx}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not create unique backup path for {src}")


def restore(args: argparse.Namespace) -> int:
    home = codex_home_from_args(args)
    db = ensure_state_db(home)
    if not args.sqlite_backup and not args.metadata_backup:
        raise SystemExit("Pass --sqlite-backup and/or --metadata-backup to restore.")
    if args.sqlite_backup and not Path(args.sqlite_backup).expanduser().exists():
        raise SystemExit(f"SQLite backup not found: {args.sqlite_backup}")
    if args.metadata_backup and not Path(args.metadata_backup).expanduser().exists():
        raise SystemExit(f"Metadata backup not found: {args.metadata_backup}")
    processes = detect_codex_processes()
    if processes and not args.allow_running:
        raise SystemExit(
            "Codex appears to be running. Close Codex Desktop first, or re-run with --allow-running "
            "if you intentionally want to restore while it is open."
        )
    if not args.apply:
        json_print(
            {
                "dry_run": True,
                "message": "No changes made. Re-run restore with --apply to restore backups.",
                "sqlite_backup_to_restore": args.sqlite_backup,
                "metadata_backup_to_restore": args.metadata_backup,
            },
            args.json,
        )
        return 0

    safety_backup = backup_sqlite(db, home / "history_sync_backups", "pre-restore")
    jsonl_restored = None
    if args.metadata_backup:
        jsonl_restored = restore_metadata_lines(Path(args.metadata_backup).expanduser())
    if args.sqlite_backup:
        with sqlite3.connect(str(Path(args.sqlite_backup).expanduser()), timeout=30) as src:
            with sqlite3.connect(str(db), timeout=30) as dst:
                src.backup(dst)
                dst.commit()
                checkpoint = dst.execute("PRAGMA wal_checkpoint(FULL)").fetchone()
    else:
        checkpoint = None
    json_print(
        {
            "dry_run": False,
            "safety_sqlite_backup": str(safety_backup),
            "sqlite_restored_from": args.sqlite_backup,
            "metadata_restored_from": args.metadata_backup,
            "jsonl_restore": jsonl_restored,
            "checkpoint": None
            if checkpoint is None
            else {
                "busy": checkpoint[0],
                "log_frames": checkpoint[1],
                "checkpointed_frames": checkpoint[2],
            },
        },
        args.json,
    )
    return 0


def restore_metadata_lines(metadata_backup: Path) -> dict[str, Any]:
    by_path: dict[Path, dict[int, str]] = collections.defaultdict(dict)
    with gzip.open(metadata_backup, "rt", encoding="utf-8") as handle:
        for raw in handle:
            rec = json.loads(raw)
            by_path[Path(rec["path"])][int(rec["line"])] = rec["old"]

    restored_files = 0
    restored_lines = 0
    missing_paths: list[str] = []
    for path, replacements in by_path.items():
        if not path.exists():
            missing_paths.append(str(path))
            continue
        original_stat = path.stat()
        fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
        changed = False
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as out:
                with path.open("r", encoding="utf-8", errors="replace", newline="") as inp:
                    for line_no, raw in enumerate(inp, start=1):
                        if line_no in replacements:
                            newline = "\n" if raw.endswith("\n") else ""
                            out.write(replacements[line_no] + newline)
                            restored_lines += 1
                            changed = True
                        else:
                            out.write(raw)
            if changed:
                os.replace(tmp_name, path)
                os.utime(path, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
                restored_files += 1
            else:
                os.unlink(tmp_name)
        except Exception:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass
            raise
    return {
        "restored_files": restored_files,
        "restored_lines": restored_lines,
        "missing_paths_count": len(missing_paths),
        "missing_paths_sample": missing_paths[:10],
    }


def repair_times(args: argparse.Namespace) -> int:
    home = codex_home_from_args(args)
    db = ensure_state_db(home)
    with connect_sqlite_ro(db) as conn:
        rows = conn.execute(
            "SELECT id, rollout_path, updated_at, updated_at_ms FROM threads WHERE rollout_path IS NOT NULL"
        ).fetchall()
    by_path = {
        str(Path(rollout_path).expanduser()): {
            "id": thread_id,
            "updated_at": updated_at,
            "updated_at_ms": updated_at_ms,
        }
        for thread_id, rollout_path, updated_at, updated_at_ms in rows
    }
    paths = selected_repair_time_paths(args, by_path)

    missing_paths: list[str] = []
    no_timestamp_paths: list[str] = []
    updates: list[dict[str, Any]] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if not path.exists():
            missing_paths.append(str(path))
            continue
        ts = last_rollout_timestamp(path)
        if ts is None:
            no_timestamp_paths.append(str(path))
            continue
        key = str(path)
        row = by_path.get(key)
        if row is None:
            continue
        updated_at = int(ts)
        updated_at_ms = int(round(ts * 1000))
        changed = row["updated_at"] != updated_at or row["updated_at_ms"] != updated_at_ms
        updates.append(
            {
                "id": row["id"],
                "path": key,
                "updated_at": updated_at,
                "updated_at_ms": updated_at_ms,
                "changed": changed,
            }
        )

    if not args.apply:
        json_print(
            {
                "dry_run": True,
                "message": "No changes made. Re-run repair-times with --apply to update SQLite times and rollout mtimes.",
                "selected_paths": len(paths),
                "computed_times": len(updates),
                "rows_to_update": sum(1 for item in updates if item["changed"]),
                "missing_paths_count": len(missing_paths),
                "missing_paths_sample": missing_paths[:10],
                "no_timestamp_paths_count": len(no_timestamp_paths),
                "no_timestamp_paths_sample": no_timestamp_paths[:10],
                "sample": [
                    {
                        "id": item["id"],
                        "updated_at": item["updated_at"],
                        "path": item["path"],
                    }
                    for item in updates[:10]
                ],
            },
            args.json,
        )
        return 0

    processes = detect_codex_processes()
    if processes and not args.allow_running:
        raise SystemExit(
            "Codex appears to be running. Close Codex Desktop first, or re-run with --allow-running "
            "if you intentionally want to repair times while it is open."
        )

    sqlite_backup = backup_sqlite(db, home / "history_sync_backups", "pre-repair-times")
    sqlite_rows_updated = 0
    with sqlite3.connect(str(db), timeout=30) as conn:
        conn.execute("PRAGMA busy_timeout = 30000")
        for item in updates:
            if not item["changed"]:
                continue
            sqlite_rows_updated += conn.execute(
                "UPDATE threads SET updated_at = ?, updated_at_ms = ? WHERE rollout_path = ?",
                (item["updated_at"], item["updated_at_ms"], item["path"]),
            ).rowcount
        conn.commit()
        checkpoint = conn.execute("PRAGMA wal_checkpoint(FULL)").fetchone()

    mtimes_updated = 0
    for item in updates:
        ns = int(round(item["updated_at_ms"] * 1_000_000))
        os.utime(item["path"], ns=(ns, ns))
        mtimes_updated += 1

    json_print(
        {
            "dry_run": False,
            "sqlite_backup": str(sqlite_backup),
            "selected_paths": len(paths),
            "computed_times": len(updates),
            "sqlite_rows_updated": sqlite_rows_updated,
            "mtimes_updated": mtimes_updated,
            "missing_paths_count": len(missing_paths),
            "missing_paths_sample": missing_paths[:10],
            "no_timestamp_paths_count": len(no_timestamp_paths),
            "no_timestamp_paths_sample": no_timestamp_paths[:10],
            "checkpoint": {
                "busy": checkpoint[0],
                "log_frames": checkpoint[1],
                "checkpointed_frames": checkpoint[2],
            },
        },
        args.json,
    )
    return 0


def selected_repair_time_paths(args: argparse.Namespace, by_path: dict[str, Any]) -> list[str]:
    if args.metadata_backup:
        seen: set[str] = set()
        paths: list[str] = []
        with gzip.open(Path(args.metadata_backup).expanduser(), "rt", encoding="utf-8") as handle:
            for raw in handle:
                rec = json.loads(raw)
                path = rec.get("path")
                if path and path not in seen:
                    seen.add(path)
                    paths.append(path)
        return paths
    if args.rollout_path:
        return [str(Path(path).expanduser()) for path in args.rollout_path]
    return sorted(by_path)


def last_rollout_timestamp(path: Path) -> float | None:
    best: float | None = None
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            try:
                obj = json.loads(raw)
            except Exception:
                continue
            ts = parse_rollout_timestamp(obj.get("timestamp"))
            if ts is not None and (best is None or ts > best):
                best = ts
            payload = obj.get("payload")
            if not isinstance(payload, dict):
                continue
            for key in ("completed_at", "started_at", "timestamp"):
                ts = parse_rollout_timestamp(payload.get(key))
                if ts is not None and (best is None or ts > best):
                    best = ts
    return best


def parse_rollout_timestamp(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str) or not value:
        return None
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and repair Codex Desktop history provider/model metadata."
    )
    parser.add_argument("--codex-home", help="Path to CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex.")
    parser.add_argument("--provider", help="Override target model_provider. Defaults to config.toml.")
    parser.add_argument("--model", help="Override target model. Defaults to config.toml.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Read-only status report.")

    sync_parser = subparsers.add_parser("sync", help="Sync provider/model metadata only.")
    sync_parser.add_argument("--apply", action="store_true", help="Actually write changes.")
    sync_parser.add_argument("--provider-only", action="store_true", help="Only sync model_provider metadata.")
    sync_parser.add_argument("--model-only", action="store_true", help="Only sync model metadata.")
    sync_parser.add_argument("--from-provider", help="Only rewrite this source model_provider.")
    sync_parser.add_argument("--from-model", help="Only rewrite this source model.")
    sync_parser.add_argument(
        "--allow-running",
        action="store_true",
        help="Allow writing while Codex processes are detected.",
    )

    subparsers.add_parser("backup", help="Create a SQLite backup only.")

    delete_archived_parser = subparsers.add_parser(
        "delete-archived",
        help="Delete archived history records by moving JSONL files to backup and removing SQLite rows.",
    )
    delete_archived_parser.add_argument(
        "--all",
        action="store_true",
        help="Allow deleting all archived records when no narrower filters are supplied.",
    )
    delete_archived_parser.add_argument("--cwd", help="Only delete archived records for this exact cwd.")
    delete_archived_parser.add_argument(
        "--before",
        help="Only delete records archived before this local date, in YYYY-MM-DD format.",
    )
    delete_archived_parser.add_argument(
        "--older-than-days",
        type=int,
        help="Only delete records archived more than this many days ago.",
    )
    delete_archived_parser.add_argument(
        "--rollout-path",
        action="append",
        help="Only delete the archived record with this rollout JSONL path. May be repeated.",
    )
    delete_archived_parser.add_argument("--apply", action="store_true", help="Actually delete archived records.")
    delete_archived_parser.add_argument(
        "--allow-running",
        action="store_true",
        help="Allow deleting while Codex processes are detected.",
    )

    restore_parser = subparsers.add_parser("restore", help="Restore backups created by this script.")
    restore_parser.add_argument("--sqlite-backup", help="SQLite backup path to restore.")
    restore_parser.add_argument("--metadata-backup", help="JSONL metadata line backup path to restore.")
    restore_parser.add_argument("--apply", action="store_true", help="Actually restore backups.")
    restore_parser.add_argument(
        "--allow-running",
        action="store_true",
        help="Allow restoring while Codex processes are detected.",
    )

    repair_times_parser = subparsers.add_parser(
        "repair-times",
        help="Repair thread updated_at fields and rollout mtimes from rollout event timestamps.",
    )
    repair_times_parser.add_argument("--metadata-backup", help="Limit to paths listed in a metadata backup.")
    repair_times_parser.add_argument(
        "--rollout-path",
        action="append",
        help="Only repair this rollout JSONL path. May be repeated.",
    )
    repair_times_parser.add_argument("--apply", action="store_true", help="Actually write time repairs.")
    repair_times_parser.add_argument(
        "--allow-running",
        action="store_true",
        help="Allow repairing times while Codex processes are detected.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "status":
        return status(args)
    if args.command == "sync":
        return sync(args)
    if args.command == "backup":
        return backup(args)
    if args.command == "delete-archived":
        return delete_archived(args)
    if args.command == "restore":
        return restore(args)
    if args.command == "repair-times":
        return repair_times(args)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
