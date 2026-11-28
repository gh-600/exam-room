"""Case study · Northwind Traders. Ten screens: D1 x2, D2 x3, D3 x1, D4 x1, D5 x2, D6 x1."""
from lib import Q, opt, lq, dq, dn, PART, YESNO

SCENARIO = """### Overview

Northwind Traders is a wholesale company that develops a warehouse management platform. Northwind Traders has a GitHub organization named Northwind.

### Existing environment

Northwind has a private repository named `warehouse-api` that contains an ASP.NET Core service. The repository has the following configuration:

- The default branch is `main`. A ruleset named RS1 targets `main`. RS1 requires a pull request, one approving review, and a status check named `build-test`.
- A workflow named `ci.yml` runs for pull requests. It reports the `build-test` check and runs a CodeQL analysis. Code scanning alerts are shown in pull requests, but they do not block merging.
- GitHub Copilot cloud agent is enabled for `warehouse-api`. The agent opens pull requests. It cannot merge or deploy.
- An environment named `production` has required reviewers.

A workflow named `release.yml` deploys the service to production. The workflow contains the following lines.

```yaml
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
        with:
          ref: main
      - run: ./scripts/deploy.sh
```

### Planned changes

Northwind plans to implement the following changes:

- Assign two types of issues to the cloud agent: corrections to user interface texts in resource files, and changes to the authentication module.
- Add three custom agents named `planner`, `implementer`, and `test-writer`. The planner will rate the risk of each plan. A workflow will apply low-risk plans automatically and will route all other plans to an approval.
- Add a GitHub Agentic Workflow named `daily-status.md` that summarizes the open issues and creates an issue that contains a status report every day.
- Preinstall the .NET SDK and restore the NuGet packages in the environment of the cloud agent before the agent starts working.

### Problem statements

Northwind identifies the following issues:

- Last month, a faulty release was deployed. The team could not determine which commit was running in production, and the rollback took three hours.
- Three pull requests from the agent were merged although CodeQL had reported new alerts of high severity for them.
- In a Copilot Chat session in Visual Studio Code, a developer and the agent agreed that the retry logic of a task must use the company's shared resilience library. The cloud agent later continued the same task from the pull request and implemented its own retry loop.
- Pull request #482 from the agent has been open for five days. The pull request contains commits. It has no workflow run, no evidence, and no review request.
- Reviewers cannot tell which agent produced a pull request or where the evidence for the pull request is.

### Technical requirements

Northwind identifies the following technical requirements:

- Corrections to user interface texts are low risk and easily reversible. For these issues, speed of iteration is more important than agreeing on a plan in advance. The merge requirements of RS1 must continue to apply.
- The routing of plans by risk must not depend on a person who reads the plan.
- Each production deployment must be traceable to one commit, and a rollback must deploy a known earlier version.
- A pull request must not be merged when code scanning reports a new alert of high or critical severity.
- Decisions about a task must be available to every tool and every session that works on the task.
- In `daily-status.md`, the coding agent must run with read-only permissions. Write operations must be applied by a separate, gated step.
- Every pull request from a custom agent must identify the agent, and the evidence for the pull request must be durable and linked from the pull request.
- All solutions must follow the principle of least privilege and must not weaken the existing controls."""

SUBS = [

Q("c1", "single", "D1", "M2U4", "apply",
  stem="You need to recommend a workflow for the issues that correct user interface texts.\n\nWhich workflow should you recommend?",
  options=[
      opt("a", "A plan-first pull request, in which the plan is approved before any code is written", "Incorrect. Plan-first is for changes that are high risk or difficult to reverse. Here it would slow down work for which speed matters more."),
      opt("b", "Plan and execution in the same pull request, with the checks and the review of RS1", "Correct. The changes are low risk and easily reversible, and iteration speed matters. The plan stays visible, and RS1 still gates the merge."),
      opt("c", "Direct commits by the agent to `main`, with the plan in each commit message", "Incorrect. That bypasses the pull request, the review and the check that RS1 requires."),
      opt("d", "Plan and execution in the same pull request, with the agent on the bypass list of RS1", "Incorrect. A bypass actor can merge without meeting RS1, which weakens the existing controls."),
  ],
  answer=["b"],
  explanation="Both workflows are reviewed before the merge. They differ in when code may be generated. For low-risk, easily reversible changes for which speed and iteration matter, the plan and the code can be in the same pull request, with the required checks and the reviews kept. Plan-first is reserved for high-risk work such as the authentication module.",
  takeaway="Low risk and reversible → plan and execution in one pull request, checks and reviews unchanged.",
  evidence=[lq("speed and iteration are more important", "M2U4"),
            lq("changes are low-risk or easily reversible", "M2U4"),
            lq("Use plan + execution for medium/low risk work, but keep checks/reviews required.", "M2U4")]),

Q("c2", "single", "D1", "M6U2", "apply", also_units=["M6U6"],
  stem="You need to recommend how the `planner` agent reports the risk of a plan to meet the technical requirements.\n\nWhat should you recommend?",
  options=[
      opt("a", "A paragraph in the pull request description that explains the risk", "Incorrect. A narrative must be read and interpreted by a person before the plan can be routed."),
      opt("b", "A label that a reviewer adds to the pull request after reading the plan", "Incorrect. The routing would depend on the reviewer, which the requirement excludes."),
      opt("c", "A sentence at the end of the session log that states the risk level", "Incorrect. A workflow cannot route reliably on free text in a log."),
      opt("d", "A `risk` field in a machine-readable plan file that is uploaded as an artifact", "Correct. A workflow can read the field and route the plan, for example to automatic application or to an approval."),
  ],
  answer=["d"],
  explanation="A plan that drives automation must be structured. When the planner writes the risk rating as a field of a machine-readable file such as `plan.json`, a job can read it, expose it as an output, and route the plan. A rating that exists only as prose depends on interpretation, and the routing is then not enforced consistently.",
  takeaway="A structured plan carries its risk as a machine-readable field, and the workflow routes on it.",
  evidence=[lq("Decision guidance: Don't rely on narrative explanations of risk. Use a machine-readable signal and enforce routing.", "M6U2"),
            lq("When an agent produces a plan with a risk rating, that rating should determine how the system responds.", "M6U2"),
            lq("plan.json (machine-readable)", "M6U6")]),

Q("c3", "single", "D2", "M2U7", "apply",
  stem="You need to change `release.yml` to meet the technical requirements for production deployments.\n\nWhat should you do?",
  options=[
      opt("a", "Deploy a commit SHA or a tag that is passed to the workflow, and remove `ref: main`.", "Correct. Each deployment then refers to one explicit commit, and a rollback deploys the reference of a known earlier version."),
      opt("b", "Keep `ref: main`, and add a `concurrency` group named `production` to the job.", "Incorrect. A concurrency group keeps deployments from overlapping. The job would still deploy whatever `main` contains when it starts."),
      opt("c", "Deploy from a branch named `stable` that is updated after each merge into `main`.", "Incorrect. That is still the latest commit of a branch. Nothing records which commit a given deployment used."),
      opt("d", "Keep `ref: main`, and increase the number of required reviewers of `production`.", "Incorrect. More reviewers do not make the deployed commit identifiable."),
  ],
  answer=["a"],
  explanation="`ref: main` checks out the latest commit of the branch at the moment the job starts, which can be later than the commit that was approved. The rollback-safe pattern is to operate on explicit references. A commit SHA or a tag identifies exactly what is deployed, and rolling back means deploying the previous reference.",
  takeaway="Deploy explicit references, a commit SHA or a tag, never \"latest on a branch\".",
  evidence=[lq("Operate on explicit references (commit/tag) when deploying sensitive configuration, rather than \"latest on a branch.\"", "M2U7"),
            lq("Rollback readiness: high-risk changes include rollback notes and scope limits.", "M2U7")]),

Q("c4", "dropdown", "D2", "M3U5", "apply", docs=["agent-env"],
  stem="You need to create the workflow file that prepares the environment of GitHub Copilot cloud agent to meet the planned changes.\n\nHow should you complete the workflow?",
  template="# File: .github/workflows/[[file]]\nname: \"Copilot Setup Steps\"\n\non:\n  workflow_dispatch:\n\njobs:\n  [[job]]:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: [[perm]]\n    steps:\n      - uses: actions/checkout@v5\n"
           "      - uses: actions/setup-dotnet@v4\n        with:\n          dotnet-version: '9.0.x'\n      - run: dotnet restore\n",
  blanks={
      "file": {"options": ["copilot-instructions.yml", "copilot-setup-steps.yml", "dependabot.yml"], "answer": "copilot-setup-steps.yml",
               "rationale": "The agent's environment is customized with a workflow file at the fixed path `.github/workflows/copilot-setup-steps.yml`."},
      "job": {"options": ["build", "copilot-setup-steps", "setup"], "answer": "copilot-setup-steps",
              "rationale": "The file must contain a single job that is named `copilot-setup-steps`. A job with another name is not picked up."},
      "perm": {"options": ["none", "read", "write"], "answer": "read",
               "rationale": "The steps clone the repository to restore the packages, which needs `contents: read`. Write access is not needed, and the agent gets its own token for its work."},
  },
  explanation="The cloud agent works in an ephemeral environment that is powered by GitHub Actions. The steps of the `copilot-setup-steps` job run before the agent starts, so the SDK and the packages are in place. The file name and the job name are fixed, the permissions are set as low as the steps allow, and the file must be on the default branch.",
  takeaway="`.github/workflows/copilot-setup-steps.yml`, one job named `copilot-setup-steps`, lowest permissions, default branch.",
  evidence=[lq("On GitHub, Copilot in the cloud works in a GitHub Actions-powered environment, creates changes on a branch, and prepares those changes for review.", "M3U5"),
            dn("You customize Copilot's environment with a workflow file located at `.github/workflows/copilot-setup-steps.yml`. The file must contain a single `copilot-setup-steps` job, and its steps are executed before Copilot starts working. The example sets the permissions to the lowest that the steps need: `contents: read` if the steps clone the repository. The workflow won't trigger unless it is present on the default branch.", "agent-env")]),

Q("c5", "dropdown", "D2", "M3U4", "apply", also_units=["M3U2"],
  stem="You need to complete the frontmatter of `daily-status.md` to meet the technical requirements.\n\nHow should you complete the configuration?",
  template="---\non:\n  schedule: daily\n\npermissions:\n  contents: read\n  issues: [[perm]]\n\n[[section]]:\n  create-issue:\n    title-prefix: \"[daily-status] \"\n    labels:\n      - report\n\ntools:\n  github:\n---\n",
  blanks={
      "perm": {"options": ["none", "read", "write"], "answer": "read",
               "rationale": "The agent must read the open issues to summarize them, and it must run with read-only permissions. It does not create the issue itself."},
      "section": {"options": ["env", "safe-outputs", "steps"], "answer": "safe-outputs",
                  "rationale": "A safe output lets the agent propose the issue. A separate, gated step creates it, with the title prefix and the label that the frontmatter allows."},
  },
  explanation="In a GitHub Agentic Workflow, the Markdown expresses the intent and the frontmatter defines the boundaries. The coding agent gets read-only tokens. A write action, such as creating an issue, is declared as a safe output: the agent proposes it, and a separate gated step decides what is allowed and applies it.",
  takeaway="Agentic workflow: read-only `permissions`, and every write as a `safe-outputs` entry.",
  evidence=[lq("Read-only tokens by default so the agent can inspect repository state without directly changing it", "M3U4"),
            lq("Safe outputs that let the agent propose actions while a separate gated step decides what is allowed", "M3U4"),
            lq("Frontmatter for configuration such as triggers, permissions, tools, and safe outputs", "M3U2")]),

Q("c6", "single", "D3", "M5U4", "apply",
  stem="You need to prevent a repetition of the issue with the retry logic and meet the related technical requirement.\n\nWhat should you do?",
  options=[
      opt("a", "Repeat the decision in the prompt of every tool that works on the task.", "Incorrect. Copies in prompts are session context. They can diverge, and a tool that does not get the prompt does not know the decision."),
      opt("b", "Ask the developer to keep the same Copilot Chat session open until the task is merged.", "Incorrect. The context of a chat session in the IDE is not available to the cloud agent."),
      opt("c", "Store the decision as a user-level preference in Copilot Memory.", "Incorrect. A user-level preference belongs to one person, and a stored memory is not a guaranteed input for every session on the task."),
      opt("d", "Record the decision in the description of the pull request.", "Correct. The pull request is the place for decisions and progress, and every tool that works on the task can read it."),
  ],
  answer=["d"],
  explanation="State is shared through durable references, not through session context. The decision existed only in a chat session, so the cloud agent could not know it. Decisions and progress live in the pull request. Any tool or session that continues the task re-anchors to it and finds the decision there.",
  takeaway="A decision that matters goes into the pull request, never only into a chat.",
  evidence=[lq("Decisions and progress live in pull requests", "M5U4"),
            lq("Avoid storing critical information only in prompts or chat history", "M5U4"),
            lq("Always write important updates to issues or pull requests", "M5U4")]),

Q("c7", "single", "D4", "M5U5", "apply", docs=["merge-protection", "merge-protection-concept"],
  stem="You need to meet the technical requirement for code scanning alerts.\n\nWhat should you do?",
  options=[
      opt("a", "Add the security team to the CODEOWNERS file as the owner of all paths.", "Incorrect. That requests a review. It does not block a merge on the basis of the scan results."),
      opt("b", "In RS1, add **Require code scanning results** with the threshold **High or higher**.", "Correct. The rule prevents a pull request from being merged when the tool reports an alert at or above the threshold."),
      opt("c", "Enable push protection for secret scanning in `warehouse-api`.", "Incorrect. Push protection stops supported secrets from being committed. It does not act on vulnerabilities that CodeQL finds."),
      opt("d", "Increase the number of required approving reviews in RS1 to two.", "Incorrect. Reviewers approved the three pull requests despite the alerts. A second approval does not turn the alerts into a gate."),
  ],
  answer=["b"],
  explanation="CodeQL already produces the signal, but nothing enforces it. A ruleset can include a code scanning rule that prevents merging when a required tool reports alerts at or above a severity that you choose. With the security alert threshold set to **High or higher**, alerts of high and critical severity block the pull request.",
  takeaway="Scan results become a gate with the ruleset rule **Require code scanning results** and a severity threshold.",
  evidence=[lq("Treat security alerts or failed checks as blockers", "M5U5"),
            lq("Review security results in the pull request", "M5U5"),
            dn("You can add code scanning rules to rulesets to prevent pull requests from being merged, for example when a required tool finds an alert of a severity that is defined in the ruleset.", "merge-protection-concept"),
            dn("Under \"Branch protections\", you select **Require code scanning results**, add a tool such as CodeQL, and choose the thresholds. For security alerts, the choices are **None**, **Critical**, **High or higher**, **Medium or higher**, or **All**.", "merge-protection")]),

Q("c8", "single", "D5", "M4U7", "analyse",
  stem="You need to classify the state of pull request #482.\n\nWhich failure mode should you identify?",
  options=[
      opt("a", "Flapping", "Incorrect. Flapping means that workflows rerun repeatedly without converging. This pull request has no workflow run at all."),
      opt("b", "Conflicting outputs", "Incorrect. Conflicting outputs are pull requests that compete and block each other. Only one pull request is involved."),
      opt("c", "A stalled workflow", "Incorrect. A stalled workflow has checks that fail repeatedly or an approval that never arrives. Here no check ran and no review was requested."),
      opt("d", "Partial execution", "Correct. The pull request exists, but the evidence and the validation are missing."),
  ],
  answer=["d"],
  explanation="The module lists four failure modes of coordination. Partial execution is a pull request that exists without evidence or validation. A stalled workflow has checks that fail repeatedly or approvals that never arrive. Conflicting outputs are competing pull requests, and flapping is repeated reruns that do not converge. The state is read from the pull request timeline, the checks and the run history.",
  takeaway="Pull request without evidence or validation = partial execution.",
  evidence=[lq("partial execution (PR exists, but evidence or validation is missing),", "M4U7"),
            lq("stalled workflows (checks fail repeatedly or approvals never arrive),", "M4U7"),
            lq("flapping (workflows rerun repeatedly with no convergence).", "M4U7")]),

Q("c9", "multiple", "D5", "M4U6", "apply", select=2,
  stem="You need to meet the technical requirement for the pull requests of the three custom agents.\n\nWhich two actions should you perform? " + PART,
  options=[
      opt("a", "Use a title prefix and a label that name the agent, such as `[agent: implementer]`.", "Correct. Consistent attribution in titles and labels shows which agent produced a pull request."),
      opt("b", "Let the three agents push to one shared branch, so that their work is in one pull request.", "Incorrect. A shared branch interleaves commits and makes it harder to attribute a change to an agent."),
      opt("c", "Upload each agent's report as a workflow artifact, and link the run in an Evidence section.", "Correct. The artifact is durable evidence, and the link makes it reachable from the pull request."),
      opt("d", "Ask each agent to describe its results in the last comment of its session log.", "Incorrect. A description is the agent's own account, and it is not linked from the pull request."),
      opt("e", "Apply one label named `automation` to every pull request that an agent opens.", "Incorrect. One label for all agents does not identify which agent produced a pull request."),
  ],
  answer=["a", "c"],
  explanation="As the number of agents grows, reviewers need to know which agent produced a change and what evidence supports it. Attribution comes from conventions: a title prefix, a label, and standard sections in the body. Evidence comes from artifacts that are uploaded by the workflow and linked from the pull request.",
  takeaway="Attribution: title prefix and label for each agent. Evidence: uploaded artifacts, linked from the pull request.",
  evidence=[lq("PR titles: [agent: dependency] Update <package> to <version>", "M4U6"),
            lq("labels: agent: dependency, agent: security, agent: refactor", "M4U6"),
            lq("Artifacts create durable evidence that supports debugging and audits.", "M4U6")]),

Q("c10", "statements", "D6", "M6U2", "understand",
  stem="Northwind plans to increase the autonomy of the agents step by step.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "With propose-only autonomy, an agent can create branches and pull requests, and it cannot merge or deploy.", "answer": "yes",
       "explanation": "That is the definition of the propose-only level, and it is the level that the cloud agent has in `warehouse-api` today."},
      {"id": "s2", "statement": "The number of changed lines is sufficient to determine the risk level of a change.", "answer": "no",
       "explanation": "Risk also depends on where the change is applied, how easily it can be reversed, and how quickly it affects users or systems."},
      {"id": "s3", "statement": "Full automation is appropriate for a change that cannot be reversed, provided that the required checks pass.", "answer": "no",
       "explanation": "Full automation is used only when failures are reversible. Irreversible actions require approval."},
  ],
  explanation="Autonomy is granted in levels and matched to risk. Propose-only lets an agent create branches and pull requests. Wider levels are added as the agent proves reliable, and each level is bounded by the impact and the reversibility of the actions, not by the size of a change or by a green check.",
  takeaway="Autonomy follows impact and reversibility. Full automation only for reversible failures.",
  evidence=[lq("Propose-only autonomy: Agent can create branches and pull requests, but can't merge or deploy.", "M6U2"),
            lq("Risk depends not only on the action itself, but also on:", "M6U2"),
            lq("Use full automation only when failures are reversible. Require approval when actions are irreversible or affect production systems.", "M6U2")]),
]

CASE = {"id": "x2-case-northwind", "type": "case", "domain": "D1", "title": "Case study: Northwind Traders", "scenario": SCENARIO, "questions": SUBS}
