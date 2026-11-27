"""Domain 4 · Evaluation, failure analysis and tuning (Learn module 5, units 5-6; module 2, unit 3). Ten screens."""
from lib import Q, opt, lq, dq, dn, YESNO

QUESTIONS = [

Q("x1-d4-real-intent", "single", "D4", "M2U3", "analyse", also_units=["M1U3"],
  stem="An agent is assigned an issue to remediate a security alert for a vulnerable dependency in a GitHub repository named Repo1. The agent opens a pull request, all required checks pass, and the agent reports that the task is complete. The alert is still open, because the vulnerable version remains reachable through a transitive dependency.\n\n"
       "You need to change the task definition so that this outcome is no longer accepted as complete. What should you do?",
  options=[
      opt("a", "Add a second approving review to the ruleset for `main`.", "Incorrect. A second reviewer sees the same green checks. Nothing in the task says that the alert must close."),
      opt("b", "Instruct the agent to state its confidence level in the pull request description.", "Incorrect. Evaluation must rest on system signals, not on how confident the agent is."),
      opt("c", "Increase the number of times that the agent may retry failed checks.", "Incorrect. No check failed. The checks passed while the real goal was missed."),
      opt("d", "Add a success criterion that the alert is resolved, and verify it from the security signal.", "Correct. The criterion now states the real intent, and it is verified by a signal that the agent doesn't control."),
  ],
  answer=["d"],
  explanation="The task was judged by \"tests passed\" when its intent was \"vulnerability resolved\". Passing checks are necessary, but they only validate what they were built to detect. A success criterion must describe the real outcome and be measured by a system signal, here the state of the alert.",
  takeaway="Write success criteria for the real intent, and measure them with a system signal.",
  evidence=[lq("\"CI passed\" is necessary, but not always sufficient. Make success criteria reflect the real intent of the task (for example, \"vulnerability resolved\" rather than \"tests passed\").", "M2U3"),
            lq("These capabilities reinforce a key lesson: agent evaluation must be grounded in system signals, not in the agent's confidence.", "M1U3")]),

Q("x1-d4-root-cause", "match", "D4", "M5U6", "analyse",
  stem="You are analyzing four failed agent tasks in a GitHub repository named Repo1 so that you can decide what to improve.\n\nWhich root cause category does each failure belong to?",
  choices=[{"id": "reasoning", "text": "Reasoning error"}, {"id": "tool", "text": "Tool misuse"}, {"id": "context", "text": "Context issue"}],
  targets=[
      {"id": "t1", "text": "The agent based its change on a pull request state that newer commits had replaced.", "answer": "context",
       "rationale": "The agent worked from stale information: an outdated pull request state."},
      {"id": "t2", "text": "The agent implemented a discount rule that ignores one of the acceptance criteria in the issue.", "answer": "reasoning",
       "rationale": "The information was available and correct. The agent's decision was wrong."},
      {"id": "t3", "text": "The validation never ran, because the agent's workflow was configured for the wrong event.", "answer": "tool",
       "rationale": "A workflow was misconfigured and wasn't triggered properly."},
      {"id": "t4", "text": "The issue and the pull request description gave different values for a timeout, and the agent applied the wrong one.", "answer": "context",
       "rationale": "Two artifacts held conflicting information, so the context itself was faulty."},
  ],
  explanation="The category points to the fix. A reasoning error is fixed with clearer prompts and instructions. Tool misuse is fixed in the tool configuration, such as workflow triggers and permissions. A context issue is fixed in memory and state: remove stale or conflicting information and keep one source of truth.",
  takeaway="Wrong decision = reasoning. Wrong use of a workflow or command = tool. Stale, missing or conflicting information = context.",
  evidence=[lq("Ignoring acceptance criteria", "M5U6"), lq("Failing to trigger or use workflows properly", "M5U6"),
            lq("Using outdated pull request state", "M5U6"), lq("Conflicting information across artifacts", "M5U6")]),

Q("x1-d4-feedback-loop", "build", "D4", "M5U6", "apply",
  stem="An agent in a GitHub repository named Repo1 often produces pull requests that fail validation. You run the agent on a task, and you need to improve its behavior by using a feedback loop.\n\n"
       "Which four actions should you perform in sequence after the agent has run?",
  items=[
      {"id": "observe", "text": "Observe the failures in the workflow logs and artifacts."},
      {"id": "cause", "text": "Identify the root cause of the failures."},
      {"id": "fix", "text": "Apply a fix to the prompts, the memory, or the tool configuration."},
      {"id": "rerun", "text": "Re-run the workflow."},
      {"id": "remove", "text": "Remove the failing checks from the required status checks."},
      {"id": "writeall", "text": "Grant write access for all scopes to the workflow token."},
  ],
  answer=["observe", "cause", "fix", "rerun"],
  explanation="Improvement is iterative: look at the evidence first, name the cause, change the one thing that the cause points to, and run again to confirm. Removing checks or widening permissions hides the failure instead of correcting the behavior.",
  takeaway="Observe → root cause → fix prompts, memory or tools → re-run.",
  evidence=[lq("Observe failures through logs and artifacts", "M5U6"), lq("Identify the root cause", "M5U6"),
            lq("Apply fixes to prompts, memory, or tools", "M5U6"), lq("Re-run the workflow", "M5U6")]),

Q("x1-d4-required-check-series", "yesno", "D4", "M5U5", "evaluate", also_units=["M2U3"], docs=["rules", "branch-protection"],
  scenario="You have a GitHub repository named Repo1. The `main` branch has no rulesets and no branch protection rules. Agents open pull requests that target `main`. A workflow named `ci.yml` runs for every pull request that targets `main` and reports a check named `test`.\n\n"
           "You need to ensure that a pull request cannot be merged into `main` unless the tests pass.",
  items=[
      {"id": "s1", "solution": "You create a ruleset that targets `main` and requires a pull request with one approving review before merging.", "answer": "no",
       "explanation": "A reviewer can approve while `test` is failing. Nothing requires the check to pass."},
      {"id": "s2", "solution": "You create a ruleset that targets `main`, and you add `test` as a required status check.", "answer": "yes",
       "explanation": "The ruleset blocks the merge until `test` passes, whoever opened or approved the pull request."},
      {"id": "s3", "solution": "You create a branch protection rule for `main`, select **Require status checks to pass before merging**, and select the `test` check.", "answer": "yes",
       "explanation": "A branch protection rule with `test` selected as a required status check enforces the same gate as the ruleset."},
  ],
  explanation="A check that runs is only information. It becomes a gate when it is selected as a required status check, in a ruleset or in a branch protection rule. Required reviews are a separate control: they gate on human approval, not on test results.",
  takeaway="Tests gate a merge only as a required status check. Rulesets and branch protection can both do it.",
  evidence=[lq("Required checks ensure that certain conditions must be met before a pull request can be merged.", "M5U5"),
            lq("When this workflow is configured as a required check (via rulesets or branch protection), a pull request can't be merged until the check passes.", "M2U3")]),

Q("x1-d4-skipped-check", "single", "D4", "M5U5", "analyse", also_units=["M5U3"], docs=["conditions", "status-checks"],
  stem="A GitHub repository named Repo1 has a ruleset that requires a status check named `integration-tests` before merging into `main`. The check is reported by a job in a workflow that runs on `pull_request`. To save runner time, a developer adds the following line to the job.\n\n"
       "```yaml\nif: contains(github.event.pull_request.labels.*.name, 'run-integration')\n```\n\n"
       "An agent opens a pull request that doesn't have the label. The job is skipped, and the pull request is merged.\n\n"
       "You need to explain why the required check did not block the merge. What is the cause?",
  options=[
      opt("a", "Required status checks are not evaluated for pull requests that agents open.", "Incorrect. Required checks apply to every pull request that targets the branch, whoever opens it."),
      opt("b", "A required check that is never reported is treated as passed.", "Incorrect. A check that isn't reported stays pending, and a pending required check blocks the merge."),
      opt("c", "A job that is skipped by a condition reports its status as Success.", "Correct. A skipped job counts as successful, so the required check is satisfied without any test having run."),
      opt("d", "A ruleset is bypassed when a pull request has no labels.", "Incorrect. Labels have no effect on whether a ruleset applies."),
  ],
  answer=["c"],
  explanation="The two cases behave in opposite ways. A job skipped by an `if` condition reports Success and doesn't block the merge, even as a required check. A workflow that is skipped entirely, for example by a path or branch filter, leaves the check pending, and that blocks the merge. An evaluation signal is only as good as the guarantee that it actually ran.",
  takeaway="Skipped job = Success. Skipped workflow = Pending, which blocks.",
  evidence=[lq("Whether workflow checks are failing or missing", "M5U3"),
            dq("A job that is skipped will report its status as \"Success\". It will not prevent a pull request from merging, even if it is a required check.", "conditions")]),

Q("x1-d4-evaluation-statements", "statements", "D4", "M5U5", "understand", also_units=["M1U5"],
  stem="You are defining how the work of agents is evaluated in a GitHub repository named Repo1.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "A passing build proves that an agent's change is complete and low risk.", "answer": "no",
       "explanation": "Checks validate only what they were designed to detect. A passing build says nothing about what isn't tested."},
      {"id": "s2", "statement": "Acceptance criteria that are written in the issue give both the agent and the reviewer a basis for verifying completion.", "answer": "yes",
       "explanation": "Clear criteria in the issue are the reference for both of them."},
      {"id": "s3", "statement": "Selecting a check as a required status check prevents a pull request from being merged until the check passes.", "answer": "yes",
       "explanation": "That is what a required status check enforces."},
  ],
  explanation="Evaluation starts from success criteria written in the issue, uses the signals that the pull request shows, and becomes enforceable when checks are required. No single signal is proof of completeness, which is why checks are combined with review.",
  takeaway="Criteria in the issue, signals in the pull request, enforcement through required checks.",
  evidence=[lq("A passing build does not automatically mean the change is complete, appropriate, or low risk.", "M1U5"),
            lq("Clear criteria allow both the agent and the reviewer to verify completion.", "M5U5"),
            lq("Required checks ensure that certain conditions must be met before a pull request can be merged.", "M5U5")]),

Q("x1-d4-trigger-fix", "single", "D4", "M5U6", "analyse", docs=["events"],
  stem="Agents in a GitHub repository named Repo1 open pull requests that break the build after they are merged, but no failed checks appear on the pull requests. You review the evidence. The acceptance criteria are clear, the agents' plans match the issues, and the validation workflow starts with the following trigger.\n\n"
       "```yaml\non:\n  push:\n    branches: [main]\n```\n\n"
       "You need to correct the root cause so that the failures are detected before merging. What should you do?",
  options=[
      opt("a", "Add more detailed acceptance criteria to each issue.", "Incorrect. The criteria are clear and the plans match them, so this isn't a reasoning error."),
      opt("b", "Add a `pull_request` trigger for `main` to the validation workflow.", "Correct. The workflow only runs after a push to `main`, which is after the merge. A `pull_request` trigger makes it report on the pull request."),
      opt("c", "Rewrite the pull request descriptions to remove outdated decisions.", "Incorrect. Nothing indicates stale or conflicting context."),
      opt("d", "Add the validation command to the repository instructions file.", "Incorrect. An instruction asks the agent to validate. It doesn't make a check appear on the pull request."),
  ],
  answer=["b"],
  explanation="The evidence rules out reasoning and context, so the cause is tool misuse: the workflow is triggered by the wrong event. The matching improvement is in tool configuration, where you make sure that workflows trigger on the correct events.",
  takeaway="No checks on the pull request → look at the workflow's `on:` before blaming the agent.",
  evidence=[lq("Failing to trigger or use workflows properly", "M5U6"),
            lq("Ensure workflows trigger on the correct events (push, pull_request)", "M5U6")]),

Q("x1-d4-dependency-review", "single", "D4", "M5U5", "apply", docs=["protect-threats", "dependency-review"],
  stem="Agents in a GitHub repository named Repo1 add and update package dependencies in their pull requests.\n\n"
       "You need to ensure that a pull request that introduces a dependency with a known vulnerability is flagged in the pull request before it is merged. Which signal should you add to the evaluation of pull requests?",
  options=[
      opt("a", "A dependency review check", "Correct. Dependency review examines the dependency changes of a pull request and surfaces known vulnerabilities before the merge."),
      opt("b", "Secret scanning push protection", "Incorrect. Push protection stops supported secrets from being committed. It doesn't assess dependencies."),
      opt("c", "An environment with required reviewers", "Incorrect. An environment gates a job, typically a deployment. It doesn't inspect what a pull request changes."),
      opt("d", "An uploaded artifact that contains the build log", "Incorrect. A build log is evidence of the build. It doesn't report vulnerabilities in new dependencies."),
  ],
  answer=["a"],
  explanation="Security is part of evaluation, and each signal answers a different question. Code scanning looks for vulnerabilities in the code, secret scanning and push protection look for credentials, and dependency review looks at the dependencies that a pull request adds or changes.",
  takeaway="New vulnerable dependency in a pull request → dependency review.",
  evidence=[lq("Dependency review checks", "M5U5"), lq("Treat security alerts or failed checks as blockers", "M5U5"),
            dq("The dependency review action lets you catch vulnerable dependencies before they're merged, by surfacing known vulnerabilities in a pull request's dependency changes.", "protect-threats")]),
]
