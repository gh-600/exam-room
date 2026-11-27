"""Domain 5 · Multi-agent orchestration (Learn module 4). Nine standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO, PART

QUESTIONS = [

Q("x1-d5-fan-in", "dropdown", "D5", "M4U3", "apply", docs=["syntax", "concurrency"],
  stem="You are building a GitHub Actions workflow named `multi-agent-orchestration`. Two analysis agents run in parallel, and a third job merges their outputs into one plan.\n\n"
       "You need to ensure that the `plan_merger` job starts only after both analysis jobs finish, and that `plan_merger` jobs for the same branch never run at the same time.\n\n"
       "How should you complete the workflow?",
  template="jobs:\n  spec_analyzer:\n    runs-on: ubuntu-latest\n    steps:\n      - run: ./executors/spec_analyzer.sh\n\n"
           "  risk_reviewer:\n    runs-on: ubuntu-latest\n    steps:\n      - run: ./executors/risk_reviewer.sh\n\n"
           "  plan_merger:\n    runs-on: ubuntu-latest\n    [[key1]]: [spec_analyzer, risk_reviewer]\n    [[key2]]:\n      group: multiagent-${{ github.ref }}\n"
           "    steps:\n      - run: ./executors/plan_merger.sh\n",
  blanks={
      "key1": {"options": ["environment", "needs", "uses", "with"], "answer": "needs",
               "rationale": "`needs` lists the jobs that must complete first, so `plan_merger` waits for both analysis jobs. That is the fan-in. `uses` calls a reusable workflow, `with` passes inputs and `environment` names a deployment environment."},
      "key2": {"options": ["concurrency", "permissions", "strategy", "timeout-minutes"], "answer": "concurrency",
               "rationale": "A `concurrency` group allows only one job in the group to run at a time. Because the group name contains the branch ref, merge jobs for the same branch can't overlap. `strategy` only creates variations of a job inside one run."},
  },
  explanation="The two analysis jobs have no dependency on each other, so they start in parallel: that is the fan-out. `needs: [spec_analyzer, risk_reviewer]` makes `plan_merger` wait for both: that is the fan-in. A `concurrency` group on the job then keeps two merge jobs for the same branch from running together.",
  takeaway="Fan-in = `needs` with a list of jobs. No overlap = `concurrency` with a group name.",
  evidence=[lq("To coordinate multiple agents in parallel and then merge their outputs, use the fan-out/fan-in orchestration with needs.", "M4U3"),
            dq("You can also limit the concurrency of jobs within a workflow by using the `concurrency` keyword at the job level:", "concurrency")]),

Q("x1-d5-workflow-run", "single", "D5", "M4U3", "apply", docs=["events"],
  stem="You have a GitHub repository named Repo1 that contains two workflow files. The first workflow is named `CI Validation` and builds and tests pull requests from a dependency agent. The second workflow is named `Security Validation`.\n\n"
       "You need to ensure that Security Validation starts automatically each time a CI Validation run finishes. You must not change the CI Validation workflow file.\n\n"
       "Which trigger event should you configure in Security Validation?",
  options=[
      opt("a", "`workflow_dispatch`", "Incorrect. `workflow_dispatch` starts a run manually or through the API. Nothing would start it when CI Validation finishes."),
      opt("b", "`workflow_run`", "Correct. `workflow_run` names the `CI Validation` workflow and reacts to its `completed` activity type, without any change to that workflow."),
      opt("c", "`workflow_call`", "Incorrect. `workflow_call` makes Security Validation reusable, but CI Validation would then have to call it, and you must not change that file."),
      opt("d", "`pull_request`", "Incorrect. Both workflows would start together on each push to the pull request, so Security Validation wouldn't wait for CI to finish."),
  ],
  answer=["b"],
  explanation="Sequential orchestration means one step runs only after another has finished. Between two separate workflows, the `workflow_run` trigger expresses that order: the second workflow names the first one and reacts to its `completed` activity type.",
  takeaway="Run workflow B after workflow A, without touching A: `on: workflow_run` in B.",
  evidence=[lq("workflow completion triggers when one step should run after another.", "M4U3"),
            lq("Use this pattern when one agent's output must be validated before another step can proceed.", "M4U3"),
            dq("This event occurs when a workflow run is requested or completed. It allows you to execute a workflow based on execution or completion of another workflow.", "events")]),

Q("x1-d5-concurrency-group", "single", "D5", "M4U4", "analyse", docs=["concurrency"],
  stem="A GitHub repository named Repo1 has two workflows named `agent-lint` and `agent-tests`. Both run on every push to a pull request branch, and several agent sessions push to the same branches many times an hour. Both workflows contain the following block.\n\n"
       "```yaml\nconcurrency:\n  group: ${{ github.ref }}\n  cancel-in-progress: true\n```\n\n"
       "You discover that an `agent-tests` run is canceled whenever `agent-lint` starts on the same branch.\n\n"
       "You need to ensure that each workflow cancels only its own outdated runs on a branch. What should you do?",
  options=[
      opt("a", "Set `cancel-in-progress` to `false` in both workflows.", "Incorrect. Both workflows would still share one group per branch, so the runs of one workflow would wait for, or replace pending runs of, the other."),
      opt("b", "Move the `concurrency` block from the workflow level to each job.", "Incorrect. The group name would still be the branch ref alone, so the jobs of both workflows would stay in the same group."),
      opt("c", "Change the group to `${{ github.run_id }}` in both workflows.", "Incorrect. A run ID is unique, so every run would be alone in its group and outdated runs would never be canceled."),
      opt("d", "Change the group to `${{ github.workflow }}-${{ github.ref }}` in both workflows.", "Correct. The group is now specific to one workflow on one branch, so a new run cancels only the earlier run of the same workflow."),
  ],
  answer=["d"],
  explanation="A concurrency group belongs to the repository, not to a workflow. With `${{ github.ref }}` alone, every workflow that uses that group shares one slot per branch, so `agent-lint` cancels `agent-tests`. Adding `${{ github.workflow }}` to the name gives each workflow its own group on each branch.",
  takeaway="Group names must be unique across workflows: `${{ github.workflow }}-${{ github.ref }}`.",
  evidence=[lq("Setting only `${{ github.ref }}` without workflow makes concurrency global to the branch, potentially blocking unrelated workflows from running.", "M4U4"),
            dq("If you have multiple workflows in the same repository, concurrency group names must be unique across workflows to avoid canceling in-progress jobs or runs from other workflows.", "concurrency")]),

Q("x1-d5-conflict-types", "match", "D5", "M4U5", "understand",
  stem="Several agents work in a GitHub repository named Repo1, and you are classifying the conflicts that occurred last month.\n\nWhich conflict type does each situation describe?",
  choices=[{"id": "textual", "text": "Textual merge conflict"}, {"id": "semantic", "text": "Semantic conflict"},
           {"id": "policy", "text": "Policy conflict"}, {"id": "duplicate", "text": "Duplicate effort"}],
  targets=[
      {"id": "t1", "text": "Two pull requests merge cleanly, but the combined build fails because one renamed a method that the other calls.", "answer": "semantic",
       "rationale": "The merge is clean and the combined behavior is broken."},
      {"id": "t2", "text": "Two agents open separate pull requests that fix the same code scanning alert in different ways.", "answer": "duplicate",
       "rationale": "Two pull requests solve the same problem differently."},
      {"id": "t3", "text": "Two agents change the same lines of the same file in separate pull requests.", "answer": "textual",
       "rationale": "The same files and lines were changed."},
      {"id": "t4", "text": "One pull request changes application code and a workflow file, and the two areas require approval from different teams.", "answer": "policy",
       "rationale": "Protected areas require different reviews or approvals."},
  ],
  explanation="Naming the type tells you which control detects it. A textual conflict is visible in the pull request. A semantic conflict is only caught by checks that build and test the combined result. A policy conflict is resolved by ownership routing, and duplicate effort by clear responsibilities for each agent.",
  takeaway="Clean merge but broken result = semantic conflict. Only checks catch it.",
  evidence=[lq("Textual merge conflicts (same files/lines changed).", "M4U5"),
            lq("Semantic conflicts (clean merge, broken combined behavior).", "M4U5"),
            lq("Policy conflicts (protected areas require different reviews/approvals).", "M4U5"),
            lq("Duplicate effort (two PRs solving the same problem differently).", "M4U5")]),

Q("x1-d5-merge-validation", "single", "D5", "M4U5", "apply",
  stem="A GitHub repository named Repo1 receives pull requests from several agents. Conflicts between the pull requests and the `main` branch are often discovered late, after reviewers have already approved the changes.\n\n"
       "You need to ensure that a conflict with `main` is detected automatically each time an agent updates a pull request, and that the result is enforced before merging. The solution must not depend on reviewers noticing the conflict.\n\n"
       "What should you do?",
  options=[
      opt("a", "Add a job that runs `git merge --no-commit origin/main`, and make it a required status check.", "Correct. The job fails when the branch can't be merged, and as a required check it blocks the merge without anyone having to notice."),
      opt("b", "Add a CODEOWNERS entry that assigns all files in the repository to the core team.", "Incorrect. CODEOWNERS routes review requests. It doesn't test whether the branch merges with `main`."),
      opt("c", "Add `cancel-in-progress: true` to the `concurrency` block of the CI workflow.", "Incorrect. That cancels outdated runs. It reports nothing about conflicts."),
      opt("d", "Add a section named Conflicts to the pull request template that agents must complete.", "Incorrect. A template section is a reminder for people, which is exactly what the solution must not depend on."),
  ],
  answer=["a"],
  explanation="A merge validation step turns a conflict into a failed check as soon as the branch is updated. Making that check required is what makes it enforceable: the pull request can't merge until the check passes, whoever reviews it.",
  takeaway="Detect conflicts with a check, then make the check required.",
  evidence=[lq("GitHub PRs show merge conflicts, but teams often add a merge validation step so conflicts fail fast as checks:", "M4U5"),
            lq("If this is a required check, conflicts become enforceable and don’t depend on reviewers noticing them manually.", "M4U5")]),

Q("x1-d5-artifact-audit", "single", "D5", "M4U6", "apply", docs=["audit-log", "retention"],
  stem="A GitHub organization named Org1 runs an agent workflow that uploads an artifact named `agent-report` on every run. During an incident review, you discover that the artifact is missing from a run that finished two days ago. The repository uses the default retention period for artifacts.\n\n"
       "You need to identify who deleted the artifact and when. What should you do?",
  options=[
      opt("a", "Re-run the workflow and compare the new artifact with the job log.", "Incorrect. A re-run produces a new artifact. It doesn't show who removed the earlier one."),
      opt("b", "Review the timeline of the pull request that triggered the run.", "Incorrect. The pull request timeline records commits, reviews and checks. It doesn't record artifact deletions."),
      opt("c", "Search the organization audit log for `action:artifact.destroy`.", "Correct. The audit log records the manual deletion of a workflow artifact, with the actor, the time and the repository."),
      opt("d", "Run `gh agent-task view --log --follow` for the agent session.", "Incorrect. That command streams the log of an agent session. It doesn't cover what happened to an artifact afterwards."),
  ],
  answer=["c"],
  explanation="With the default retention period, an artifact from two days ago hasn't expired, so someone deleted it. Deletions of workflow artifacts are written to the organization audit log as `artifact.destroy`, which answers who and when.",
  takeaway="Missing artifact before it could expire → audit log, `action:artifact.destroy`.",
  evidence=[lq("If workflow artifacts (output files) are unexpectedly missing, GitHub audit logging reveals deletions.", "M4U6"),
            lq("This event shows who deleted an artifact, when, and the affected repository.", "M4U6"),
            dn("The organization audit log lists the event `artifact.destroy`: \"A workflow run artifact was manually deleted.\" By default, artifacts and logs are retained for 90 days.", "audit-log")]),

Q("x1-d5-subagent-frontmatter", "multiple", "D5", "M4U7", "analyse", docs=["custom-agents"], select=2,
  stem="You are designing a planner agent that delegates work to an implementer agent. The profile of the implementer agent starts with the following frontmatter.\n\n"
       "```yaml\n---\nname: implementer\ndisable-model-invocation: true\nuser-invocable: true\n---\n```\n\n"
       "The design has the following requirements:\n\n- The planner must be able to invoke the implementer as a subagent.\n- Users must not be able to select the implementer directly.\n\n"
       "You need to meet the requirements. Which two changes should you make to the frontmatter of the implementer agent? " + PART,
  options=[
      opt("a", "Set `disable-model-invocation` to `false`.", "Correct. While the value is `true`, the agent can't be invoked as a subagent, so the planner's delegation fails."),
      opt("b", "Set `user-invocable` to `false`.", "Correct. With `false`, users can't select the agent, and it can only be reached programmatically."),
      opt("c", "Add `agents: [planner]`.", "Incorrect. `agents` lists the subagents that an agent may orchestrate. It belongs in the planner's frontmatter and names the implementer."),
      opt("d", "Remove the `name` property.", "Incorrect. The name is how a handoff finds the agent. Removing it doesn't change who may invoke the agent."),
  ],
  answer=["a", "b"],
  explanation="Two properties control who can start a custom agent. `disable-model-invocation: true` stops other agents from invoking it, which breaks orchestration. `user-invocable: false` hides it from users. The design needs the opposite of the current values for both.",
  takeaway="Subagent only: `disable-model-invocation: false` and `user-invocable: false`.",
  evidence=[lq("A `disable-model-invocation: true` agent cannot be called as a subagent, which can cause orchestration failures.", "M4U7"),
            lq("`agents`: lists allowed subagents for this agent to orchestrate", "M4U7"),
            dn("`user-invocable` controls whether a custom agent can be selected by a user. When it is `false`, the agent can't be selected manually and can only be accessed programmatically. `disable-model-invocation: true` means the agent is not used automatically and must be selected manually.", "custom-agents")]),

Q("x1-d5-isolation-statements", "statements", "D5", "M4U4", "understand", docs=["syntax"],
  stem="You are reviewing the isolation design of a multi-agent system in a GitHub repository named Repo1.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "A `strategy.matrix` setting prevents two runs of the same workflow from overlapping when two agent sessions push to the same branch.", "answer": "no",
       "explanation": "A matrix creates several jobs inside one run. It doesn't control what happens between separate runs. That is the job of `concurrency`."},
      {"id": "s2", "statement": "Giving each agent a dedicated branch, such as `agent/dependency/<ticket>`, keeps its changes bounded and helps reviewers understand intent and scope.", "answer": "yes",
       "explanation": "A dedicated branch per agent bounds the change and shows which agent produced it."},
      {"id": "s3", "statement": "Letting several agents share one branch simplifies rollback and auditing, because all of their commits are in one place.", "answer": "no",
       "explanation": "On a shared branch the commits interleave and ownership becomes ambiguous, so one agent's change can't be reverted or attributed cleanly."},
  ],
  explanation="Isolation separates agents by branch, by workflow and by permissions, and uses `concurrency` for runs that overlap in time. A matrix is a different tool: it fans one job out into variations within a single run.",
  takeaway="Matrix = parallel jobs inside one run. Concurrency = control across runs.",
  evidence=[lq("This makes changes bound and helps reviewers understand intent and scope.", "M4U4"),
            lq("Using `strategy.matrix` controls intra-run parallelism, not parallelism across triggers or agent sessions.", "M4U4"),
            lq("If multiple agents share the same branch or workflow context, you can end up with interleaved commits, ambiguous ownership, and repeated failures. This makes rollback and auditing significantly harder.", "M4U4")]),

Q("x1-d5-ruleset-bypass", "single", "D5", "M4U7", "apply", docs=["copilot-on-github", "ruleset-bypass"],
  stem="A GitHub repository named Repo1 has a ruleset named RS1 that targets all branches. After RS1 is enabled, GitHub Copilot cloud agent can no longer push commits to its `copilot/` branches, because one of the rules in RS1 rejects them. The agent's tasks fail.\n\n"
       "You need to allow the agent to push to its branches. RS1 must continue to apply to all other contributors on all branches.\n\n"
       "What should you do?",
  options=[
      opt("a", "Change the enforcement status of RS1 to Disabled.", "Incorrect. A disabled ruleset no longer applies to anyone."),
      opt("b", "Add Copilot as a bypass actor in RS1.", "Correct. The bypass applies to Copilot only, so the rules of RS1 still bind every other contributor."),
      opt("c", "Add the repository administrator role to the bypass list of RS1.", "Incorrect. That lets administrators bypass the rules. The agent is still blocked."),
      opt("d", "Change the target of RS1 from all branches to the default branch only.", "Incorrect. The agent could push again, but RS1 would stop applying to the other branches for everyone."),
  ],
  answer=["b"],
  explanation="A repository rule can stop the agent from creating or updating its branch. The supported fix is a bypass for Copilot on that ruleset. It is the narrowest change: one actor, one ruleset, and the rule stays active for people.",
  takeaway="Rule blocks the agent's branch → bypass for Copilot on that ruleset, not a weaker ruleset.",
  evidence=[lq("In the repository's Branches/Rulesets settings, locate your ruleset. Add \"GitHub Copilot\" as a bypass actor for that ruleset.", "M4U7"),
            dn("A ruleset or branch protection rule can prevent Copilot from creating or updating pull requests. Repository administrators can configure a ruleset bypass for Copilot.", "copilot-on-github")]),
]
