#!/usr/bin/env node

const childProcess = require("child_process");
const fs = require("fs");
const fsp = require("fs/promises");
const os = require("os");
const path = require("path");

const HELP = `
用法:
  npx skills add <source> --skill <name> [--global|--project] [--copy|--symlink]

参数:
  --skill <name>       要安装的 skill 目录名或 frontmatter name。
  --global             安装为全局 skill。默认选项。
  --project            安装为当前项目 skill。
  --copy               复制 skill 目录。默认选项。
  --symlink            软链到本地 skill 目录。
  --scope <scope>      global 或 project。兼容旧参数。
  --method <method>    copy 或 symlink。兼容旧参数。
  --agent <agent>      agents 或 claude-code。默认: agents。
  --dest <path>        覆盖安装根目录。
  --force              替换已存在的 skill。
  --dry-run            只打印解析结果，不写文件。
  --help               显示帮助。

示例:
  npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline
  npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline --agent claude-code --global --copy
`;

main().catch((error) => {
  console.error(`skills: ${error.message}`);
  process.exit(1);
});

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log(HELP.trim());
    return;
  }

  const command = args.shift();
  if (command !== "add") {
    throw new Error(`unknown command "${command}". Run "skills --help".`);
  }

  const source = args.shift();
  if (!source || source.startsWith("-")) {
    throw new Error("missing <source> for add.");
  }

  const options = parseOptions(args);
  const skillName = requireOption(options, "skill");
  const scope = resolveScope(options);
  const method = resolveMethod(options);
  const agent = options.agent || "agents";
  const force = Boolean(options.force);
  const dryRun = Boolean(options["dry-run"]);

  if (!["global", "project"].includes(scope)) {
    throw new Error('--scope must be "global" or "project".');
  }

  if (!["copy", "symlink"].includes(method)) {
    throw new Error('--method must be "copy" or "symlink".');
  }

  assertSupportedAgent(agent);

  const workspace = await resolveSource(source);
  try {
    if (workspace.isTemporary && method === "symlink") {
      throw new Error("remote Git sources cannot be installed with --symlink; use --copy or clone the repo locally first.");
    }

    const skillDir = await findSkillDir(workspace.root, skillName);
    const installRoot = options.dest
      ? path.resolve(options.dest)
      : resolveInstallRoot(scope, agent);
    const targetDir = path.join(installRoot, skillName);

    if (dryRun) {
      console.log(`来源: ${skillDir}`);
      console.log(`目标: ${targetDir}`);
      console.log(`方式: ${method}`);
      return;
    }

    await installSkill({ skillDir, targetDir, method, force });
    console.log(`已安装 ${skillName}`);
    console.log(`来源: ${skillDir}`);
    console.log(`目标: ${targetDir}`);
    console.log(`方式: ${method}`);
  } finally {
    if (workspace.cleanup) {
      await workspace.cleanup();
    }
  }
}

function parseOptions(args) {
  const options = {};

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];

    if (!arg.startsWith("--")) {
      throw new Error(`unexpected argument "${arg}".`);
    }

    const key = arg.slice(2);
    if (["force", "dry-run", "global", "project", "copy", "symlink"].includes(key)) {
      options[key] = true;
      continue;
    }

    const value = args[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`missing value for ${arg}.`);
    }
    options[key] = value;
    index += 1;
  }

  return options;
}

function resolveScope(options) {
  if (options.global && options.project) {
    throw new Error("--global and --project cannot be used together.");
  }

  if (options.global) {
    return "global";
  }

  if (options.project) {
    return "project";
  }

  return options.scope || "global";
}

function resolveMethod(options) {
  if (options.copy && options.symlink) {
    throw new Error("--copy and --symlink cannot be used together.");
  }

  if (options.copy) {
    return "copy";
  }

  if (options.symlink) {
    return "symlink";
  }

  return options.method || "copy";
}

function assertSupportedAgent(agent) {
  if (!["agents", "codex", "openclaw", "opencode", "claude", "claude-code"].includes(agent)) {
    throw new Error('--agent must be "agents" or "claude-code". Use --dest for a custom runtime path.');
  }
}

function requireOption(options, key) {
  if (!options[key]) {
    throw new Error(`missing --${key}.`);
  }
  return options[key];
}

async function resolveSource(source) {
  const localPath = path.resolve(source);
  if (fs.existsSync(localPath)) {
    const stats = await fsp.stat(localPath);
    if (!stats.isDirectory()) {
      throw new Error(`source is not a directory: ${source}`);
    }
    return { root: localPath, isTemporary: false };
  }

  if (!isGitSource(source)) {
    throw new Error(`source does not exist and does not look like a Git URL: ${source}`);
  }

  const tempRoot = await fsp.mkdtemp(path.join(os.tmpdir(), "baku-skills-"));
  const cloneDir = path.join(tempRoot, "repo");
  const result = childProcess.spawnSync("git", ["clone", "--depth", "1", source, cloneDir], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"]
  });

  if (result.status !== 0) {
    await fsp.rm(tempRoot, { recursive: true, force: true });
    throw new Error(`git clone failed: ${result.stderr.trim() || result.stdout.trim()}`);
  }

  return {
    root: cloneDir,
    isTemporary: true,
    cleanup: () => fsp.rm(tempRoot, { recursive: true, force: true })
  };
}

function isGitSource(source) {
  return /^(https?:\/\/|git@|ssh:\/\/)/.test(source) || source.endsWith(".git");
}

async function findSkillDir(root, skillName) {
  const skillFiles = await findSkillFiles(root, 4);
  const matches = [];

  for (const skillFile of skillFiles) {
    const skillDir = path.dirname(skillFile);
    const dirName = path.basename(skillDir);
    const frontmatterName = await readSkillName(skillFile);

    if (dirName === skillName || frontmatterName === skillName) {
      matches.push(skillDir);
    }
  }

  if (matches.length === 1) {
    return matches[0];
  }

  if (matches.length > 1) {
    throw new Error(`found multiple skills named "${skillName}": ${matches.join(", ")}`);
  }

  const seen = skillFiles.map((file) => path.relative(root, path.dirname(file))).sort();
  throw new Error(`could not find skill "${skillName}". Available skill directories: ${seen.join(", ") || "(none)"}`);
}

async function findSkillFiles(root, maxDepth) {
  const results = [];

  async function walk(dir, depth) {
    if (depth > maxDepth) {
      return;
    }

    const entries = await fsp.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name === ".git" || entry.name === "node_modules") {
        continue;
      }

      const entryPath = path.join(dir, entry.name);
      if (entry.isFile() && entry.name === "SKILL.md") {
        results.push(entryPath);
      } else if (entry.isDirectory()) {
        await walk(entryPath, depth + 1);
      }
    }
  }

  await walk(root, 0);
  return results;
}

async function readSkillName(skillFile) {
  const text = await fsp.readFile(skillFile, "utf8");
  const frontmatter = text.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatter) {
    return null;
  }

  const nameLine = frontmatter[1].split(/\r?\n/).find((line) => /^name:\s*/.test(line));
  if (!nameLine) {
    return null;
  }

  return nameLine.replace(/^name:\s*/, "").trim().replace(/^["']|["']$/g, "");
}

function resolveInstallRoot(scope, agent) {
  if (agent === "claude" || agent === "claude-code") {
    return scope === "global"
      ? path.join(os.homedir(), ".claude", "skills")
      : path.join(process.cwd(), ".claude", "skills");
  }

  if (scope === "global") {
    return path.join(os.homedir(), ".agents", "skills");
  }

  return path.join(process.cwd(), ".agents", "skills");
}

async function installSkill({ skillDir, targetDir, method, force }) {
  await fsp.mkdir(path.dirname(targetDir), { recursive: true });

  if (fs.existsSync(targetDir)) {
    if (!force) {
      throw new Error(`target already exists: ${targetDir}. Use --force to replace it.`);
    }
    await fsp.rm(targetDir, { recursive: true, force: true });
  }

  if (method === "symlink") {
    await fsp.symlink(skillDir, targetDir, "dir");
    return;
  }

  await fsp.cp(skillDir, targetDir, {
    recursive: true,
    filter: (sourcePath) => {
      const name = path.basename(sourcePath);
      return name !== ".git" && name !== "node_modules";
    }
  });
}
