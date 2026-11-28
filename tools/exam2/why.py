"""Why each question of full exam 2 may be on the exam: the study-guide bullet it maps to, plus the clues that suggest the topic is examinable.

Clue types (kept honest: none of them is knowledge of the real item pool):
- SG    the study guide names the skill (the bullets illustrate what is assessed)
- TEST  the Learn unit says the pattern is tested in the exam
- DG    the Learn unit flags it as "Decision guidance", "Important", "Tip" or "Key takeaway", or gives it as a numbered procedure
- REP   the idea is repeated in several Learn units or modules
- CODE  the unit shows it as YAML/JSON/CLI, the raw material of code-completion items
- LIVE  a candidate who passed in Aug 2026 reported the topic (one first-hand source)
- DOCS  GitHub Docs define the behaviour precisely, so a right answer is unambiguous
- TRAP  a well-known confusion that makes a good distractor
"""

LIVE = "A candidate who passed the live exam (Aug 2026) reported this topic: "

WHY = {
# ---------------- D1
"x2-d1-task-contract": ("Define inputs, outputs, and success criteria for agents", [
    ("SG", "The bullet and the title of M2 unit 3 are almost identical."),
    ("DG", "The unit gives a complete example task contract, with each item under its heading."),
    ("TRAP", "Constraints read like acceptance conditions, but the unit lists them under Inputs.")]),
"x2-d1-auto-merge": ("Configure human intervention for autonomous agents without slowing delivery", [
    ("SG", "The bullet asks for intervention that does not slow delivery, which is the point of this scenario."),
    ("DG", "M2 unit 6 autonomy table: low-risk paths merge automatically after the required checks."),
    ("REP", "M6 unit 4 repeats it as a tip: people at decision points, not at every step.")]),
"x2-d1-evidence-jobs": ("Configure agent to produce inspectable artifacts within standard development tooling", [
    ("CODE", "M2 unit 7 shows `actions/upload-artifact` in YAML and states the upload and download pattern."),
    ("REP", "Artifacts as evidence return in M4 unit 6 and M6 unit 6."),
    ("LIVE", LIVE + "completing workflow YAML.")]),
"x2-d1-plan-elements": ("Configure an agent to output a structured plan", [
    ("SG", "The bullet names the structured plan."),
    ("DG", "M1 unit 3 gives the three elements in a Tip box."),
    ("REP", "The pull request template of M2 unit 5 has a field for each of the three.")]),
"x2-d1-plan-gate": ("Validate agent plans", [
    ("DG", "M2 unit 5: a required status check turns \"include a plan\" into a system guarantee."),
    ("REP", "Guidance versus enforcement recurs in M2 unit 4, M2 unit 7 and M6 unit 3."),
    ("TRAP", "A template and an instruction both look like controls. Neither blocks a merge.")]),
"x2-d1-anti-patterns": ("Identify and mitigate common anti-patterns in agents", [
    ("SG", "The bullet asks to identify and to mitigate, which is the shape of this item."),
    ("DG", "M1 unit 5 has a table that maps each anti-pattern to GitHub controls.")]),
"x2-d1-plan-boundaries": ("Prevent agent action until the agent checked and approved", [
    ("DG", "M2 unit 4 lists four ways to enforce the planning boundary, including handoff and tool gating."),
    ("TRAP", "Plan and execution is often misread as \"no validation\". Validation is still required before merge.")]),
"x2-d1-scope-complete": ("Identify steps for agents to perform", [
    ("SG", "The bullet asks which steps an agent performs."),
    ("DG", "M2 unit 2 ends its example by stating when the agent's scoped responsibility is complete."),
    ("REP", "\"Agents propose; humans and policy accept\" appears in M2 unit 2 and in M4 unit 2.")]),
# ---------------- D2
"x2-d2-required-tools": ("Identify required tools", [
    ("SG", "The bullet asks to identify the tools that an agent requires."),
    ("DOCS", "Docs list the tool aliases: `agent` invokes another custom agent, `execute` runs commands, `edit` changes files."),
    ("TRAP", "The name of the other agent looks like a tool name. Unrecognized names are ignored.")]),
"x2-d2-mcp-rollout": ("Configure the MCP registries", [
    ("SG", "The bullet names the MCP registries."),
    ("DG", "M3 unit 3 gives this flow as a numbered list, \"A practical GitHub workflow\".")]),
"x2-d2-ci-invoke": ("Configure an agent to be invoked in a CI workflow", [
    ("SG", "The bullet names the CI workflow."),
    ("CODE", "M3 unit 4 shows the steps, with `--agent`, `-p` and `--no-ask-user`."),
    ("LIVE", LIVE + "code completion items.")]),
"x2-d2-github-mcp-scope": ("Configure a GitHub remote MCP server", [
    ("SG", "The bullet names the GitHub remote MCP server."),
    ("DOCS", "Docs state the default scope of the token and the exact name of the secret that widens it."),
    ("TRAP", "The firewall and GitHub Actions secrets are the usual wrong turns.")]),
"x2-d2-tools-statements": ("Configure agent tools", [
    ("SG", "The bullet names the configuration of agent tools."),
    ("DOCS", "Docs define the three cases exactly: omitted, empty list, specific list."),
    ("TRAP", "An omitted `tools` property looks restrictive and is the widest setting.")]),
"x2-d2-repo-access": ("Configure an agent's scope to a specific repository", [
    ("SG", "The bullet names the scope to a specific repository."),
    ("DG", "M3 unit 4 calls repository scope the first boundary and shows where it is configured."),
    ("DOCS", "Docs name the control: Repository access, with Selected repositories.")]),
"x2-d2-error-handling": ("Implement error handling", [
    ("SG", "\"Implement error handling\" is a named bullet."),
    ("CODE", "M3 unit 5 shows `continue-on-error: false` on the agent step."),
    ("DOCS", "Docs define what `continue-on-error: true` does to the job.")]),
"x2-d2-contexts": ("Configure an agent to be invoked in a CI workflow", [
    ("DG", "M2 unit 6 has a section named \"Contexts: GitHub vs vars vs env\" with one line for each."),
    ("CODE", "The unit shows `github.event_name` in a job condition."),
    ("LIVE", LIVE + "drop-down items in workflow YAML.")]),
"x2-d2-base-branch": ("Configure an agent to use branch-based scope", [
    ("SG", "The bullet names branch-based scope."),
    ("DG", "M3 unit 4 has a section with the same title, about selecting the base branch."),
    ("DOCS", "Docs give the CLI option: `--base`.")]),
"x2-d2-retries": ("Implement retries", [
    ("SG", "\"Implement retries\" is a named bullet."),
    ("CODE", "M3 unit 5 shows a retry loop of three attempts."),
    ("REP", "Bounded retries return in M2 unit 7, M4 unit 7 and M6 unit 7.")]),
"x2-d2-registry-cloud-agent": ("Configure MCP allow lists", [
    ("SG", "The bullet names the MCP allow lists."),
    ("DOCS", "Docs have a table of supported surfaces. This kind of detail can change, so check the page before the exam."),
    ("TRAP", "It is natural to assume that an organization policy covers every Copilot surface.")]),
# ---------------- D3
"x2-d3-stale-series": ("Prevent stale context", [
    ("SG", "\"Prevent stale context\" is a named bullet."),
    ("DG", "M5 unit 4 lists an outdated pull request as stale context and mentions the up-to-date requirement."),
    ("DOCS", "Docs define strict status checks, and state that a re-run uses the same commit SHA.")]),
"x2-d3-scope-memory": ("Scope agent memory to task-relevant information", [
    ("SG", "The bullet and the section title in M5 unit 2 match."),
    ("DG", "The unit lists what is relevant and what should not be stored.")]),
"x2-d3-durable-progress": ("Capture task progress and decisions as durable artifacts", [
    ("SG", "The bullet names durable artifacts."),
    ("DG", "M5 unit 3 gives the four steps as an example, a ready-made build-list item.")]),
"x2-d3-memory-types": ("Choose between short-term, long-term, and external memory", [
    ("SG", "The bullet names the three types."),
    ("DG", "M5 unit 2 defines each type under its own heading.")]),
"x2-d3-summarize": ("Define memory expiration, pruning, and reset rules", [
    ("SG", "The bullet names expiration, pruning and reset."),
    ("DG", "M5 unit 3 has a subsection for each of expiration, pruning, summarization and reset."),
    ("TRAP", "Reset and pruning are the neighboring concepts that look like a cleanup.")]),
# ---------------- D4
"x2-d4-path-filter": ("Identify failures by using logs, plans, traces, outputs, and workflow artifacts", [
    ("DOCS", "The troubleshooting page for required status checks has this exact example."),
    ("TRAP", "A skipped job reports Success. A skipped workflow leaves the check pending. The two are easy to swap."),
    ("LIVE", LIVE + "reading logs and status to diagnose a problem.")]),
"x2-d4-refine-memory": ("Refine memory usage", [
    ("SG", "\"Refine memory usage\" is a named bullet."),
    ("DG", "M5 unit 6 names \"Memory and state\" as one of three areas to adjust, with these actions.")]),
"x2-d4-codeql-job": ("Generate evaluation signals by using automated scanning tools", [
    ("SG", "The bullet names automated scanning tools."),
    ("CODE", "M2 unit 3 shows this job, including the `permissions` block."),
    ("LIVE", LIVE + "permissions blocks in workflow YAML.")]),
"x2-d4-ambiguity": ("Specify expected outcomes and operational constraints for agent tasks", [
    ("SG", "The bullet names expected outcomes and constraints."),
    ("DG", "M6 unit 7, \"Prevent ambiguity before execution\", lists what a task must define."),
    ("REP", "The task contract of M2 unit 3 and the criteria of M5 unit 5 say the same.")]),
"x2-d4-signals-statements": ("Identify qualitative and quantitative evaluation signals to evaluate agents", [
    ("SG", "The bullet names evaluation signals."),
    ("DG", "M1 unit 3 lists the signals and states the \"key lesson\" about the agent's confidence.")]),
"x2-d4-tune-instructions": ("Revise instructions, workflows, or constraints", [
    ("SG", "The bullet names the revision of instructions."),
    ("DG", "M5 unit 6 names \"Prompts and instructions\" as an area to adjust, with repository instruction files."),
    ("TRAP", "Weakening the check or the workflow makes the symptom disappear.")]),
"x2-d4-classify": ("Classify root causes, including reasoning errors, tool misuse, and context or environment issues", [
    ("SG", "The bullet lists the categories by name."),
    ("DG", "M5 unit 6 defines each category with examples."),
    ("TRAP", "All checks pass, which hides the failure.")]),
"x2-d4-tool-access": ("Refine tool usage and tool access", [
    ("SG", "The bullet names tool access."),
    ("DOCS", "Docs: an agent profile without `tools` enables all tools."),
    ("REP", "Allowlists for tools appear in M2 unit 4 and M2 unit 7.")]),
"x2-d4-align-intent": ("Align evaluation criteria with development intent", [
    ("SG", "The bullet names development intent."),
    ("DG", "M5 unit 6 has a section \"Compare intent with results\"."),
    ("REP", "M2 unit 3 tip: \"CI passed\" is necessary, but not always sufficient.")]),
# ---------------- D5
"x2-d5-workflow-run-gate": ("Apply an orchestration pattern to coordinate multiple agents", [
    ("CODE", "M4 unit 3 shows `workflow_run` with `workflows` and `types: [completed]`."),
    ("DOCS", "Docs: the workflow runs regardless of the conclusion of the previous one."),
    ("LIVE", LIVE + "completing workflow YAML.")]),
"x2-d5-live-log": ("Identify failed, partial, or stalled agent executions", [
    ("CODE", "M4 unit 7 shows the command and says what it is for."),
    ("LIVE", LIVE + "logs and session history."),
    ("DOCS", "Docs describe `--log` and `--follow`.")]),
"x2-d5-artifact-coordination": ("Configure multi-agent workflows to produce artifacts suitable for review and audit", [
    ("SG", "The bullet names artifacts for review and audit."),
    ("DG", "M4 unit 3 gives the pattern as three numbered steps.")]),
"x2-d5-incompatible-fixes": ("Implement multi-agent recovery patterns, including rollback and human-in-the-loop", [
    ("SG", "The bullet names human-in-the-loop recovery."),
    ("DG", "M4 unit 5 lists this exact case as an escalation threshold."),
    ("REP", "Escalation after repeated failure returns in M2 unit 7 and M4 unit 7.")]),
"x2-d5-pr-sections": ("Document key decisions, handoffs, and outcomes across agents", [
    ("SG", "The bullet names decisions and handoffs."),
    ("DG", "M4 unit 6 gives a pull request structure with these sections.")]),
"x2-d5-add-agent": ("Add agents to existing multi-agent workflows", [
    ("SG", "The bullet names adding agents."),
    ("DG", "M4 unit 4 describes branch, workflow and permission isolation for each agent."),
    ("REP", "M4 unit 2 defines scope boundaries by path.")]),
"x2-d5-retire-agent": ("Retire agents while preserving auditability and workflow continuity", [
    ("SG", "The bullet names retirement, auditability and continuity. Learn mentions retirement in one sentence only, so an exam item must rest on the general principles used here.")]),
"x2-d5-agent-versioning": ("Update, reconfigure, or replace agents without disrupting active workflows", [
    ("SG", "The bullet names updates that do not disrupt active work."),
    ("DOCS", "Docs define how agent profiles are versioned and which version an open pull request uses.")]),
# ---------------- D6
"x2-d6-hook-series": ("Block actions that violate defined security, compliance, or Responsible AI policies", [
    ("SG", "The bullet names blocking."),
    ("DG", "M6 unit 3 decision guidance: use enforceable hooks for blocking."),
    ("LIVE", LIVE + "hooks."),
    ("DOCS", "Docs state where each surface loads hook files from.")]),
"x2-d6-job-permissions": ("Scope permissions and execution contexts to enforce least-privilege access", [
    ("SG", "The bullet names least-privilege access."),
    ("CODE", "M6 unit 5 shows the workflow default and the job-level elevation in YAML."),
    ("LIVE", LIVE + "permissions blocks and the scope of `GITHUB_TOKEN`.")]),
"x2-d6-small-diff": ("Classify agent actions by operational, security, and compliance risk to right-size human interventions", [
    ("SG", "The bullet names the classification by risk."),
    ("DG", "M6 unit 2 has an Important box: these paths are high risk by default."),
    ("TRAP", "A one-line diff looks harmless.")]),
"x2-d6-human-judgment": ("Identify the subset of actions that require human judgment", [
    ("SG", "The bullet asks for the subset of actions."),
    ("DG", "M6 unit 4 tip: humans at merge, deploy and secret access.")]),
"x2-d6-self-review": ("Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes", [
    ("SG", "The bullet names explicit authorization."),
    ("DOCS", "Docs define **Prevent self-review** and state that one approval is enough."),
    ("REP", "Environments with required reviewers appear in M1, M2, M3, M4 and M6.")]),
# ---------------- case study
"c1": ("Configure agent planning to be distinct from agent execution", [
    ("DG", "M2 unit 4 has a list \"When to use each option\" and explicit decision guidance."),
    ("TRAP", "Plan-first sounds safer, so it is tempting to choose it everywhere.")]),
"c2": ("Configure an agent to output a structured plan", [
    ("SG", "The bullet names the structured plan."),
    ("DG", "M6 unit 2 decision guidance: use a machine-readable signal and enforce routing."),
    ("CODE", "The unit reads `risk` from `plan.json` in workflow YAML.")]),
"c3": ("Implement rollbacks", [
    ("SG", "\"Implement rollbacks\" is a named bullet."),
    ("DG", "M2 unit 7 calls this the rollback-safe pattern.")]),
"c4": ("Configure an agent to handle environment-specific constraints", [
    ("SG", "The audience profile of the study guide names \"Copilot setup steps\"."),
    ("DOCS", "The file path and the job name are fixed, which makes an exact drop-down item.")]),
"c5": ("Configure agent tool permissions", [
    ("CODE", "M3 unit 2 shows this frontmatter, with read-only permissions and `safe-outputs`."),
    ("DG", "M3 unit 4 lists the guardrails of agentic workflows."),
    ("LIVE", LIVE + "permissions blocks.")]),
"c6": ("Share agent state", [
    ("SG", "\"Share agent state\" is a named bullet."),
    ("DG", "M5 unit 4: avoid storing critical information only in prompts or chat history.")]),
"c7": ("Generate evaluation signals by using automated scanning tools", [
    ("SG", "The bullet names automated scanning tools."),
    ("DG", "M5 unit 5: treat security alerts or failed checks as blockers."),
    ("DOCS", "Docs name the ruleset rule and its thresholds.")]),
"c8": ("Identify failed, partial, or stalled agent executions", [
    ("SG", "The bullet uses the same three words as the failure modes."),
    ("DG", "M4 unit 7 defines each failure mode in one line.")]),
"c9": ("Configure multi-agent workflows to produce artifacts suitable for review and audit", [
    ("SG", "The bullet names artifacts for review and audit."),
    ("DG", "M4 unit 6 gives the naming conventions and the artifact upload."),
    ("CODE", "The unit shows `actions/upload-artifact` for an agent report.")]),
"c10": ("Assign autonomy levels to maximize delivery speed while remaining compliant with organizational security and Responsible AI standards", [
    ("SG", "The bullet names autonomy levels."),
    ("DG", "M6 unit 2 defines the levels and gives the rule about reversible failures.")]),
}

LABEL = {"SG": "Study guide", "TEST": "Learn says it is tested", "DG": "Emphasised in Learn", "REP": "Repeated across modules",
         "CODE": "Code in the unit", "LIVE": "Reported from the live exam", "DOCS": "Precise in GitHub Docs", "TRAP": "Classic trap"}


def why(qid, domain):
    skill, clues = WHY[qid]
    strong = any(k in ("TEST", "LIVE") for k, _ in clues) or sum(k in ("DG", "SG", "REP") for k, _ in clues) >= 2
    return {"skill": skill, "strength": "strong" if strong else "moderate",
            "clues": [{"kind": LABEL[k], "text": t} for k, t in clues]}
