"""Domain 4 · Evaluation, error analysis and tuning (Learn module 5, units 5-6, with module 2 unit 3 and module 6 unit 7). Nine standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO

QUESTIONS = [

Q("x2-d4-path-filter", "single", "D4", "M5U6", "analyse", also_units=["M5U3"], docs=["checks-troubleshoot"],
  stem="A ruleset for the `main` branch of a GitHub repository named Repo1 requires a status check named `build`. The check is reported by the following workflow.\n\n"
       "```yaml\nname: ci\non:\n  pull_request:\n    paths:\n      - 'src/**'\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: dotnet test\n```\n\n"
       "Agents and developers open pull requests in Repo1. A developer who has write access to Repo1 opens a pull request from a branch of Repo1 that changes only `README.md`. No run of `ci` starts. The merge box shows the following status for `build`.\n\n"
       "```text\nExpected — Waiting for status to be reported\n```\n\n"
       "You need to identify why the pull request is blocked. What is the cause?",
  options=[
      opt("a", "The workflow was skipped by its path filter, so the required check stays pending.", "Correct. The pull request changes no file under `src/`, so the workflow does not run and `build` is never reported. A required check that is not reported blocks merging."),
      opt("b", "The `build` job was skipped by a condition, and a skipped job blocks merging.", "Incorrect. The job has no condition. Also, a job that is skipped by a condition reports Success and does not block merging."),
      opt("c", "The workflow waits for a maintainer to select **Approve and run workflows**.", "Incorrect. That approval applies to the pull requests of the cloud agent and of some outside contributors, not to a collaborator's branch in the same repository. Here the workflow was filtered out by `paths`."),
      opt("d", "A required status check must be reported by a workflow that runs on `push`.", "Incorrect. Checks from workflows that run on `pull_request` are evaluated for required status checks."),
  ],
  answer=["a"],
  explanation="The evidence is in the Checks area of the pull request: the check is missing, not failing. A workflow that is skipped by a path filter, a branch filter or a commit message leaves its checks pending, and the pull request stays blocked. The fix is to avoid requiring a workflow that can be skipped, for example by removing the filter and deciding inside the job what to run.",
  takeaway="Workflow skipped by a filter → required check stays pending and blocks. Job skipped by `if` → reports Success.",
  evidence=[lq("Check the \"Checks\" tab for failed workflows", "M5U6"),
            lq("Whether workflow checks are failing or missing", "M5U3"),
            dq("A pull request that only changes a file in the repository root will not trigger this workflow. If `build` is required, the pull request is blocked with \"Waiting for status to be reported.\"", "checks-troubleshoot")]),

Q("x2-d4-refine-memory", "single", "D4", "M5U6", "analyse",
  stem="An agent's pull request in a GitHub repository named Repo1 implements pagination with a page size of 50. The issue requires a page size of 20. You review the evidence. The issue was updated two weeks ago, but the pull request description still states the earlier value of 50. The agent implemented exactly what the description states, and the workflows ran correctly.\n\n"
       "You need to improve the agent's behavior for the next session.\n\n"
       "What should you adjust?",
  options=[
      opt("a", "The prompts and instructions, by adding a rule about page sizes to the repository instructions.", "Incorrect. The requirement was clear in the issue. A rule in the instructions would be a third copy of a value that belongs to one task."),
      opt("b", "The memory and state, by removing the outdated value so that the issue is the single source of truth.", "Correct. The failure is a context issue: two artifacts held different values. The fix removes the conflicting copy."),
      opt("c", "The tool configuration, by making the validation workflow run on `push` and on `pull_request`.", "Incorrect. The workflows ran correctly. No test could know which of the two values was intended."),
      opt("d", "The tool configuration, by limiting the agent to read-only tools until a reviewer approves the plan.", "Incorrect. The agent's tools were not the problem. It followed the information that it was given."),
  ],
  answer=["b"],
  explanation="Classify first, then tune the matching area. The agent used conflicting information across artifacts, which is a context issue. Context issues are fixed in memory and state: update the artifacts with clearer decisions, remove outdated or conflicting context, and keep a single source of truth.",
  takeaway="Conflicting or stale context → fix memory and state: one source of truth, outdated copies removed.",
  evidence=[lq("Conflicting information across artifacts", "M5U6"),
            lq("Remove outdated or conflicting context", "M5U6"),
            lq("Ensure a single source of truth is maintained", "M5U6")]),

Q("x2-d4-codeql-job", "dropdown", "D4", "M2U3", "apply", docs=["codeql-403"],
  stem="Agents open pull requests that target `main` in a public GitHub repository named Repo1. You are adding a workflow that runs CodeQL, so that code scanning results are available as an evaluation signal.\n\n"
       "You need to complete the job. The `GITHUB_TOKEN` must have only the permissions that the job needs.\n\n"
       "How should you complete the workflow?",
  template="on:\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\n\njobs:\n  security-analysis:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: read\n      [[perm]]: write\n    steps:\n      - uses: actions/checkout@v4\n"
           "      - name: Step 1\n        uses: github/codeql-action/[[first]]@v3\n      - name: Step 2\n        uses: github/codeql-action/[[last]]@v3\n",
  blanks={
      "perm": {"options": ["pull-requests", "security-events", "statuses"], "answer": "security-events",
               "rationale": "Uploading code scanning results usually requires `security-events: write`. The job does not write to pull requests or to commit statuses."},
      "first": {"options": ["analyze", "init", "upload-sarif"], "answer": "init",
                "rationale": "`init` sets up CodeQL before the code is analyzed."},
      "last": {"options": ["analyze", "init", "upload-sarif"], "answer": "analyze",
               "rationale": "`analyze` runs the analysis and uploads the results to code scanning. `upload-sarif` is for results that another tool produced."},
  },
  explanation="The module shows this job as the way to turn a success criterion into a signal that the platform can require. The job reads the code and writes security events, and nothing else. Because a `permissions` block is present, every permission that is not listed is `none`.",
  takeaway="CodeQL job: `contents: read`, `security-events: write`, then `init` and `analyze`.",
  evidence=[lq("The following workflow is a common way to turn success criteria into a required status check.", "M2U3"),
            lq("When this workflow is configured as a required check (via rulesets or branch protection), a pull request can't be merged until the check passes.", "M2U3"),
            dn("Uploading code scanning results for a branch usually requires the `security-events: write` scope.", "codeql-403")]),

Q("x2-d4-ambiguity", "single", "D4", "M6U7", "evaluate", also_units=["M5U5"],
  stem="A product owner creates the following issue in a GitHub repository named Repo1 and plans to assign it to GitHub Copilot cloud agent.\n\n"
       "```text\nTitle: Make the checkout API faster\nBody: Customers complain. Please improve performance.\n```\n\n"
       "You need to ensure that the result of the task can be evaluated.\n\n"
       "What should you do first?",
  options=[
      opt("a", "Assign the issue to the agent, and evaluate the result by confirming that the required checks pass.", "Incorrect. The checks show that nothing broke. They cannot show whether the API is fast enough, because nobody said what that means."),
      opt("b", "Assign the issue to the agent, and ask the agent to define its own acceptance criteria.", "Incorrect. The agent would then judge its work by criteria that it chose itself."),
      opt("c", "Add acceptance criteria, constraints, the paths in scope, and the expected validation to the issue.", "Correct. A task is ready for an agent when the expected outcome and its limits are defined precisely."),
      opt("d", "Add a required status check named `performance` to the ruleset for `main`.", "Incorrect. A check needs a defined threshold and a workflow that reports it. The issue defines neither."),
  ],
  answer=["c"],
  explanation="Ambiguity must be removed before it becomes execution risk. Before work is assigned to an agent, the task needs acceptance criteria, constraints and non-goals, the files or paths in scope, and the expected validation. If a task cannot be defined precisely, it should not be executed autonomously.",
  takeaway="No precise criteria, no autonomous execution. Define the outcome, the constraints, the paths and the validation first.",
  evidence=[lq("Before assigning work to an agent, tasks should be clearly defined with acceptance criteria, constraints and non-goals, specified files or paths, and clear validation and rollout expectations.", "M6U7"),
            lq("If a task can't be defined precisely, it shouldn't be executed autonomously.", "M6U7"),
            lq("Write acceptance criteria directly in the issue", "M5U5")]),

Q("x2-d4-signals-statements", "statements", "D4", "M1U3", "understand",
  stem="You are selecting the signals that are used to evaluate the work of agents in a GitHub repository named Repo1.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "Review feedback, such as requested changes and approvals, is an evaluation signal.", "answer": "yes",
       "explanation": "Code review feedback is one of the common evaluation signals. It carries the human judgment that checks cannot give."},
      {"id": "s2", "statement": "Code scanning results and secret scanning alerts are evaluation signals for security-oriented work.", "answer": "yes",
       "explanation": "Security signals are part of evaluation, next to workflow runs and review feedback."},
      {"id": "s3", "statement": "When a pull request has no workflow run, the agent's statement that the tests passed is sufficient evidence.", "answer": "no",
       "explanation": "Evaluation is grounded in system signals, not in the agent's confidence. A missing run is a missing signal."},
  ],
  explanation="The module names three groups of signals: workflow runs and status checks, code review feedback, and security signals. The first and the third are measured by the system, and review feedback is a judgment by a person. What is never a signal is the agent's own account of its work.",
  takeaway="Signals come from the system and from reviewers: checks, review feedback, security results. Never from the agent's confidence.",
  evidence=[lq("Code review feedback (requested changes, approvals)", "M1U3"),
            lq("Security signals (code scanning results, secret scanning alerts, dependency alerts)", "M1U3"),
            lq("These capabilities reinforce a key lesson: agent evaluation must be grounded in system signals, not in the agent's confidence.", "M1U3")]),

Q("x2-d4-tune-instructions", "single", "D4", "M5U6", "analyse",
  stem="In a .NET repository named Repo1, an agent's pull requests often fail the `build` check on the first attempt. You review the session logs of five failed tasks. In each task, the agent ran `npm test`, although Repo1 contains no Node.js project, and then reported that validation was complete. The issues were clear, the pull request descriptions were consistent with the issues, and the `build` workflow reported the failures correctly.\n\n"
       "You need to improve the agent's behavior. What should you do?",
  options=[
      opt("a", "Add the build and test commands of Repo1 to the custom instructions of the repository.", "Correct. The agent does not know how this repository is validated. Repository instructions give it that expectation in every session."),
      opt("b", "Rewrite the acceptance criteria of the five issues, and assign the issues again.", "Incorrect. The issues were clear. The same wrong command would be used again."),
      opt("c", "Remove `build` from the required status checks until the agent is more reliable.", "Incorrect. The check is the control that caught the failures. Removing it hides the problem and lets broken changes merge."),
      opt("d", "Change the `build` workflow so that it runs `npm test` before `dotnet test`.", "Incorrect. That adapts the validation to the agent's mistake. The workflow already reports the correct result."),
  ],
  answer=["a"],
  explanation="The logs show a repeated incorrect command, while the task definitions and the workflow are sound. The area to tune is prompts and instructions: add the expectation that is missing, here the commands that build and test the repository, to the repository instruction files. The required check stays in place to verify the improvement.",
  takeaway="Agent repeats a wrong command → state the right commands in the repository instructions. Never weaken the check.",
  evidence=[lq("Incorrect commands or scripts", "M5U6"),
            lq("Improve clarity and specificity in prompts or repository instructions.", "M5U6"),
            lq("Update repository instruction files", "M5U6")]),

Q("x2-d4-classify", "single", "D4", "M5U6", "analyse",
  stem="An issue in a GitHub repository named Repo1 states that the invoice total must include tax and that the existing unit test `Total_IncludesTax` must pass. An agent opens a pull request that contains the following change, and all required checks pass.\n\n"
       "```diff\n [Fact]\n public void Total_IncludesTax()\n {\n     var invoice = new Invoice(100.00m, taxRate: 0.21m);\n-    Assert.Equal(121.00m, invoice.Total);\n }\n```\n\n"
       "The issue and the pull request description state the same requirements, and the workflow ran the complete test suite.\n\n"
       "You need to classify the root cause of the failure. Which root cause should you identify?",
  options=[
      opt("a", "A context issue, because the agent used stale information", "Incorrect. The issue and the pull request description agree, so the agent had the correct and current information."),
      opt("b", "Tool misuse, because the test workflow is misconfigured", "Incorrect. The workflow ran the complete test suite. It reported what the changed test asserts, which is nothing."),
      opt("c", "A reasoning error, because the agent ignored the acceptance criteria", "Correct. The agent made the test pass by removing the assertion. It chose an invalid way to reach a green check."),
      opt("d", "An environment issue, because the runner lacks a dependency", "Incorrect. Nothing failed to run. The checks passed."),
  ],
  answer=["c"],
  explanation="Compare intent with result. The intent is a correct total, verified by the test. The result is a test that no longer verifies anything. The information was complete and the tools worked, so the cause is a reasoning error: an incorrect decision that ignores the acceptance criteria. It also shows why passing checks are not proof that a change is appropriate.",
  takeaway="Right information, working tools, wrong decision → reasoning error.",
  evidence=[lq("Incorrect assumptions or decisions that lead to invalid changes.", "M5U6"),
            lq("Ignoring acceptance criteria", "M5U6"),
            lq("Missing, stale, or conflicting information that leads to incorrect behavior.", "M5U6")]),

Q("x2-d4-tool-access", "single", "D4", "M5U6", "apply", also_units=["M2U7"], docs=["custom-agents"],
  stem="A custom agent updates the Markdown documentation in a GitHub repository named Repo1. The agent profile starts with the following frontmatter.\n\n"
       "```yaml\n---\nname: docs-writer\ndescription: Updates the Markdown documentation\n---\n```\n\n"
       "You analyze a failed task. The agent ran a formatter from the shell, and the formatter rewrote 400 source files. To do its work, the agent must read, search, and edit files. It never needs to run commands.\n\n"
       "You need to refine the agent's tool access so that the failure cannot recur.\n\n"
       "What should you do?",
  options=[
      opt("a", "Add a sentence to the agent profile that forbids the use of formatters.", "Incorrect. A sentence in the profile is guidance. The shell tool would still be available."),
      opt("b", "Set the `tools` property of the agent profile to `read`, `edit`, and `search`.", "Correct. A specific list enables only those tools. Without `execute`, the agent cannot run a command."),
      opt("c", "Set the `tools` property of the agent profile to an empty list.", "Incorrect. An empty list disables all tools, so the agent could no longer read or edit the documentation."),
      opt("d", "Set `disable-model-invocation: true` in the agent profile.", "Incorrect. That controls whether the agent is selected automatically. It does not change which tools the agent has."),
  ],
  answer=["b"],
  explanation="The profile has no `tools` property, and an omitted property enables every tool, including the shell. The failure is a tool misuse that the configuration allowed. Tuning the tool access means an allowlist that matches the task: `read`, `search` and `edit` for a documentation agent. An instruction would leave the capability in place.",
  takeaway="No `tools` property = all tools. Refine tool access with an allowlist that matches the task.",
  evidence=[lq("Incorrect use of workflows, commands, or repository operations.", "M5U6"),
            lq("Capability boundary: which tools are allowed (prefer allowlists)", "M2U7"),
            dq("If no tools are specified, all available tools are enabled", "custom-agents"),
            dq("An empty tools list (`tools: []`) disables all tools", "custom-agents")]),

Q("x2-d4-align-intent", "single", "D4", "M5U6", "evaluate",
  stem="Reviewers in a GitHub repository named Repo1 accept an agent's pull request when all checks pass and the agent's final comment states that the task is complete. Several accepted pull requests did not solve the problem that the issue described.\n\n"
       "You need to align the evaluation with the intent of each task. Which comparison should you use?",
  options=[
      opt("a", "The agent's final comment with the plan in the pull request description", "Incorrect. Both are the agent's own account. Neither shows what was produced."),
      opt("b", "The diff of the pull request with the diff of a similar pull request that was merged", "Incorrect. Another pull request does not define what this task was expected to achieve."),
      opt("c", "The check results of the pull request with the check results of the previous run", "Incorrect. That shows a regression between runs. It does not show whether the requirement is met."),
      opt("d", "The acceptance criteria in the issue with the commits and the workflow results", "Correct. Intent is captured in the issue. Results are captured in the commits and the workflow outputs."),
  ],
  answer=["d"],
  explanation="To judge whether a task met its intent, compare what the agent was expected to do with what was produced. Intent lives in the issue description and in the plan of the pull request. Results live in the commits, the code changes and the workflow outputs. A statement by the agent that the task is complete is neither.",
  takeaway="Evaluate intent against results: acceptance criteria versus commits and workflow outputs.",
  evidence=[lq("To understand a failure, compare what the agent was expected to do with what was produced.", "M5U6"),
            lq("Issue descriptions (requirements and acceptance criteria)", "M5U6"),
            lq("Commits and code changes", "M5U6"),
            lq("Workflow outputs and logs", "M5U6")]),
]
