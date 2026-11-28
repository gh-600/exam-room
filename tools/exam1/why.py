"""Why each question may be on the exam: the study-guide bullet it maps to, plus the clues that suggest the topic is examinable.

Clue types (kept honest: none of them is knowledge of the real item pool):
- SG    the study guide names the skill (the bullets illustrate what is assessed)
- TEST  the Learn unit says the pattern is tested in the exam
- DG    the Learn unit flags it as "Decision guidance", "Important" or "Key takeaway"
- REP   the idea is repeated in several Learn units or modules
- CODE  the unit shows it as YAML/JSON/CLI, the raw material of code-completion items
- LIVE  a candidate who passed in Aug 2026 reported the topic (one first-hand source)
- DOCS  GitHub Docs define the behaviour precisely, so a right answer is unambiguous
- TRAP  a well-known confusion that makes a good distractor
"""

LIVE = "A candidate who passed the live exam (Aug 2026) reported this topic: "

WHY = {
# ---------------- D1
"x1-d1-plan-first": ("Configure agent planning to be distinct from agent execution", [
    ("DG", "M2 unit 4 gives explicit decision guidance: plan-first for high-risk work (workflows, infra, auth, production)."),
    ("REP", "Plan-first versus plan + execution is the central choice of the unit and returns in M6 (risk-based autonomy)."),
    ("TRAP", "Both options are reviewed before merge; only the timing of validation differs, which makes an easy distractor.")]),
"x1-d1-read-only-planner": ("Prevent agent action until the agent checked and approved", [
    ("DG", "M2 unit 4: \"Treat instructions not to edit as guidance; treat tool allowlists and gates as enforcement.\""),
    ("REP", "Guidance versus enforcement recurs in M2 u.7 (hooks), M3 (tools) and M6 u.3 (\"controls in docs only\")."),
    ("TRAP", "Instructions look like a control. Exams like options that only ask the model to behave.")]),
"x1-d1-control-plane-statements": ("Plan and implement the degree of agent autonomy, including guardrails", [
    ("DG", "M1 unit 4 has a \"Controls at a glance\" table: each GitHub control and what it enforces."),
    ("SG", "The audience profile describes GitHub as \"the system of record and control plane\"."),
    ("TRAP", "Environment reviewers act before the job starts, not after.")]),
"x1-d1-job-outputs": ("Configure an agent to output a structured plan", [
    ("CODE", "M2 unit 6 shows step outputs, job outputs and `needs` in YAML, a natural code-completion item."),
    ("DG", "The unit stresses \"Outputs are workflow contracts\" and contrasts them with `env`."),
    ("LIVE", LIVE + "completing workflow YAML.")]),
"x1-d1-critical-tier": ("Plan and implement the degree of agent autonomy, including guardrails", [
    ("REP", "The risk tiers (low, medium, high, critical) appear in M2 u.6 and again in M6 u.2."),
    ("DOCS", "Docs define exactly when environment secrets become available (after approval)."),
    ("TRAP", "Each tier has a different control; picking the control of the neighbouring tier is the usual mistake.")]),
"x1-d1-evidence": ("Configure agent to produce inspectable artifacts within standard development tooling", [
    ("REP", "\"Minimum observability set\" appears twice in M2 u.7 and returns in M4 u.6 and M6 u.6."),
    ("DG", "Explicit principle: \"Evidence should be traceable to a specific workflow run and a specific commit.\"")]),
"x1-d1-plan-first-sequence": ("Validate agent plans", [
    ("DG", "M2 unit 4 lists the plan-first steps in order, the raw material of a build-list item."),
    ("TRAP", "The plan + execution PR is a tempting distractor in the sequence.")]),
"x1-d1-defensive-gating": ("Configure an agent to be invoked in a CI workflow", [
    ("CODE", "M2 unit 6 gives a full YAML example of a job-level `if: github.event_name == 'pull_request'`."),
    ("REP", "The unit also contrasts the `github`, `vars` and `env` contexts, a classic matching or option set.")]),
"c1": ("Identify and mitigate common anti-patterns in agents", [
    ("DG", "M6 unit 3: \"Make sure require CODEOWNERS review is enabled, or CODEOWNERS becomes advisory only.\""),
    ("REP", "CODEOWNERS appears in M1, M2, M4 and M6."),
    ("TRAP", "Order in the CODEOWNERS file: the last match wins.")]),
"c7": ("Identify and mitigate common anti-patterns in agents", [
    ("DG", "M1 unit 5 has a risk-to-mitigation table; \"planless execution\" is its first row."),
    ("SG", "The study guide names anti-patterns explicitly.")]),
"c8": ("Identify steps for agents to perform", [
    ("DG", "M2 unit 2: \"Most teams start by scoping agents to the implementation and validation stages.\""),
    ("REP", "\"Agents propose; humans and policy accept\" appears in M2 and M4.")]),
# ---------------- D2
"x1-d2-mcp-secret-series": ("Configure an agent to handle environment-specific constraints", [
    ("DG", "M2 unit 7: \"The agent's runtime environment has its own secret boundary.\""),
    ("DOCS", "Docs state the exact rule: only Agents secrets prefixed `COPILOT_MCP_` reach the MCP configuration."),
    ("LIVE", LIVE + "restricting MCP tools and permission scopes."),
    ("TRAP", "Actions secrets look like the obvious answer.")]),
"x1-d2-setup-steps": ("Configure an agent to handle environment-specific constraints", [
    ("SG", "The audience profile names \"Copilot setup steps\" explicitly."),
    ("DOCS", "Fixed file path and fixed job name: an unambiguous detail.")]),
"x1-d2-mcp-config": ("Add an MCP server as a tool to an agent", [
    ("SG", "Four study-guide bullets are about MCP servers."),
    ("CODE", "JSON configuration with `type`, `url` and `tools`: a natural drop-down item."),
    ("LIVE", LIVE + "restricting the tools of an MCP server."),
    ("TRAP", "`servers` (VS Code) versus `mcpServers` (cloud agent).")]),
"x1-d2-app-token": ("Configure agent tool permissions", [
    ("DG", "M3 unit 5 has a section on trigger behaviour of `GITHUB_TOKEN` versus App tokens and PATs."),
    ("LIVE", LIVE + "`GITHUB_TOKEN` scope and permissions blocks."),
    ("TRAP", "Adding `contents: write` doesn't help, a common wrong fix.")]),
"x1-d2-approve-workflows": ("Enable an agent to perform autonomous actions, including creating branches and pull requests", [
    ("DG", "M1 unit 4 presents \"Approve and run workflows\" as a built-in guardrail; M2 u.5 repeats it."),
    ("DOCS", "Docs describe the default precisely, including who can approve.")]),
"x1-d2-hook-events": ("Implement traceability and accountability for agent actions", [
    ("REP", "Hooks appear in M2 u.7, M4 u.7 and M6 u.3."),
    ("LIVE", LIVE + "hooks as guardrails."),
    ("TRAP", "Only a pre-execution hook can block; the others only observe.")]),
"x1-d2-cloud-agent-statements": ("Evaluate the execution context for an agent", [
    ("DG", "M3 unit 5 is a list of built-in limits of the cloud agent."),
    ("DOCS", "Docs state who can't approve and what the firewall covers: crisp true/false facts.")]),
"x1-d2-hook-log": ("Implement escalation paths", [
    ("CODE", "M4 unit 7 shows this exact log output and names the `preToolUse` hook."),
    ("LIVE", LIVE + "diagnosing from logs and hooks as guardrails.")]),
"x1-d2-lock-file": ("Configure an agent to be invoked in a CI workflow", [
    ("DG", "M3 unit 2 explains that the Markdown is compiled into a lock file that Actions executes."),
    ("TRAP", "Editing only the `.md` file feels enough. The study guide allows commonly used preview features, so treat this as medium likelihood.")]),
"c3": ("Configure MCP allow lists", [
    ("DG", "M2 unit 7: \"prefer enabling a narrow tool subset rather than broad wildcards\"."),
    ("LIVE", LIVE + "restricting MCP tools."),
    ("TRAP", "`*` plus an instruction is the classic guidance-instead-of-enforcement distractor.")]),
"c4": ("Configure an agent to handle environment-specific constraints", [
    ("DG", "M3 unit 4 lists network isolation and allowlisted outbound access among the guardrails."),
    ("DOCS", "Docs describe the firewall warning in the PR and the custom allowlist.")]),
# ---------------- D3
"x1-d3-source-of-truth": ("Prevent conflicting context", [
    ("DG", "M5 units 2 and 4 both give the same mapping list: requirements → issue, decisions → PR, rules → instructions, results → runs."),
    ("SG", "The study guide has a skill group for memory and state continuity.")]),
"x1-d3-resume": ("Resume agent work without repeating steps or diverging from prior decisions", [
    ("SG", "The study-guide bullet matches the unit's resume flow almost word for word."),
    ("DG", "M5 unit 3 gives a numbered resume flow.")]),
"x1-d3-drift": ("Detect and correct drift during extended agent execution", [
    ("SG", "Drift detection and correction is a named skill."),
    ("DG", "M5 unit 3 lists the signs of drift and the steps to correct it.")]),
"x1-d3-retention": ("Define memory expiration, pruning, and reset rules", [
    ("DG", "M5 unit 3 puts the retention limits in bold, and unit 5 repeats the 90-day default."),
    ("DOCS", "Numbers (90, 1–90, 1–400) are exact and testable."),
    ("TRAP", "`retention-days` can't exceed the repository limit.")]),
"x1-d3-continuity-statements": ("Prevent stale context", [
    ("SG", "Share state, prevent conflicting context, prevent stale context: three named bullets, one per statement."),
    ("DG", "M5 unit 4: \"Agent state should be shared using durable references, not copied context.\"")]),
"x1-d3-reset": ("Define memory expiration, pruning, and reset rules", [
    ("SG", "\"Reset rules\" is named in the study guide."),
    ("TRAP", "Pruning, summarizing and resetting are easily confused.")]),
"x1-d3-memory-vs-instructions": ("Choose between short-term, long-term, and external memory", [
    ("SG", "The study guide links Copilot Memory as the documentation for this domain."),
    ("LIVE", LIVE + "Copilot Memory."),
    ("TRAP", "A stored memory looks like a rule, but Copilot only uses it when it judges it relevant.")]),
# ---------------- D4
"x1-d4-real-intent": ("Align evaluation criteria with development intent", [
    ("DG", "M2 unit 3 tip: \"CI passed is necessary, but not always sufficient.\""),
    ("REP", "M1 u.3 and u.5 repeat that evaluation rests on system signals, not on the agent's confidence.")]),
"x1-d4-root-cause": ("Classify root causes, including reasoning errors, tool misuse, and context or environment issues", [
    ("SG", "The bullet names the three categories used in M5 unit 6."),
    ("DG", "The unit gives examples per category, ready-made matching items.")]),
"x1-d4-feedback-loop": ("Revise instructions, workflows, or constraints", [
    ("DG", "M5 unit 6 gives the feedback loop as numbered steps: a build-list item."),
    ("TRAP", "Removing checks or widening permissions are tempting \"fixes\".")]),
"x1-d4-required-check-series": ("Generate evaluation signals by using automated scanning tools", [
    ("REP", "Required status checks appear in nearly every module."),
    ("DG", "M2 unit 3: \"success is enforced by the system, not assumed by the agent\".")]),
"x1-d4-skipped-check": ("Identify failures by using logs, plans, traces, outputs, and workflow artifacts", [
    ("DOCS", "Docs state it bluntly: a skipped job reports Success, even for a required check."),
    ("TRAP", "Skipped job (passes) versus skipped workflow (pending, blocks).")]),
"x1-d4-evaluation-statements": ("Identify qualitative and quantitative evaluation signals to evaluate agents", [
    ("DG", "M1 unit 5: \"A passing build does not automatically mean the change is complete.\""),
    ("REP", "Acceptance criteria in the issue appear in M2, M5 u.3 and u.5.")]),
"x1-d4-trigger-fix": ("Refine tool usage and tool access", [
    ("DG", "M5 unit 6 lists \"Ensure workflows trigger on the correct events (push, pull_request)\" under tool configuration."),
    ("LIVE", LIVE + "diagnosing problems from logs and workflow YAML.")]),
"x1-d4-dependency-review": ("Generate evaluation signals by using automated scanning tools", [
    ("SG", "\"Automated scanning tools\" is a named bullet."),
    ("REP", "Security signals appear in M1 u.3, M2 u.3 and M5 u.5.")]),
# ---------------- D5
"x1-d5-fan-in": ("Apply an orchestration pattern to coordinate multiple agents", [
    ("TEST", "M4 unit 3 says of fan-out/fan-in with `needs`: \"This pattern is tested in the exam\". The strongest clue in the material."),
    ("CODE", "The unit gives the full YAML."),
    ("LIVE", LIVE + "completing workflow YAML.")]),
"x1-d5-workflow-run": ("Apply an orchestration pattern to coordinate multiple agents", [
    ("CODE", "M4 unit 3 shows the `workflow_run` YAML for sequential orchestration."),
    ("TRAP", "`workflow_call` and `workflow_dispatch` are close distractors.")]),
"x1-d5-concurrency-group": ("Configure agent isolation for parallel execution", [
    ("DG", "M4 unit 4 has a dedicated section and a Note on the group name; M6 u.4 reuses concurrency."),
    ("DOCS", "Docs: group names must be unique across workflows."),
    ("TRAP", "`${{ github.ref }}` alone, matrix, and job-level concurrency are all offered as alternatives in the unit.")]),
"x1-d5-conflict-types": ("Detect and resolve agent conflicts, including overlapping code changes, duplicated effort, and contradictory outputs", [
    ("SG", "The bullet names the conflict types almost exactly."),
    ("DG", "M4 unit 5 lists four types, a ready-made matching item.")]),
"x1-d5-merge-validation": ("Detect and resolve agent conflicts, including overlapping code changes, duplicated effort, and contradictory outputs", [
    ("CODE", "M4 unit 5 shows the merge validation step."),
    ("DG", "\"If this is a required check, conflicts become enforceable.\"")]),
"x1-d5-artifact-audit": ("Perform post-hoc analysis of multi-agent behavior", [
    ("DG", "M4 unit 6 names the exact audit log query `action:artifact.destroy`, a precise, testable fact."),
    ("SG", "\"Post-hoc analysis\" is a named bullet.")]),
"x1-d5-subagent-frontmatter": ("Update, reconfigure, or replace agents without disrupting active workflows", [
    ("DG", "M4 unit 7 has a table of the two frontmatter settings and their effect on orchestration."),
    ("SG", "The audience profile names \"Configuring custom agents\" as a responsibility."),
    ("TRAP", "The two settings sound alike and act on different callers.")]),
"x1-d5-isolation-statements": ("Configure agent isolation for parallel execution", [
    ("DG", "M4 unit 4: \"Why not job-level or matrix-based concurrency?\" is answered explicitly."),
    ("TRAP", "Matrix versus concurrency.")]),
"x1-d5-ruleset-bypass": ("Respond to degraded behavior or coordination across agents", [
    ("DG", "M4 unit 7 has a dedicated section on adding Copilot as a ruleset bypass actor."),
    ("TRAP", "Bypass lists are normally a wrong answer; here the narrow bypass is the right one, so read the constraint.")]),
"c5": ("Apply an orchestration pattern to coordinate multiple agents", [
    ("DG", "M4 unit 3 key takeaway: parallel only when agents work on isolated paths."),
    ("REP", "M4 u.2 uses the same dependency-agent example.")]),
# ---------------- D6
"x1-d6-autonomy-levels": ("Assign autonomy levels to maximize delivery speed while remaining compliant with organizational security and Responsible AI standards", [
    ("SG", "Autonomy levels are a named skill group."),
    ("DG", "M6 unit 2 defines four named levels, a ready-made matching item.")]),
"x1-d6-risk-routing": ("Classify agent actions by operational, security, and compliance risk to right-size human interventions", [
    ("DG", "M6 unit 2: \"Don't rely on narrative explanations of risk. Use a machine-readable signal and enforce routing.\""),
    ("CODE", "The unit gives the complete YAML with `needs.plan.outputs.risk` and `environment`.")]),
"x1-d6-security-failure": ("Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes", [
    ("DG", "M6 unit 7: \"Investigate security failures instead of repeatedly retrying\"."),
    ("REP", "\"Escalate after the same failure twice\" appears in M2 u.7, M4 u.5 and u.7.")]),
"x1-d6-rubber-stamping": ("Preserve execution velocity by minimizing approvals that do not materially reduce risk", [
    ("DG", "M6 unit 7 has an anti-pattern table with \"Rubber-stamping\"; M6 u.4 lists how to avoid governance fatigue."),
    ("TRAP", "\"Add more approvals\" looks safe but is the opposite of the remedy.")]),
"x1-d6-cli-tool-scope": ("Scope permissions and execution contexts to enforce least-privilege access", [
    ("DG", "M6 unit 2: \"Match tool access to consequence\", with a Copilot CLI `--allow-tool` example."),
    ("DOCS", "Docs define precedence: `--deny-tool` wins over `--allow-tool`.")]),
"x1-d6-progressive-autonomy": ("Assign autonomy levels to maximize delivery speed while remaining compliant with organizational security and Responsible AI standards", [
    ("DG", "M6 unit 2 lists four phases in order, a ready-made build-list item.")]),
"x1-d6-governance-statements": ("Identify the subset of actions that require human judgment", [
    ("DG", "M6 unit 4 tip: humans at decision points, not every step. M6 u.3: \"Controls in docs only is an anti-pattern\"."),
    ("SG", "The bullet matches the tip almost word for word.")]),
"c2": ("Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes", [
    ("DG", "M6 unit 3: \"If a workflow accesses production secrets, treat it as critical risk and gate it.\""),
    ("REP", "Environments with required reviewers appear in M1, M2, M3, M4 and M6.")]),
"c6": ("Scope permissions and execution contexts to enforce least-privilege access", [
    ("CODE", "M6 unit 5 shows job-level permissions in YAML."),
    ("LIVE", LIVE + "`id-token: write` for OIDC and permissions blocks."),
    ("DOCS", "Docs: declaring one permission sets every other one to `none`.")]),
# ---------------- sample bank (former Module 3)
"m3-u4-least-priv": ("Configure agent tool permissions", [
    ("REP", "Least-privilege tokens appear in M1, M2, M3 and M6."),
    ("LIVE", LIVE + "`GITHUB_TOKEN` scope and permissions blocks.")]),
"m3-u3-api-center": ("Configure the MCP registries", [
    ("DG", "M3 unit 3 gives the registry requirements as numbered steps, including the Azure API Center option."),
    ("DOCS", "Exact endpoints and the \"base URL only\" rule are precise, testable details.")]),
"m3-u3-registry-only": ("Configure MCP allow lists", [
    ("DG", "M3 unit 3 Note: under Registry only, even local servers must be in the registry with matching IDs."),
    ("TRAP", "Local servers seem exempt from the policy.")]),
"m3-u5-rollback": ("Implement rollbacks", [
    ("SG", "\"Implement rollbacks\" is a named bullet."),
    ("TRAP", "Force-push and bypass lists are standard wrong options.")]),
"m3-u3-three-roles": ("Configure MCP servers", [
    ("DG", "M3 unit 3 states the three roles in one list: server exposes, registry makes discoverable, allow list decides.")]),
"m3-u3-remote-config": ("Configure a GitHub remote MCP server", [
    ("SG", "The bullet names the GitHub remote MCP server explicitly."),
    ("CODE", "M3 unit 3 gives the URL and server type, a natural drop-down item.")]),
}

LABEL = {"SG": "Study guide", "TEST": "Learn says it is tested", "DG": "Emphasised in Learn", "REP": "Repeated across modules",
         "CODE": "Code in the unit", "LIVE": "Reported from the live exam", "DOCS": "Precise in GitHub Docs", "TRAP": "Classic trap"}


def why(qid, domain):
    skill, clues = WHY[qid]
    strong = any(k in ("TEST", "LIVE") for k, _ in clues) or sum(k in ("DG", "SG", "REP") for k, _ in clues) >= 2
    return {"skill": skill, "strength": "strong" if strong else "moderate",
            "clues": [{"kind": LABEL[k], "text": t} for k, t in clues]}
