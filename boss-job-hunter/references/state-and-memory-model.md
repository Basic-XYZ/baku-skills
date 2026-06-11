# 状态与记忆模型

状态只用于让未来由用户主动发起的搜索更快、更准。简历和候选人画像属于敏感数据，只有用户明确同意时才能持久化。

## 隐私规则

- 保存原始简历文本、结构化画像或搜索历史前必须询问用户。
- 优先使用用户可控的本地持久化。
- 除非用户明确要求，不把简历数据上传到远程存储。
- 不保存密钥、账号凭证、cookie 或 BOSS 会话数据。
- 如果用户要求忘记数据，必须删除或停止使用已保存状态。

## 核心状态

### original_resume

用户原始简历文本，或本地简历文件指针。它是事实声明的 source of truth。

建议字段：

- `source_type`：`text`、`file` 或 `user_summary`。
- `source_path`：用户提供本地文件时记录路径。
- `content_summary`：简短摘要，不能替代原始来源。
- `last_updated_at`：日期或会话标记。

### candidate_profile

从原始简历和用户澄清中提取的结构化画像。

建议字段：

- `years_experience`：工作年限。
- `target_level`：目标职级。
- `core_stack`：核心技术栈。
- `secondary_stack`：辅助技术栈。
- `project_domains`：项目领域。
- `business_domains`：业务领域。
- `measurable_outcomes`：可量化成果。
- `seniority_signals`：资深度信号。
- `strengths`：优势。
- `resume_gaps`：简历缺口。
- `interview_selling_points`：面试卖点。

### job_preferences

当前搜索要求。硬性筛选和软性排序信号要分开。

建议字段：

- `target_cities`：目标城市。
- `remote_preference`：远程偏好。
- `salary_floor`：薪资底线。
- `salary_target`：目标薪资。
- `target_directions`：目标方向。
- `unacceptable_directions`：不可接受方向。
- `company_size_preference`：公司规模偏好。
- `industry_preference`：行业偏好。
- `financing_stage_preference`：融资阶段偏好。
- `stability_preference`：稳定性偏好。
- `outsourcing_tolerance`：外包容忍度。
- `overtime_tolerance`：加班容忍度。
- `commute_limits`：通勤限制。
- `notice_period`：到岗周期。

### capability_snapshot

本轮搜索周期的能力状态。

建议字段：

- `proven_capabilities`：已证明能力。
- `capabilities_to_emphasize`：应重点强调的能力。
- `weak_but_repairable_signals`：较弱但可修复的信号。
- `true_gaps`：真实缺口。
- `projects_ready_for_deep_dive`：可以面试深挖的项目。
- `projects_needing_more_metrics`：需要补指标的项目。
- `interview_risk_topics`：面试风险话题。

## 会话状态

### search_passes

每轮主动搜索记录一条。

建议字段：

- `keyword_group`：关键词组。
- `filters`：筛选条件。
- `reviewed_count`：查看数量。
- `kept_count`：保留数量。
- `rejected_count`：拒绝数量。
- `access_notes`：访问说明。
- `quality_notes`：质量说明。
- `next_adjustment`：下一步调整。

### job_evidence

每个值得保留、重点拒绝或之后复查的岗位记录一条。

建议字段：

- `title`：岗位名。
- `company`：公司名。
- `url_or_page_identity`：URL 或页面身份。
- `city`：城市。
- `district`：区域。
- `salary_range`：薪资范围。
- `experience_requirement`：经验要求。
- `education_requirement`：学历要求。
- `company_size`：公司规模。
- `industry`：行业。
- `tech_stack`：技术栈。
- `business_direction`：业务方向。
- `jd_summary`：JD 摘要。
- `recruiter_or_posting_signals`：招聘者或发布信号。
- `risk_signals`：风险信号。
- `source_confidence`：`high`、`medium` 或 `low`。

### score_breakdown

附加到每个保留岗位。

建议字段：

- `technical_match`：技术匹配。
- `project_domain_match`：项目 / 领域匹配。
- `seniority_years_fit`：职级和年限匹配。
- `salary_location_fit`：薪资和地点匹配。
- `company_preference_fit`：公司偏好匹配。
- `interview_probability`：面试概率。
- `resume_repairability`：简历可修复性。
- `total_score`：总分。
- `recommendation_band`：推荐分档。
- `confidence`：置信度。

## 长期记忆

### company_memory

用于避免重复推荐已知不合适公司，并记住有潜力的公司。

建议字段：

- `company`：公司名。
- `status`：`viewed`、`rejected`、`promising`、`applied`、`interviewed`、`blacklisted` 或 `deferred`。
- `reason`：原因。
- `related_roles`：相关岗位。
- `last_seen_at`：最近看到时间。

### growth_notes

用于跨会话保留成长线索。

建议字段：

- `resume_improvement_points`：简历优化点。
- `capability_gaps`：能力缺口。
- `interview_prep_backlog`：面试准备 backlog。
- `keyword_gaps`：关键词缺口。
- `preference_changes`：偏好变化。
- `next_search_hypotheses`：下一轮搜索假设。

## 更新策略

每次主动搜索会话结束时，只提出记忆更新建议，不静默保存。用户应该能接受、拒绝或编辑这些更新。
