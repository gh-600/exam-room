"""Lessons (Learn mode) for full exam 1: one lesson per concept that the exam tests, in the order of the Learn modules.
Every fact under "What GitHub Docs adds" was checked against the GitHub Docs source (or the gh-aw docs) while the exam was built."""
from lib import learn, DOCS

LESSONS = []


def N(nid, domain, skill, title, body, example=None, depth=None, watch=None, docs=()):
    mod, unit, _ = nid.split("-")
    n = {"id": nid, "module": mod, "unit": unit, "domain": domain, "skill": skill,
         "status": "confirmed" if depth else "learn-only", "title": title, "body": body.strip()}
    if example: n["example"] = example.strip()
    if depth: n["depth"] = depth.strip()
    if watch: n["watch"] = watch.strip()
    n["learn"] = learn(mod + unit)
    n["sources"] = [DOCS[d] for d in docs]
    LESSONS.append(n)


# ============================================================ M1
N("M1-U4-C1", "D1", "Plan and implement the degree of agent autonomy, including guardrails",
  "Each GitHub control enforces one thing, and only when it is turned on",
  """
GitHub is the **system of record** (issues, pull requests, commits, workflow runs and reviews are stored there) and the **control plane** (it has enforcement points that shape what an agent's contribution can do).

- **Pull requests**: changes are proposed before merging.
- **Required reviews**: an approval gate.
- **Required status checks**: CI evidence before merging.
- **CODEOWNERS**: review routing by path.
- **Rulesets and branch protection**: central branch policy.
- **Environments**: approvals for deployments and access to secrets.

The supervision model works everywhere, but enforcement requires each control to be configured.""",
  example="An agent opens a pull request that changes `/infra/`. CODEOWNERS requests the platform team, the required checks run, the ruleset blocks the merge until both are satisfied, and after the merge the deploy job waits in the `production` environment for a reviewer.",
  depth="A job that references an environment with required reviewers waits for an approval **before it starts**, and it can't read the environment's secrets until then.",
  watch="Options that attach a control to the wrong moment. CODEOWNERS routes reviews and doesn't block on its own. Environments gate jobs, not merges. A check gates a merge only when it is required.",
  docs=["control-deployments", "environments", "rules"])

N("M1-U4-C2", "D2", "Enable an agent to perform autonomous actions, including creating branches and pull requests",
  "Workflows wait for a person before they run on an agent's pull request",
  """
A workflow can read secrets and receive a token with write permissions. Code written by an agent is untrusted until someone has looked at it, so running workflows on it automatically would be a risk.

By default, the workflows on a pull request from Copilot cloud agent don't start. A user with write access reviews the changes and then selects **Approve and run workflows**. Learn calls this a built-in guardrail.""",
  example="Copilot opens a pull request and CI shows as waiting. You read the diff, paying attention to anything under `.github/workflows/`, and then approve the runs.",
  depth="The repository can be configured to let these workflows run automatically, which is a decision about risk. Only users with write access to the repository can trigger the cloud agent at all.",
  watch="Pushing another commit, or closing and reopening the pull request, doesn't start CI. A ruleset bypass has nothing to do with the approval of workflow runs.",
  docs=["agent-risks"])

N("M1-U5-C1", "D1", "Identify and mitigate common anti-patterns in agents",
  "A diff without a plan is planless execution: require a plan section",
  """
Humans stay accountable for what an agent does, so the system has to make the agent's work understandable. Learn lists four anti-patterns and the GitHub control that mitigates each one:

- **Planless execution** (a diff with no plan or rationale): require a plan section through a pull request template, and require review before merge.
- **Over-permissioned agents**: a least-privilege `GITHUB_TOKEN`, environments with required reviewers, and limits on who can trigger workflows.
- **Hidden reasoning** (only the diff is visible): require the plan, link the workflow runs, and record decisions in the pull request.
- **Blind trust in automation** ("CI passed, ship it"): combine checks with CODEOWNERS, required reviews and risk-based approvals.""",
  example="A file named `.github/pull_request_template.md` with a section `## Plan (required)` that asks for the goal, the scope, the steps, verifiable success criteria, the risks and a rollback plan.",
  watch="\"Add a second reviewer\" doesn't fix a missing plan: two people then look at the same unexplained diff.")

# ============================================================ M2
N("M2-U2-C1", "D1", "Identify steps for agents to perform",
  "Start agents in implementation and validation",
  """
An agent that acts like a general-purpose developer across the whole SDLC is hard to reason about, to limit and to audit. Map it to stages in which GitHub can enforce boundaries:

- **Planning**: issues, pull request descriptions.
- **Implementation**: branch, commits, pull request.
- **Validation**: workflow runs, checks, artifacts.
- **Deployment**: usually restricted, behind environments and approvals.

Most teams start with implementation and validation, where pull requests and workflows are natural control points. The boundary is: **agents propose; humans and policy accept.**""",
  example="A dependency remediation agent detects a vulnerable package, creates a branch, updates the dependency and the lock file, and opens a pull request with a plan and the expected success signals. Its responsibility ends there. Checks, reviews and policy do the rest.",
  watch="\"All stages\" and \"deployment\" are wrong as a first scope. Also remember the related guidance: treat workflow and infrastructure changes as higher risk than application code.")

N("M2-U3-C1", "D4", "Align evaluation criteria with development intent",
  "Success criteria state the real intent and are measured by system signals",
  """
Define every agent task with three parts: **inputs** (context, constraints, boundaries), **outputs** (plan, pull request, evidence) and **success criteria** (checks, scans, review outcomes). An under-specified task produces changes that look plausible and miss the goal.

\"CI passed\" is necessary but not always sufficient. Write the criterion for what you really want: \"the vulnerability is resolved\", not \"the tests passed\". And measure it with a signal from the system, never with the agent's own confidence.""",
  example="An agent updates a vulnerable package and all checks pass, but the vulnerable version is still reachable through a transitive dependency, so the alert stays open. With the criterion \"the alert is resolved\", the task isn't complete.",
  watch="Options that make the agent report on itself (a confidence level, a summary) or that add reviewers or retries. None of them changes what \"done\" means.")

N("M2-U4-C1", "D1", "Configure agent planning to be distinct from agent execution",
  "Plan-first validates intent before any code; plan + execution validates before merge",
  """
Both workflows end in a reviewed pull request. They differ in **when** a person validates the work.

**Plan-first**

1. A plan is generated (for example, by assigning the issue to the agent).
2. The agent opens a pull request that contains only the plan.
3. Reviewers discuss, refine and approve the plan.
4. The agent implements it in follow-up commits or a new pull request.

**Plan + execution**: one pull request holds the plan and the first commits. Required checks, CODEOWNERS and branch rules still prevent the merge.

Use plan-first for work that is high risk or hard to reverse (workflows, infrastructure, authentication, production). Use plan + execution when the change is low risk, reversible, and speed matters.""",
  example="A change to the authentication flow of a production service: plan-only pull request first. A fix to a typo in the documentation: plan and change together.",
  watch="\"Is it reviewed?\" doesn't separate the two, because both are. Look for wording such as \"before any code is generated\".")

N("M2-U4-C2", "D1", "Prevent agent action until the agent checked and approved",
  "Instructions are guidance; tool allowlists and gates are enforcement",
  """
An instruction such as \"do not edit files\" asks the model to behave. It can fail. A boundary removes the ability. Learn names four ways to enforce the line between planning and execution:

- **Capability boundary**: the planning agent has read-only tools only.
- **Explicit handoff** to an implementation agent after the plan is approved.
- **Tool gating** in an orchestrator: planning runs without tool execution, and tools are enabled after approval.
- **Plan mode**: the interface produces a plan and pauses before any change.""",
  example="A planner profile whose `tools` list holds only read and search tools, and an implementer profile that also has edit and execute tools. The planner can't change a file, whatever it decides.",
  depth="In a custom agent profile, `tools` is the allowlist. If the property is omitted, the agent gets **all** tools, and `tools: []` disables them all.",
  watch="Repeating the instruction, adding a template section, or asking reviewers to reject plans with code. The first two are guidance, and the third detects the problem after it happened.",
  docs=["custom-agents"])

N("M2-U5-C1", "D1", "Configure human intervention for autonomous agents without slowing delivery",
  "CODEOWNERS routes reviews; it blocks only when the ruleset requires code owner review",
  """
A CODEOWNERS file maps paths to owners, and GitHub requests those owners as reviewers when the paths change. That is routing. On its own it is advisory: if the rule says \"one approving review\", anyone's approval satisfies it.

To make the owners' approval a condition for merging, select **Require review from Code Owners** in the ruleset or branch protection rule.""",
  example="```text\n*                    @org/core\n/infra/              @org/platform\n/.github/workflows/  @org/platform\n```",
  depth="Order matters: the **last** matching pattern takes precedence. Put the general `*` line first and the specific paths after it. The example in the Learn module has `*` last, which would hand every file to the core team.",
  watch="\"Require two approvals\" (any two people) and \"add the owners as environment reviewers\" (that gates jobs, not merges).",
  docs=["codeowners", "rules"])

N("M2-U6-C1", "D1", "Plan and implement the degree of agent autonomy, including guardrails",
  "Match the control to the risk tier; critical work is gated at execution",
  """
Autonomy is designed per risk level, not applied the same way everywhere.

- **Low** (docs, formatting): merge can be automated after the required checks pass.
- **Medium** (`src/`, dependency bumps): pull request, checks and at least one review.
- **High** (`infra/`, `.github/workflows/`): CODEOWNERS, multiple reviews and stricter rulesets.
- **Critical** (production deployment settings, secrets): environment approvals. The agent prepares the change but can't execute it.

The first three tiers gate the **merge**. The critical tier gates the **execution**.""",
  example="```yaml\njobs:\n  deploy:\n    runs-on: ubuntu-latest\n    environment:\n      name: production\n    steps:\n      - run: ./deploy.sh\n```\n\nThe job pauses until a required reviewer of `production` approves it.",
  depth="Secrets stored in an environment are available only to jobs that reference the environment, and only after approval. An environment can list up to six reviewers, and one approval is enough.",
  watch="Choosing the control of the neighboring tier. Reviews and CODEOWNERS decide who approves a merge. They don't protect a secret or stop a deployment.",
  docs=["environments", "manage-environments"])

N("M2-U6-C2", "D1", "Configure an agent to be invoked in a CI workflow",
  "Data moves between jobs as outputs: step, then job, then needs",
  """
Treat data that another step or job consumes as an explicit output, not as something left in the logs.

1. A step writes `name=value` to the file in `$GITHUB_OUTPUT`. Later steps of the **same job** read `steps.<id>.outputs.<name>`.
2. The job publishes the value under `outputs:`.
3. Another job declares `needs: <job>` and reads `needs.<job>.outputs.<name>`.

Environment variables configure how a job runs. They aren't a channel between jobs.""",
  example="```yaml\njobs:\n  plan:\n    runs-on: ubuntu-latest\n    outputs:\n      risk: ${{ steps.read.outputs.risk }}\n    steps:\n      - id: read\n        run: echo \"risk=high\" >> \"$GITHUB_OUTPUT\"\n  apply:\n    needs: plan\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo \"Risk is ${{ needs.plan.outputs.risk }}\"\n```",
  depth="Outputs are strings, limited to 1 MB per job and 50 MB per run. An output that may contain a secret is skipped. The `needs` context holds only **direct** dependencies. For a file or a large plan, use an artifact.",
  watch="`steps.<id>.outputs` read from another job (empty), and `$GITHUB_ENV` (it only reaches later steps of the same job).",
  docs=["job-outputs", "syntax"])

N("M2-U6-C3", "D1", "Configure an agent to be invoked in a CI workflow",
  "Guard pull-request-only jobs with a job-level condition on the event",
  """
A workflow often has several triggers: `pull_request`, `push`, `workflow_dispatch`, `schedule`. A job that comments on a pull request or evaluates its changes fails when the run has no pull request.

Add a job-level condition on the event that triggered the run. The `github` context answers \"what triggered this run?\". The `vars` context holds configuration that is managed centrally, and `env` holds runtime variables.""",
  example="```yaml\non:\n  pull_request:\n    branches: [main]\n  workflow_dispatch:\n\njobs:\n  comment:\n    if: github.event_name == 'pull_request'\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo \"Validation complete\"\n```",
  depth="A job that is skipped by a condition reports **Success**. Don't put such a condition on a job that is a required status check unless a skip really should count as a pass.",
  watch="Conditions on `github.ref` (the branch), `vars.*` (configuration) or `github.actor` (who started it). None of them says which event triggered the run.",
  docs=["conditions"])

N("M2-U7-C1", "D1", "Configure agent to produce inspectable artifacts within standard development tooling",
  "Evidence is durable as an artifact and traceable when the run is linked",
  """
An agent system must leave a visible artifact for every meaningful action. The minimum observability set is:

- a structured plan (pull request description or discussion);
- a bounded pull request and commit history;
- links to the workflow runs of the required checks;
- uploaded artifacts such as logs and reports;
- review outcomes.

Logs scroll away, and an uploaded artifact stays with the run. Evidence should be traceable to **a specific workflow run and a specific commit**. Upload artifacts where they are produced and download them where they are reviewed or deployed, without committing generated files to the repository.""",
  example="```yaml\n- name: Upload test results\n  uses: actions/upload-artifact@v4\n  with:\n    name: test-results\n    path: results/\n```\n\nThen link the run and the artifact in an **Evidence** section of the pull request.",
  depth="By default, artifacts and logs are kept for 90 days and then deleted automatically.",
  watch="The agent's summary of the results (its own account, not evidence) and committing the report to the branch.",
  docs=["store-data", "retention"])

N("M2-U7-C2", "D2", "Configure an agent to handle environment-specific constraints",
  "The agent has its own secret boundary: MCP credentials are Agents secrets named COPILOT_MCP_…",
  """
Secrets don't belong in instructions files, committed configuration or workflow YAML. They are injected at run time through a protected boundary and passed only to the component that needs them.

Learn states the principle: the agent's runtime environment has its own secret boundary, so don't assume that it inherits the repository's CI secrets.

For Copilot cloud agent this is literal. The agent can't read secrets created for GitHub Actions, Codespaces or Dependabot. It has its own **Agents** secrets and variables.""",
  example="Create an Agents secret named `COPILOT_MCP_TRACKER_KEY` and reference it in the MCP configuration:\n\n```json\n\"headers\": { \"Authorization\": \"$COPILOT_MCP_TRACKER_KEY\" }\n```",
  depth="Only Agents secrets and variables whose names start with `COPILOT_MCP_` are available to the MCP configuration, referenced as `$COPILOT_MCP_NAME` or `${COPILOT_MCP_NAME}`.",
  watch="An Actions secret referenced from the MCP configuration, and an Agents secret without the prefix. Both fail.",
  docs=["mcp-config", "agent-secrets"])

N("M2-U7-C3", "D2", "Implement traceability and accountability for agent actions",
  "Hooks run at fixed points of execution; only a pre-execution hook can block",
  """
A hook runs a command at a defined point of the agent's execution, independently of the model's reasoning. That makes it an enforceable control and a source of audit data.

- **Pre-action** hooks validate or block an action before it runs: `preToolUse`.
- **Post-action** hooks log tool use and results: `postToolUse`.
- **Error** hooks capture failures and trigger escalation: `errorOccurred`.
- `sessionStart` runs when a session begins or is resumed.

Repository hooks are JSON files in `.github/hooks/`.""",
  example="A session log that ends like this shows a `preToolUse` hook that denied the tool call:\n\n```text\nError: Command blocked by policy\nReason: destructive_operation_detected\n[agent] Escalating to human review...\n```",
  depth="A `preToolUse` hook returns a `permissionDecision` of `allow`, `deny` or `ask`. In the cloud agent, `ask` is treated as `deny`, because nobody is there to answer. A hook that crashes or exits with a non-zero code denies the call (fail-closed), but a hook that times out lets it through (fail-open). The cloud agent runs hooks in a Linux sandbox, so `powershell` commands are ignored.",
  watch="`postToolUse` can't prevent anything, because the tool has already run. The firewall and rulesets don't judge commands. The JSON hook examples in the Learn modules are illustrative: the real format is in the hooks reference.",
  docs=["hooks", "hooks-ref"])

# ============================================================ M3
N("M3-U2-C1", "D2", "Configure an agent to be invoked in a CI workflow",
  "An agentic workflow runs from its compiled lock file",
  """
A GitHub Agentic Workflow is a Markdown file with two parts:

- **Frontmatter**: triggers, permissions, tools and safe outputs. It defines the boundaries.
- **Markdown instructions**: the intent, in natural language.

The file is compiled into a lock file, and the lock file is what GitHub Actions executes. The agent job has read-only permissions. Anything that writes (an issue, a comment, a pull request) is requested as a **safe output** and applied by a separate, gated step.""",
  example="You change `safe-outputs` so that created issues get a label. Run `gh aw compile`, then commit both the `.md` file and the regenerated `.lock.yml` file.",
  depth="Frontmatter is embedded at compile time, so every change to it needs a recompile. The Markdown body is loaded at run time, so an edit to the instructions takes effect on the next run.",
  watch="\"Commit the Markdown file\" after a frontmatter change, and \"grant write permission to the agent job\". The agent stays read-only by design.",
  docs=["gh-aw-faq", "gh-aw-how"])

N("M3-U3-C1", "D2", "Add an MCP server as a tool to an agent",
  "Cloud agent MCP configuration: mcpServers, a type, and a specific tools list",
  """
Three pieces work together: an **MCP server** exposes tools, a **registry** makes servers discoverable, and an **allow list** decides which servers are permitted.

For Copilot cloud agent, MCP servers are configured as JSON in the repository settings. The root is an `mcpServers` object keyed by server name. Each server needs:

- `type`: `http` or `sse` for a remote server, `local` or `stdio` for a local one;
- `tools`: the allowlist of tools that the agent may call;
- `url` for a remote server, or `command` and `args` for a local one.""",
  example="```json\n{\n  \"mcpServers\": {\n    \"tickets\": {\n      \"type\": \"http\",\n      \"url\": \"https://mcp.contoso.com/tickets\",\n      \"tools\": [\"get_ticket\", \"search_tickets\"]\n    }\n  }\n}\n```",
  depth="The agent uses configured tools autonomously and doesn't ask for approval first, so GitHub recommends listing specific read-only tools. `\"*\"` enables every tool of the server.",
  watch="`\"tools\": [\"*\"]` combined with an instruction not to write: that is guidance, not enforcement. And the root key: `servers` in the VS Code configuration, `mcpServers` for the cloud agent.",
  docs=["mcp-config"])

N("M3-U4-C1", "D2", "Configure an agent to handle environment-specific constraints",
  "The agent's firewall limits internet access; open one host with the custom allowlist",
  """
Execution context is what makes an agent safe: repository scope, branch isolation, workflow execution and permissions. Network isolation with allowlisted outbound access is one of the guardrails.

Copilot cloud agent has a firewall that is on by default. A recommended allowlist lets it reach common package registries. Anything else is blocked, and a blocked request appears as a warning in the pull request, with the address and the command that made it.""",
  example="The agent can't restore packages from the private feed `nuget.contoso.com`. Add that host to the custom allowlist of the firewall and start a new session.",
  depth="A change to the allowlist applies to new sessions only. The firewall covers processes that the agent starts through its Bash tool. It doesn't apply directly to the MCP servers that you configure, so it isn't a complete security boundary.",
  watch="Disabling the firewall (every host becomes reachable), and putting the URL in the instructions or in a secret (neither opens the firewall).",
  docs=["firewall"])

N("M3-U5-C1", "D2", "Evaluate the execution context for an agent",
  "The cloud agent works inside built-in limits",
  """
Copilot cloud agent acts in the repository, but inside limits that the platform sets:

- It makes its changes on a **separate branch**, never directly on the default branch.
- It doesn't finalize anything: a person reviews the result and decides whether it is merged.
- Its work runs in a GitHub Actions-powered environment, so repository and organization settings control which workflows and actions run and what the `GITHUB_TOKEN` may do.
- The session is visible while it runs: you can follow the log and steer the agent.""",
  example="You assign an issue to Copilot. It pushes to a `copilot/` branch and opens a draft pull request. You asked for the work, so your approval doesn't count: a colleague has to review and approve it.",
  depth="The agent can't approve or merge a pull request, and the user who asked it to create the pull request can't approve it. Its pull requests are subject to the branch protections and required checks of the repository.",
  watch="\"The requester approves\" and \"the agent merges after the checks pass\". Also, \"only the current repository\" holds for sessions on GitHub Actions. Docs say that sessions in a cloud sandbox can work across repositories.",
  docs=["agent-risks", "copilot-on-github"])

N("M3-U5-C2", "D2", "Configure an agent to handle environment-specific constraints",
  "Prepare the agent's environment with copilot-setup-steps",
  """
Copilot cloud agent works in an ephemeral environment that is powered by GitHub Actions. If it has to discover and install its own tools in every session, it is slow and sometimes fails.

Install tools and dependencies deterministically, before the agent starts, with a workflow file at a fixed path that contains one job with a fixed name.""",
  example="```yaml\n# .github/workflows/copilot-setup-steps.yml\non:\n  workflow_dispatch:\n\njobs:\n  copilot-setup-steps:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-dotnet@v4\n        with:\n          dotnet-version: '9.0.x'\n      - run: dotnet restore\n```",
  depth="The file must be `.github/workflows/copilot-setup-steps.yml`, the job must be named `copilot-setup-steps`, and the file takes effect only when it is on the default branch.",
  watch="Installation commands in the instructions file (the agent still installs by trial and error), a `preToolUse` hook, or a separate CI workflow with a cache. None of them prepares the agent's environment.",
  docs=["agent-env"])

N("M3-U5-C3", "D2", "Configure agent tool permissions",
  "Events caused by GITHUB_TOKEN don't start new workflow runs",
  """
Most actions performed with the repository's `GITHUB_TOKEN` don't trigger further workflow runs. This protects against loops, where a workflow keeps triggering itself.

When one workflow must start another on purpose, use a different credential, such as an installation access token of a GitHub App or a personal access token, and design the automation so that it can't recurse.""",
  example="A scheduled agent workflow commits documentation with `GITHUB_TOKEN`. The workflow that publishes on `push` never starts. Pushing with a GitHub App token creates the `push` event, without a long-lived personal credential.",
  depth="`workflow_dispatch` and `repository_dispatch` are exceptions: events created with `GITHUB_TOKEN` do start those runs. The token is scoped to the repository, and when a `permissions` block names any scope, every scope that isn't named is set to `none`.",
  watch="\"Grant `contents: write`\": the token can already push, and the limit is on triggering. A personal access token works, but it is a long-lived personal credential.",
  docs=["trigger", "github-token"])

# ============================================================ M4
N("M4-U3-C1", "D5", "Apply an orchestration pattern to coordinate multiple agents",
  "Fan-out/fan-in: independent jobs run in parallel, and needs with a list joins them",
  """
Express orchestration through workflows and events, so that coordination is visible in runs, checks and logs.

- **Fan-out**: jobs that don't depend on each other start in parallel.
- **Fan-in**: a job with `needs: [job_a, job_b]` waits until both are complete.

The Learn module says about this pattern: \"This pattern is tested in the exam.\" A `concurrency` group on the joining job keeps two of them from running at the same time for one branch.""",
  example="```yaml\njobs:\n  spec_analyzer:\n    runs-on: ubuntu-latest\n    steps:\n      - run: ./executors/spec_analyzer.sh\n  risk_reviewer:\n    runs-on: ubuntu-latest\n    steps:\n      - run: ./executors/risk_reviewer.sh\n  plan_merger:\n    runs-on: ubuntu-latest\n    needs: [spec_analyzer, risk_reviewer]\n    concurrency:\n      group: multiagent-${{ github.ref }}\n    steps:\n      - run: ./executors/plan_merger.sh\n```",
  depth="If a job fails or is skipped, every job that needs it is skipped too, unless that job has a condition that lets it continue.",
  watch="`uses` (calls a reusable workflow), `with` (inputs) and `strategy` (variations of one job) in the place of `needs`.",
  docs=["syntax", "concurrency"])

N("M4-U3-C2", "D5", "Apply an orchestration pattern to coordinate multiple agents",
  "Run one workflow after another with workflow_run",
  """
Some work must happen in strict order: the dependency agent opens a pull request, CI validates it, a security validation runs after CI, a person approves, and only then the merge happens.

Between two separate workflows, the second one declares the order. It names the first workflow in a `workflow_run` trigger and reacts to its `completed` activity type. The first workflow doesn't change.""",
  example="```yaml\nname: Security Validation\non:\n  workflow_run:\n    workflows: [CI Validation]\n    types: [completed]\n```",
  depth="The run starts whatever the result of the first workflow was, so test `github.event.workflow_run.conclusion` when it must run only after success. The workflow file must be on the default branch, and chains are limited to three levels.",
  watch="`workflow_call` (the first workflow would have to call the second), `workflow_dispatch` (manual or through the API) and `pull_request` (both workflows would start together).",
  docs=["events"])

N("M4-U3-C3", "D5", "Apply an orchestration pattern to coordinate multiple agents",
  "Parallel agents need isolated scopes; dependent work runs in sequence",
  """
A multi-agent system starts with clear responsibilities: a narrow role for each agent, a scope limited by path and by type of artifact, and completion signals that checks can verify.

- **Parallel** orchestration fits when scope boundaries prevent overlap. If agents can collide on the same files, parallelism adds instability, not throughput.
- **Sequential** orchestration fits when one agent's output is another's input.

Agents coordinate through shared, reviewable artifacts (a plan, a report, a pull request), not through direct agent-to-agent messages.""",
  example="A dependency agent may change package references and lock files. A documentation agent may change `/docs/`. They run at the same time, each on its own branch, and their results meet in pull request checks and reviews.",
  watch="\"One shared branch to reduce the number of pull requests\" and \"one general-purpose agent that can change any path\".")

N("M4-U4-C1", "D5", "Configure agent isolation for parallel execution",
  "A concurrency group belongs to the repository: name it by workflow and ref",
  """
When agents push often, runs of the same workflow overlap. A concurrency group lets only one of them proceed.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

The group name isolates runs per workflow and per branch. `cancel-in-progress: true` cancels the earlier run, so only the newest one continues.""",
  example="Two workflows both use `group: ${{ github.ref }}`. On every push, the run of one cancels the run of the other, because for GitHub they are in the same group.",
  depth="Group names must be unique across workflows, or runs of different workflows cancel or queue behind each other. Without `cancel-in-progress`, one run is in progress and at most one is pending: a newer run replaces the pending one. Docs describe job-level `concurrency` as acting across runs too, which contradicts a sentence in the Learn unit.",
  watch="`strategy.matrix` (parallel jobs inside one run, nothing to do with overlapping runs) and `${{ github.run_id }}` (unique, so nothing is ever canceled).",
  docs=["concurrency"])

N("M4-U4-C2", "D5", "Configure agent isolation for parallel execution",
  "Isolate agents by branch, by workflow, and by permissions",
  """
Execution isolation means that each agent works in its own controlled scope, so that concurrency is safe and attribution is clear.

- **Branch**: one branch per agent and task, such as `agent/dependency/<ticket>`.
- **Workflow**: a dedicated workflow, or a dedicated job with its own permissions.
- **Permissions**: the minimum that the workflow needs.
- **Concurrency**: for runs that overlap in time.

When agents share a branch or a workflow context, commits interleave, ownership is ambiguous and failures repeat. Rollback and auditing become much harder.""",
  example="Three agents, three branches: `agent/dependency/123`, `agent/refactor/124`, `agent/security/125`. Each pull request shows one agent's intent and scope.",
  watch="A matrix presented as isolation between runs, and a shared branch presented as easier to audit.")

N("M4-U5-C1", "D5", "Detect and resolve agent conflicts, including overlapping code changes, duplicated effort, and contradictory outputs",
  "Name the conflict type, then make its detection a required check",
  """
Isolation reduces conflicts but doesn't remove them. There are four types:

- **Textual merge conflict**: the same files or lines changed.
- **Semantic conflict**: the merge is clean and the combined behavior is broken.
- **Policy conflict**: protected areas need different reviews or approvals.
- **Duplicate effort**: two pull requests solve the same problem differently.

Detect early with a merge validation step, and make it a **required check** so that it doesn't depend on a reviewer noticing. Route sensitive paths with CODEOWNERS. Escalate to a person when a pull request conflicts twice after rebasing, when the same check fails twice with the same signature, or when two agents propose incompatible fixes.""",
  example="```yaml\n- name: Validate merge with main\n  run: |\n    git fetch origin main\n    git merge --no-commit origin/main\n```",
  depth="A required status check can be strict: with **Require branches to be up to date before merging**, the branch must contain the latest base branch before it merges, which is how the checks get to test the combined result.",
  watch="A clean merge with a broken build is a semantic conflict, and only checks catch it. CODEOWNERS routes reviews and detects nothing.",
  docs=["rules"])

N("M4-U6-C1", "D5", "Perform post-hoc analysis of multi-agent behavior",
  "A missing artifact is traced in the organization audit log",
  """
Observability means that every meaningful step leaves a durable trace in GitHub: a pull request that states intent, checks and runs that produce evidence, artifacts and logs that explain outcomes, and clear attribution (titles such as `[agent: dependency] …`, labels, owners).

For analysis after the fact, artifacts are the primary evidence: open the run and download them from the **Artifacts** section of the summary.

When an artifact is unexpectedly missing, search the organization audit log for `action:artifact.destroy`. The event shows who deleted it, when, and in which repository.""",
  example="The `agent-report` artifact is gone from a run that finished two days ago. With the default retention it can't have expired, so someone deleted it. The audit log names the actor.",
  depth="The audit log describes `artifact.destroy` as a workflow run artifact that was manually deleted. A deleted artifact can't be restored.",
  watch="Re-running the workflow (that creates a new artifact), the pull request timeline (no artifact events), and `gh agent-task view --log --follow` (the live log of an agent session).",
  docs=["audit-log", "remove-artifacts"])

N("M4-U7-C1", "D5", "Update, reconfigure, or replace agents without disrupting active workflows",
  "Two frontmatter settings decide who can start a custom agent",
  """
In the profile of a custom agent, two properties control invocation:

- `disable-model-invocation: true`: the agent can't be invoked as a subagent, which breaks an orchestration that depends on it.
- `user-invocable: false`: users can't select the agent directly.

A parent agent lists the subagents that it may orchestrate in `agents`, and `handoffs` describe the transitions between agents.""",
  example="An implementer that only the planner should start:\n\n```yaml\n---\nname: implementer\ndisable-model-invocation: false\nuser-invocable: false\n---\n```",
  depth="Docs describe `user-invocable: false` as \"can only be accessed programmatically\", and `disable-model-invocation: true` as \"must be manually selected\". The older `infer` property is retired in favor of these two. `handoffs` is a VS Code feature and is ignored by the cloud agent on GitHub.com.",
  watch="The two names sound alike. One is about other agents calling this agent. The other is about people selecting it.",
  docs=["custom-agents"])

N("M4-U7-C2", "D5", "Respond to degraded behavior or coordination across agents",
  "When a rule blocks the agent's branch, add Copilot as a bypass actor on that ruleset",
  """
Multi-agent failures are often coordination failures: partial execution, stalled workflows, conflicting outputs, and flapping. Design for them with bounded retries, an escalation threshold and small pull requests that are easy to revert.

One stall has a specific fix. A repository rule can reject the agent's pushes to its own branch (Learn's example is a rule that requires signed commits). You can add Copilot as a **bypass actor** on that ruleset: the agent can work, and the rule still binds everyone else.""",
  example="Ruleset RS1 targets all branches, and one of its rules rejects the agent's commits. Add Copilot to the bypass list of RS1. Don't disable RS1 and don't narrow its target.",
  depth="Docs confirm it: a ruleset or branch protection rule can prevent Copilot from creating or updating pull requests, and repository administrators can configure a ruleset bypass for Copilot. A bypass list belongs to one ruleset, so other rulesets still apply to the agent.",
  watch="In most questions a bypass list is the wrong answer. Here the constraint (\"the ruleset must keep applying to everyone else\") makes the narrow bypass the right one. Read the constraint.",
  docs=["copilot-on-github", "ruleset-bypass"])

# ============================================================ M5
N("M5-U2-C1", "D3", "Choose between short-term, long-term, and external memory",
  "Memory is a fact the agent may use; a rule that must always apply goes in instructions",
  """
Agent memory has three layers:

- **Short-term**: the working context of the current task. It isn't preserved across sessions.
- **Long-term**: curated knowledge that is reused across tasks.
- **External**: durable artifacts outside the agent, such as issues, pull requests, documentation and workflow outputs. This is the source of truth.

Choose the place by the kind of information: requirements, plans and decisions go in issues and pull requests, and **repeatable processes go in instructions or reusable skills**. Store only what affects the outcome of the task.""",
  example="Copilot Memory holds the fact \"format the code with `dotnet format` before each commit\", yet some sessions skip it. Put the rule in the repository's custom instructions, which are given to the agent every time.",
  depth="Copilot Memory stores repository-level facts and user-level preferences. Before it uses a repository-level fact, Copilot checks the fact's citations against the current branch. That is a judgment, not a guarantee. Facts expire after 90 days by default, and owners can set 7 to 180 days. Older guides say 28 days.",
  watch="Treating a memory as enforcement, and \"increase the expiry period\": expiry decides how long a fact is kept, not whether it is applied.",
  docs=["memory"])

N("M5-U3-C1", "D3", "Resume agent work without repeating steps or diverging from prior decisions",
  "To resume, re-anchor to the pull request",
  """
State isn't kept in the session. It is spread over GitHub artifacts: the issue holds the requirements, the pull request is the **state anchor** (description, plan, updates), commits show progress and workflow runs hold the validation results.

To resume without repeating work:

1. Open the existing pull request.
2. Review the description and the linked issue.
3. Check the commits already made.
4. Review the results in the **Checks** tab.
5. Continue from the latest state.""",
  example="A session ends halfway through a task. The next session reads pull request #42, sees that the validation is committed and that one check fails, and continues with that failure instead of starting again.",
  depth="On GitHub, Copilot remembers context from earlier sessions on the same pull request, and you ask for further changes by mentioning `@copilot` in a comment on the pull request.",
  watch="A new branch from `main` (repeats the work), pasted chat history (session context, not state), and closing and recreating the pull request (that is a reset, for when requirements change).",
  docs=["use-agent"])

N("M5-U3-C2", "D3", "Detect and correct drift during extended agent execution",
  "Drift is corrected against the source of truth",
  """
**Context drift** occurs when the agent's actions no longer align with the original goal or with earlier decisions.

Detect it by checking:

- whether the changes satisfy the acceptance criteria;
- whether commits contradict earlier decisions;
- whether checks are failing or missing.

Correct it by re-aligning the agent with the source of truth: re-read the issue and the pull request description, compare the changes with the acceptance criteria, update the description if a decision really changed, and re-run the workflows.""",
  example="The issue asks for input validation on one endpoint. The pull request now also refactors logging. Move the refactoring out, and bring the commits back in line with the recorded design decision.",
  watch="Changing the acceptance criteria to fit the drift, continuing from the agent's own summary (it carries the drift forward), and merging now to clean up later. Drift isn't a reset: in a reset, the requirements themselves changed.")

N("M5-U3-C3", "D3", "Define memory expiration, pruning, and reset rules",
  "Artifacts and logs expire: 90 days by default",
  """
Memory has to be maintained, or it becomes stale. Learn names four practices:

- **Expiration**: some memory is kept for a limited time only, such as workflow logs and artifacts.
- **Pruning**: remove artifacts and runs that are no longer needed.
- **Summarization**: reduce detailed history to final decisions and links.
- **Reset**: start from a new plan when the requirements change.""",
  example="An auditor wants test reports kept for 180 days in a private repository. Change the repository's artifact and log retention period to 180 days. It applies to artifacts created from then on.",
  depth="The default is 90 days. A public repository allows 1 to 90 days, and a private one 1 to 400 days. A new period isn't retroactive. `retention-days` on an upload step can't exceed the repository's limit. A deleted artifact can't be restored.",
  watch="\"Artifacts are kept until someone deletes them\", \"make the repository public and set 180\", and `retention-days: 180` while the repository limit is still 90.",
  docs=["retention", "store-data", "remove-artifacts"])

N("M5-U3-C4", "D3", "Define memory expiration, pruning, and reset rules",
  "When the requirements change, reset the recorded plan",
  """
Some memory must be reset so that it isn't carried over wrongly. Reset when:

- the requirements in the issue change significantly;
- a new implementation approach is chosen;
- earlier assumptions are no longer valid.

In practice: update or rewrite the pull request description, close and recreate the pull request if needed, and document the new direction **before** the agent continues.""",
  example="The issue asked for a caching layer. The product owner now wants fewer database queries instead. Rewrite the pull request description with the new approach before the agent writes another commit.",
  watch="Putting the new requirement only in the next prompt: the pull request still describes the old plan, so the agent has two conflicting sources. Deleting artifacts is pruning, and adding a summary is summarization. Neither replaces the plan.")

N("M5-U4-C1", "D3", "Prevent conflicting context",
  "One source of truth for each type of information",
  """
An agent may start in an IDE, continue in the CLI and finish in a GitHub-hosted environment. Continuity comes from durable artifacts, not from session context. Give each type of information one place:

- **Requirements** live in issues.
- **Decisions and progress** live in pull requests.
- **Validation rules** live in repository instructions.
- **Execution results** live in workflow runs and artifacts.

Don't keep critical information only in prompts or chat history. Write important updates to the issue or the pull request.""",
  example="A reviewer changes a timeout requirement. The change goes into the issue, not into a chat message, so every tool and every later session reads the same value.",
  watch="Requirements can be restated in a pull request description, but before work starts only the issue exists. \"Where do the rules for every task go?\" is repository instructions, not an issue.")

N("M5-U4-C2", "D3", "Prevent stale context",
  "Share references, not copies: conflicting context and stale context",
  """
Share state with **durable references**: the pull request number, the branch name, commit SHAs, links to workflow runs. Every tool can resolve them against the same repository data, so no session context has to be transferred.

- **Conflicting context**: the same information exists in several places with different values. Prevent it with a single source, and update the original instead of creating copies.
- **Stale context**: outdated information is used. It happens when the pull request is behind its base branch, when workflow results no longer reflect the code, or when requirements changed without being updated.""",
  example="The agent works in the IDE, then the CLI, then the cloud. All three refer to pull request #42 and read its latest commits and runs before changing anything.",
  depth="A strict required status check (**Require branches to be up to date before merging**) enforces part of this: the branch must contain the latest base branch before it can merge.",
  watch="Restating the acceptance criteria in each tool's prompt \"to be safe\". Those copies are exactly what creates conflicting context.",
  docs=["rules"])

N("M5-U5-C1", "D4", "Identify qualitative and quantitative evaluation signals to evaluate agents",
  "Evaluation starts from criteria in the issue; no single signal proves completeness",
  """
Evaluation begins with success criteria that are written in the issue and referenced in the pull request. They let both the agent and the reviewer verify completion.

The pull request is where the signals arrive: status checks, workflow runs, the **Checks** tab and review outcomes. The typical flow is: the issue defines the task, the agent opens a pull request, workflows run, the required checks must pass, a reviewer approves, and the merge happens.

A check validates only what it was designed to detect. A passing build doesn't mean that the change is complete, appropriate or low risk.""",
  example="The build is green and the tests pass, but the acceptance criterion \"the export also works for empty orders\" has no test. The reviewer uses the criteria in the issue to see the gap.",
  watch="\"A passing build proves that the change is complete and low risk.\" That is the anti-pattern called blind trust in automation.")

N("M5-U5-C2", "D4", "Specify expected outcomes and operational constraints for agent tasks",
  "A check gates a merge only when it is a required status check",
  """
A workflow that runs on a pull request reports information. Nothing stops the merge when it fails, unless the check is **required**.

- In a ruleset: add the rule that requires status checks to pass, and name the check.
- In a branch protection rule: select **Require status checks to pass before merging**, and select the check.

Required reviews are a different gate. They require a person's approval, not a test result.""",
  example="`ci.yml` reports a check named `test` on every pull request. An active ruleset that targets `main` and requires `test` blocks the merge of any pull request, from a person or an agent, until `test` passes.",
  depth="A ruleset is enforced only when its status is Active. Nobody bypasses a ruleset unless they are on its bypass list. You can also name the app that is expected to report a check.",
  watch="\"Require one approving review\": a reviewer can approve while the tests fail. And an instruction to the agent to run the tests is guidance, not a gate.",
  docs=["rules", "branch-protection", "ruleset-bypass"])

N("M5-U5-C3", "D4", "Identify failures by using logs, plans, traces, outputs, and workflow artifacts",
  "A skipped job passes a required check; a skipped workflow leaves it pending",
  """
A required check protects a branch only if it really runs. Two cases look alike and behave in opposite ways:

- A **job** that is skipped by an `if` condition reports **Success**. The required check is satisfied, and nothing was tested.
- A **workflow** that is skipped entirely (by a path filter, a branch filter or a commit message) leaves its checks **Pending**. A pending required check blocks the merge.

This is why \"checks are failing or missing\" is one of the signs to look for when work drifts.""",
  example="```yaml\nintegration-tests:\n  if: contains(github.event.pull_request.labels.*.name, 'run-integration')\n```\n\nA pull request without the label skips the job, the required check passes, and the pull request can merge untested.",
  depth="Docs say it directly: a skipped job reports its status as Success and doesn't prevent a pull request from merging, even if it is a required check.",
  watch="\"A check that is never reported counts as passed.\" It doesn't: it stays pending and blocks.",
  docs=["conditions", "status-checks"])

N("M5-U5-C4", "D4", "Generate evaluation signals by using automated scanning tools",
  "Each security signal answers a different question",
  """
Security is part of evaluation, and a failed security check is a blocker. Know which tool answers which question:

- **Code scanning**: does the code contain a vulnerability?
- **Dependency review**: does this pull request add or change a dependency that has a known vulnerability?
- **Secret scanning**: has a credential been committed?
- **Push protection**: stop a supported secret before it is committed.""",
  example="An agent updates a package to a version with a known vulnerability. A dependency review check flags it in the pull request, before the merge.",
  depth="The dependency review action surfaces known vulnerabilities in the dependency changes of a pull request, so that vulnerable dependencies are caught before they are merged.",
  watch="Push protection offered for a dependency problem (it is about secrets), and an environment with reviewers (it gates a job, it doesn't inspect a pull request).",
  docs=["protect-threats", "dependency-review"])

N("M5-U6-C1", "D4", "Classify root causes, including reasoning errors, tool misuse, and context or environment issues",
  "Classify the root cause, then fix the matching lever",
  """
To analyze a failure, compare **intent** (the issue and the pull request description) with **results** (commits, workflow outputs and logs). Then classify the cause, because each class has its own fix:

- **Reasoning error**: requirements misread, wrong logic, acceptance criteria ignored. Fix the **prompts and instructions**.
- **Tool misuse**: a misconfigured workflow, a wrong command, a workflow that wasn't triggered. Fix the **tool configuration**: workflow files, triggers, permissions, required checks.
- **Context issue**: an outdated pull request state, missing decisions, conflicting information. Fix **memory and state**: update the issue or pull request, remove stale context, keep one source of truth.""",
  example="No failed checks appear on agent pull requests that later break the build. The criteria are clear and the plans match them. The validation workflow triggers only on `push` to `main`: tool misuse. Add a `pull_request` trigger.",
  watch="Blaming the agent's reasoning when the evidence points to a workflow, and \"add the command to the instructions\" when what is missing is a check on the pull request.")

N("M5-U6-C2", "D4", "Revise instructions, workflows, or constraints",
  "Improve behavior in a loop: observe, find the cause, fix, and re-run",
  """
Improving an agent is iterative:

1. Run the agent on a task.
2. Observe the failures in logs and artifacts.
3. Identify the root cause.
4. Apply a fix to the prompts, the memory or the tools.
5. Re-run the workflow.

Keep every adjustment traceable: document it in the pull request, reference the commits and runs, and keep changes small enough to review.""",
  example="After three failed tasks you find that the agent used a stale timeout value from an old comment. You remove the comment, keep the value in the issue only, and run the task again to confirm.",
  watch="Removing the failing check from the required checks, or giving the token write access to everything. Both hide the failure and leave the behavior as it was.")

# ============================================================ M6
N("M6-U2-C1", "D6", "Assign autonomy levels to maximize delivery speed while remaining compliant with organizational security and Responsible AI standards",
  "Four autonomy levels, raised in phases as the agent proves reliable",
  """
Risk-based autonomy gives an agent boundaries that match the impact and reversibility of its actions.

- **Read-only**: inspect, summarize, classify, recommend. Nothing is modified.
- **Propose-only**: create branches and pull requests. No merge, no deployment.
- **Execute with guardrails**: run pre-approved workflows (tests, builds, staging deployments) within limits.
- **Human-authorized execution**: high-impact actions only after a person approves.

Teams usually tighten first and relax in phases: (1) open pull requests only, (2) merge low-risk pull requests after checks, (3) deploy to staging automatically, (4) deploy to production only through an environment approval.""",
  example="A triage agent that labels issues is read-only. A coding agent that opens pull requests is propose-only. An agent that deploys to production after a release manager approves is human-authorized execution.",
  watch="Autonomy isn't one setting: it is a combination of pull request rules, environments, workflow permissions and tool access. No phase of progressive autonomy removes pull requests or required checks.")

N("M6-U2-C2", "D6", "Classify agent actions by operational, security, and compliance risk to right-size human interventions",
  "Route execution by a machine-readable risk signal",
  """
When an agent's plan carries a risk rating, the rating should decide what the system does, not a person's reading of a description. Learn's guidance: \"Don't rely on narrative explanations of risk. Use a machine-readable signal and enforce routing.\"

- Low risk: applied automatically.
- Medium risk: validated through pull requests and checks.
- High risk: explicit human approval.

In a workflow, a job reads the rating from the plan and exposes it as an output. An `if` on each following job selects the path, and `environment` adds the approval to the path that needs it.""",
  example="```yaml\napply:\n  needs: plan\n  environment: approval-required\n  if: ${{ needs.plan.outputs.risk != 'low' }}\napply_auto:\n  needs: plan\n  if: ${{ needs.plan.outputs.risk == 'low' }}\n```",
  depth="A job that references an environment with required reviewers waits for an approval before it starts. Outputs are strings, which is why the comparison is with `'low'` in quotes.",
  watch="`concurrency` or `permissions` where `environment` belongs, and the two comparisons swapped.",
  docs=["control-deployments", "job-outputs"])

N("M6-U2-C3", "D6", "Scope permissions and execution contexts to enforce least-privilege access",
  "Scope a terminal agent with allow and deny tool options",
  """
For a terminal-based agent such as Copilot CLI, tool access is the main governance boundary. Read-only actions can be allowed by default. Writing files, running commands and privileged actions stay gated unless the task needs them.

The rule is to match tool access to consequence: a low-risk task shouldn't inherit high-risk capabilities.""",
  example="```bash\ncopilot -p \"Summarize the last 10 commits.\" --allow-tool='shell(git)' --deny-tool='shell(git push)'\n```\n\n`git` commands run without a prompt, `git push` is blocked, and every other tool still needs approval.",
  depth="`--deny-tool` takes precedence over `--allow-tool` and `--allow-all-tools`. For `git` and `gh`, a rule can name a first-level subcommand, as in `shell(git push)`.",
  watch="`--allow-all-tools` and `--allow-tool='shell'` (every shell command). The command `copilot agent run … --allow-tool 'read,search'` in the Learn module is illustrative, not real syntax.",
  docs=["copilot-cli"])

N("M6-U3-C1", "D6", "Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes",
  "A production gate is an environment with required reviewers plus environment secrets",
  """
Governance is enforced with controls, not with trust: rulesets, required checks, CODEOWNERS, environments and guardrail workflows. For deployments, the control is the **environment**:

- require reviewers for production deployments;
- keep production secrets in the production environment only;
- keep a record of deployments and approvals.

Learn's guidance: if a workflow accesses production secrets, treat it as critical risk and gate it.""",
  example="Move the Azure credentials from repository secrets to the secrets of an environment named `production`, add the release managers as required reviewers, and reference the environment in the deploy job.",
  depth="Environment secrets reach only the jobs that reference the environment, and only after approval. Up to six reviewers can be listed, and one approval is enough. A workflow that references an environment that doesn't exist creates it, without any protection, so a misspelled name is a hole.",
  watch="CODEOWNERS on `deploy.yml` (reviews changes to the file, not each deployment), more approvals on the merge, and renamed secrets. Also, `cancel-in-progress: true` on a production group cancels a deployment that is already running.",
  docs=["environments", "manage-environments"])

N("M6-U4-C1", "D6", "Identify the subset of actions that require human judgment",
  "People at decision points; enforcement by the platform",
  """
Human-in-the-loop design puts people where their judgment matters and automates the rest.

- **Decision points**: merge, deployment, access to secrets.
- **Not at every step**: analysis, formatting and routine checks run without approval.

Enforcement must be technical. \"Controls in docs only\" is an anti-pattern: what the platform can't enforce will be bypassed. Use hooks that block; logging and banners help, but they don't prevent execution. Think in layers: constraints before the action (permissions), validation during it (checks), traceability after it (logs and artifacts).""",
  example="A `preToolUse` hook denies `terraform destroy`. A banner that warns about destructive commands would only inform the agent, and the command would still run.",
  watch="\"Require approval at every step\" sounds safe. It causes governance fatigue, and tired reviewers stop reviewing.")

N("M6-U5-C1", "D6", "Scope permissions and execution contexts to enforce least-privilege access",
  "Declare permissions on the job that needs them; OIDC needs id-token: write",
  """
Permissions are the real boundary of what an agent can do, whatever its instructions say. Broad tokens turn small mistakes into incidents.

- Set a read-only default at the workflow level.
- Elevate only the job that must write.
- Treat `pull-requests: write` as an elevated capability.
- Restrict secrets with environments, keep high-risk jobs apart, and pin third-party actions.""",
  example="```yaml\njobs:\n  deploy:\n    runs-on: ubuntu-latest\n    environment: production\n    permissions:\n      contents: read\n      id-token: write\n    steps:\n      - uses: azure/login@v2\n        with:\n          client-id: ${{ secrets.AZURE_CLIENT_ID }}\n          tenant-id: ${{ secrets.AZURE_TENANT_ID }}\n          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}\n```",
  depth="When a `permissions` block names any scope, every scope that isn't named is set to `none`. `id-token: write` lets the job request an OpenID Connect token, so no client secret has to be stored. It gives no write access to any resource.",
  watch="`write-all`, and removing the `permissions` key (the job then gets the repository's default, which may be read and write).",
  docs=["syntax", "oidc-azure", "oidc"])

N("M6-U7-C1", "D6", "Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes",
  "Retry transient failures, investigate security failures, escalate repeated ones",
  """
Recovery depends on the kind of failure:

- **Transient** (a network error): retry, within a limit.
- **Repeated**: when the same required check fails twice, stop the automated iteration and escalate to a person, with what failed, what was tried, the evidence and a suggested next step.
- **Security**: investigate. Don't retry until it passes.
- **High-risk changes**: keep them small, so that a revert is quick.

Governance also drifts: checks get renamed, reviews relaxed, permissions widened. Review it on a cadence: failed runs weekly, permissions and secret scopes monthly, rulesets, CODEOWNERS and environment reviewers quarterly.""",
  example="A code scanning check fails three times with the same alert while the agent rearranges the code. Automated iteration stops and a person investigates the finding.",
  watch="\"Retry until the limit is reached\", \"remove the check for agent pull requests\" and \"the agent dismisses the alert as a false positive\".")

N("M6-U7-C2", "D6", "Preserve execution velocity by minimizing approvals that do not materially reduce risk",
  "Rubber-stamping is fixed by making review easier, not by adding approvals",
  """
Learn lists governance failure patterns and their mitigations:

- **Unbounded autonomy** (no approval for production): environments, required reviewers, rulesets.
- **Excess permissions**: least privilege, environment scoping, job-level permissions.
- **Missing audit trail**: artifact uploads and evidence-first workflows.
- **Bypass paths** (direct push, disabled checks): rulesets and restricted pushes.
- **Rubber-stamping** (approvals become a click to unblock): better evidence, CODEOWNERS, smaller pull requests.

To avoid governance fatigue: require evidence so that review is fast, route reviews so that reviewers have context, keep pull requests small, and ask for a rollback plan on high-impact changes.""",
  example="Reviewers approve 60 large agent pull requests a day in under a minute each. Require test and scan results in every pull request, route by CODEOWNERS, and keep each pull request to one scoped change.",
  watch="\"Three approvals instead of one\" adds friction, not review. A bypass list for reviewers and self-merge for agents remove oversight.")

# ------------------------------------------------------------ question → lesson
LINK = {
    "x1-d1-plan-first": ("M2-U4-C1", []), "x1-d1-plan-first-sequence": ("M2-U4-C1", []), "x1-d1-read-only-planner": ("M2-U4-C2", []),
    "x1-d1-control-plane-statements": ("M1-U4-C1", []), "x1-d1-job-outputs": ("M2-U6-C2", []), "x1-d1-critical-tier": ("M2-U6-C1", ["M6-U3-C1"]),
    "x1-d1-evidence": ("M2-U7-C1", []), "x1-d1-defensive-gating": ("M2-U6-C3", []),
    "x1-d2-mcp-secret-series": ("M2-U7-C2", []), "x1-d2-setup-steps": ("M3-U5-C2", []), "x1-d2-mcp-config": ("M3-U3-C1", []),
    "x1-d2-app-token": ("M3-U5-C3", []), "x1-d2-approve-workflows": ("M1-U4-C2", []), "x1-d2-hook-events": ("M2-U7-C3", []),
    "x1-d2-cloud-agent-statements": ("M3-U5-C1", ["M3-U4-C1"]), "x1-d2-hook-log": ("M2-U7-C3", []), "x1-d2-lock-file": ("M3-U2-C1", []),
    "x1-d3-source-of-truth": ("M5-U4-C1", []), "x1-d3-resume": ("M5-U3-C1", []), "x1-d3-drift": ("M5-U3-C2", []), "x1-d3-retention": ("M5-U3-C3", []),
    "x1-d3-continuity-statements": ("M5-U4-C2", ["M5-U4-C1"]), "x1-d3-reset": ("M5-U3-C4", []), "x1-d3-memory-vs-instructions": ("M5-U2-C1", []),
    "x1-d4-real-intent": ("M2-U3-C1", []), "x1-d4-root-cause": ("M5-U6-C1", []), "x1-d4-feedback-loop": ("M5-U6-C2", []),
    "x1-d4-required-check-series": ("M5-U5-C2", []), "x1-d4-skipped-check": ("M5-U5-C3", []), "x1-d4-evaluation-statements": ("M5-U5-C1", ["M5-U5-C2"]),
    "x1-d4-trigger-fix": ("M5-U6-C1", ["M5-U6-C2"]), "x1-d4-dependency-review": ("M5-U5-C4", []),
    "x1-d5-fan-in": ("M4-U3-C1", []), "x1-d5-workflow-run": ("M4-U3-C2", []), "x1-d5-concurrency-group": ("M4-U4-C1", []),
    "x1-d5-conflict-types": ("M4-U5-C1", []), "x1-d5-merge-validation": ("M4-U5-C1", []), "x1-d5-artifact-audit": ("M4-U6-C1", []),
    "x1-d5-subagent-frontmatter": ("M4-U7-C1", []), "x1-d5-isolation-statements": ("M4-U4-C2", ["M4-U4-C1"]), "x1-d5-ruleset-bypass": ("M4-U7-C2", []),
    "x1-d6-autonomy-levels": ("M6-U2-C1", []), "x1-d6-progressive-autonomy": ("M6-U2-C1", []), "x1-d6-risk-routing": ("M6-U2-C2", ["M2-U6-C2"]),
    "x1-d6-security-failure": ("M6-U7-C1", []), "x1-d6-rubber-stamping": ("M6-U7-C2", ["M6-U4-C1"]), "x1-d6-cli-tool-scope": ("M6-U2-C3", []),
    "x1-d6-governance-statements": ("M6-U4-C1", []),
    "c1": ("M2-U5-C1", []), "c2": ("M6-U3-C1", []), "c3": ("M3-U3-C1", []), "c4": ("M3-U4-C1", []),
    "c5": ("M4-U3-C3", []), "c6": ("M6-U5-C1", []), "c7": ("M1-U5-C1", []), "c8": ("M2-U2-C1", []),
}
