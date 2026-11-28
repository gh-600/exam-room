"""Domain 5 · Multi-agent coordination (Learn module 4, with module 6 unit 7 for the agent lifecycle). Eight standalone screens."""
from lib import Q, opt, lq, dq, dn, PART

QUESTIONS = [

Q("x2-d5-workflow-run-gate", "dropdown", "D5", "M4U3", "apply", docs=["events"],
  stem="A GitHub repository named Repo1 has a workflow named `CI Validation` that builds and tests the pull requests of a dependency agent. You are creating a second workflow that runs a security agent.\n\n"
       "You need to ensure that the second workflow starts when `CI Validation` finishes, and that the `validate` job runs only if `CI Validation` succeeded.\n\n"
       "How should you complete the workflow?",
  template="name: Security Validation\n\non:\n  workflow_run:\n    [[key]]: [CI Validation]\n    types:\n      - [[type]]\n\njobs:\n  validate:\n    if: ${{ github.event.workflow_run.[[prop]] == 'success' }}\n    runs-on: ubuntu-latest\n    steps:\n      - run: ./executors/security_agent.sh\n",
  blanks={
      "key": {"options": ["branches", "needs", "workflows"], "answer": "workflows",
              "rationale": "`workflows` names the workflow whose runs start this one. `needs` orders jobs inside one workflow, and `branches` only filters by branch."},
      "type": {"options": ["completed", "in_progress", "requested"], "answer": "completed",
               "rationale": "`completed` starts the workflow when the other run has finished. `requested` and `in_progress` fire before a result exists."},
      "prop": {"options": ["conclusion", "result", "status"], "answer": "conclusion",
               "rationale": "The result of the triggering run is in `github.event.workflow_run.conclusion`. Without the condition, the job would also run after a failed `CI Validation`."},
  },
  explanation="Sequential orchestration is used when the output of one step must be validated before the next step proceeds. `workflow_run` with `types: [completed]` starts the second workflow when the first one finishes, whatever its result. To continue only after success, the job needs a condition on the conclusion of the triggering run.",
  takeaway="`workflow_run` fires on every completion. Gate on `github.event.workflow_run.conclusion == 'success'`.",
  evidence=[lq("Use this pattern when one agent's output must be validated before another step can proceed.", "M4U3"),
            dq("A workflow run is triggered regardless of the conclusion of the previous workflow.", "events"),
            dq("If you want to run a job or step based on the result of the triggering workflow, you can use a conditional with the `github.event.workflow_run.conclusion` property.", "events")]),

Q("x2-d5-live-log", "single", "D5", "M4U7", "apply", docs=["agent-task"],
  stem="You delegated a task to GitHub Copilot cloud agent in a GitHub repository named Repo1. The session is associated with pull request #123. No new commit has appeared for 40 minutes, and you suspect that the session is stalled.\n\n"
       "You need to stream the session log to your terminal while the agent works. Which command should you run?",
  options=[
      opt("a", "`gh run watch 123`", "Incorrect. `gh run watch` follows a workflow run that is identified by its run ID. It does not show the log of an agent session."),
      opt("b", "`gh pr checks 123 --watch --interval 30`", "Incorrect. This shows the status of the checks of the pull request, not what the agent is doing."),
      opt("c", "`gh agent-task list`", "Incorrect. This lists your running and past sessions. It does not show a log."),
      opt("d", "`gh agent-task view 123 --log --follow`", "Correct. `view` selects the session of the pull request, `--log` shows the session log, and `--follow` streams it live."),
  ],
  answer=["d"],
  explanation="A stalled or long-running agent session is diagnosed from its session log. The GitHub CLI can stream that log while the agent works. The log shows the last action of the agent, which tells you whether the agent is waiting, looping or blocked.",
  takeaway="Stalled agent session → `gh agent-task view … --log --follow`.",
  evidence=[lq("Use this command to debug a stalled or long-running agent run in real time.", "M4U7"),
            dq("To view the session logs, add the `--log` option. Optionally, use the `--follow` option to stream live logs as the agent works.", "agent-task")]),

Q("x2-d5-artifact-coordination", "build", "D5", "M4U3", "apply",
  stem="You are designing how an analysis agent hands its proposal to the rest of a multi-agent workflow in a GitHub repository named Repo1. The handoff must leave evidence that reviewers can inspect, and the agent must not write to the repository.\n\n"
       "Which three actions should be performed in sequence?",
  items=[
      {"id": "run", "text": "The agent runs with restricted permissions."},
      {"id": "art", "text": "The agent produces a structured output, such as a plan or a report, as an artifact."},
      {"id": "apply", "text": "A controlled step applies only the operations that the workflow allows."},
      {"id": "direct", "text": "The agent sends its proposal directly to the next agent, without an artifact."},
      {"id": "write", "text": "The agent receives write permissions so that it can apply its own proposal."},
  ],
  answer=["run", "art", "apply"],
  explanation="Artifact-based coordination separates reasoning from writing. The agent runs with restricted permissions and produces a structured output as an artifact. A controlled step then applies only what the workflow allows. Direct agent-to-agent communication leaves no evidence, and write permissions for the agent remove the boundary.",
  takeaway="Restricted agent → structured artifact → controlled step that writes.",
  evidence=[lq("run an agent with restricted permissions,", "M4U3"),
            lq("produce a structured output (plan/report/proposal) as an artifact, and then", "M4U3"),
            lq("use a controlled step to apply only the operations your workflow allows.", "M4U3"),
            lq("This pattern creates an explicit boundary between \"reasoning\" and \"writing,\" and it leaves evidence that reviewers can inspect.", "M4U3")]),

Q("x2-d5-incompatible-fixes", "single", "D5", "M4U5", "apply",
  stem="In a GitHub repository named Repo1, a security agent and a dependency agent each open a pull request for the same code scanning alert. One pull request upgrades the affected library, and the other replaces the library. Both pull requests pass the required checks, and the two fixes cannot be combined.\n\n"
       "You need to resolve the situation in a predictable way. What should occur next?",
  options=[
      opt("a", "The pull request that passed its checks first is merged, and the other one is closed.", "Incorrect. The outcome would be decided by timing, not by correctness."),
      opt("b", "Both agents rebase their branches until one of the pull requests has no conflicts.", "Incorrect. The fixes are incompatible by design. More automated attempts cannot decide between them."),
      opt("c", "Automation stops, and a human receives a short report of the conflict, the attempts, and the options.", "Correct. Two incompatible fixes for the same alert are an escalation threshold. A person decides, with the facts in hand."),
      opt("d", "Both pull requests are merged, and the resulting conflict is resolved on `main`.", "Incorrect. That moves the conflict into the protected branch, where it affects everyone."),
  ],
  answer=["c"],
  explanation="This is duplicate effort that ended in contradictory outputs. The module defines escalation thresholds so that automation stops before it creates instability: a pull request that conflicts twice after rebasing, a required check that fails twice with the same signature, or two agents that propose incompatible fixes to the same alert. The escalation includes a short report.",
  takeaway="Incompatible fixes for one alert → stop and escalate with what conflicted, what was attempted, and the options.",
  evidence=[lq("if two agents propose incompatible fixes to the same alert.", "M4U5"),
            lq("Escalation should include a short report: what conflicted, what was attempted, and which options exist.", "M4U5"),
            lq("Without arbitration rules, whichever pull request merges first becomes the \"winner,\" which encourages instability and forces reviewers to untangle the system after the fact.", "M4U5")]),

Q("x2-d5-pr-sections", "match", "D5", "M4U6", "apply",
  stem="The agents in a GitHub repository named Repo1 use a pull request structure that has the following sections.\n\n"
       "```md\n## Objective\n## Plan\n## Evidence\n## Decisions and handoffs\n## Risks and rollback\n```\n\n"
       "Which section should contain each item?",
  choices=[{"id": "obj", "text": "Objective"}, {"id": "plan", "text": "Plan"}, {"id": "ev", "text": "Evidence"},
           {"id": "dec", "text": "Decisions and handoffs"}, {"id": "risk", "text": "Risks and rollback"}],
  targets=[
      {"id": "t1", "text": "The link to the CI run and the scan outputs", "answer": "ev",
       "rationale": "Runs and scan outputs are what a reviewer inspects to verify the result."},
      {"id": "t2", "text": "The next owner when an escalation is needed", "answer": "dec",
       "rationale": "A handoff names who continues. It is recorded with the decision that led to it."},
      {"id": "t3", "text": "The problem that the pull request solves", "answer": "obj",
       "rationale": "The objective states the problem, before any step is described."},
      {"id": "t4", "text": "The rationale for choosing one approach over another", "answer": "dec",
       "rationale": "A decision is recorded together with its rationale, so that a later agent or reviewer does not reopen it."},
  ],
  explanation="A standard structure keeps handoffs consistent across agents. The objective states the problem, the plan lists the steps, the evidence links the CI run, the scan outputs and the related issue or alert, the decisions and handoffs section records each decision with its rationale and the next owner, and the last section holds the risks and the rollback.",
  takeaway="Decision, rationale and next owner go in Decisions and handoffs. Runs and scans go in Evidence.",
  evidence=[lq("What problem is being solved?", "M4U6"),
            lq("Next owner (if escalation needed):", "M4U6"),
            lq("Rationale:", "M4U6"),
            lq("This structure ensures that every decision is captured, every action is justified, and every handoff is clear.", "M4U6")]),

Q("x2-d5-add-agent", "multiple", "D5", "M4U4", "apply", also_units=["M4U2"], select=2,
  stem="A GitHub repository named Repo1 has a dependency agent and a refactoring agent. Each agent has its own workflow and its own branch prefix. You plan to add a test agent that writes unit tests in `tests/`.\n\n"
       "You need to add the test agent without creating interference with the existing agents. Which two actions should you perform? " + PART,
  options=[
      opt("a", "Give the test agent a dedicated branch prefix, such as `agent/test/<ticket>`.", "Correct. A branch for each agent keeps its changes bounded and its ownership clear."),
      opt("b", "Let the test agent push its commits to the open branches of the refactoring agent.", "Incorrect. Shared branches interleave commits and make ownership, rollback and auditing harder."),
      opt("c", "Give the test agent a dedicated workflow that has only the permissions that the agent needs.", "Correct. Separate workflows keep triggers, permissions and outputs easy to reason about."),
      opt("d", "Reuse the workflow of the dependency agent, and add the permissions that the test agent needs.", "Incorrect. That couples the two agents and widens the permissions of both."),
      opt("e", "Allow the test agent to change `src/` so that it can fix the code that its tests cover.", "Incorrect. `src/` is the scope of the refactoring agent. Overlapping scopes produce collisions."),
  ],
  answer=["a", "c"],
  explanation="A new agent joins an existing system through the same isolation rules as the others: a narrow role, a scope that is limited by path, a dedicated branch, and a dedicated workflow or job with its own minimal permissions. Each of these prevents one kind of interference: overlapping changes, interleaved commits, or shared permissions.",
  takeaway="New agent: its own role, paths, branch prefix, and workflow with minimal permissions.",
  evidence=[lq("Each agent should open a PR from a dedicated branch such as:", "M4U4"),
            lq("Give each agent a dedicated workflow (or a dedicated job with distinct permissions) so triggers, permissions, and outputs are easy to reason about.", "M4U4"),
            lq("A strong design prevents these outcomes by assigning each agent a narrow role, limiting scope by path and artifact type, and defining completion signals that can be verified through GitHub checks and review outcomes.", "M4U2")]),

Q("x2-d5-retire-agent", "single", "D5", "M6U7", "evaluate", also_units=["M4U6"], docs=["custom-agents"],
  stem="A GitHub repository named Repo1 has a documentation agent that is defined by an agent profile and a dedicated workflow. The agent has two open pull requests and many merged pull requests. The team decides to retire the agent. Auditors must still be able to reconstruct what the agent did, and the other agents must continue to work.\n\n"
       "You need to retire the agent. What should you do?",
  options=[
      opt("a", "Remove the agent profile and the workflow in a reviewed pull request, and assign an owner to the two open pull requests.", "Correct. The retirement itself leaves a trace, the history of the agent stays in the repository, and the unfinished work gets a clear owner."),
      opt("b", "Delete the agent's branches, workflow runs, and artifacts, and then remove the agent profile.", "Incorrect. That destroys the evidence that the auditors need, and deleted artifacts cannot be restored."),
      opt("c", "Set `user-invocable: false` in the agent profile, and leave the workflow enabled.", "Incorrect. The agent can then no longer be selected by a user, but it can still be accessed programmatically, and its workflow keeps running. It is hidden, not retired."),
      opt("d", "Remove the agent profile by pushing directly to `main`, and close the open pull requests without a comment.", "Incorrect. A direct push bypasses review, and pull requests that are closed without a reason leave the outcome of the work unclear."),
  ],
  answer=["a"],
  explanation="Retirement is the last stage of the agent lifecycle, and it follows the same rules as every other change: it goes through a pull request, it leaves a durable trace, and ownership is explicit. The merged pull requests, the workflow runs and the Git history remain as the audit trail. The module names the lifecycle stages but gives no procedure, so this answer applies its principles.",
  takeaway="Retire an agent through a reviewed pull request, keep its history, and give its open work an owner.",
  evidence=[lq("Agent lifecycle management follows a continuous sequence of deployment, monitoring, updating, and eventual retirement.", "M6U7"),
            lq("A practical observability goal is that every meaningful step leaves a durable trace in GitHub:", "M4U6"),
            dq("When `false`, the agent cannot be manually selected and can only be accessed programmatically.", "custom-agents")]),

Q("x2-d5-agent-versioning", "single", "D5", "M6U7", "analyse", docs=["custom-agents"],
  stem="A custom agent named `implementer` is defined by an agent profile on the `main` branch of a GitHub repository named Repo1. The agent created three pull requests that are still open, and reviewers continue to interact with the agent in those pull requests. You merge a change to the agent profile that removes the `execute` tool.\n\n"
       "You need to plan the rollout of the change. Which behavior should you expect?",
  options=[
      opt("a", "All sessions, including the interactions in the three open pull requests, use the updated profile immediately.", "Incorrect. The interactions in a pull request keep the version of the agent that created the pull request."),
      opt("b", "The three open pull requests are closed, because the version of the agent that created them no longer exists.", "Incorrect. Updating a profile does not close pull requests. Every version remains in the Git history."),
      opt("c", "The updated profile is used only after the agent is removed and added again in the settings of Repo1.", "Incorrect. The profile is a file in the repository. A new task picks up its latest version without any other step."),
      opt("d", "New tasks use the updated profile, and the interactions in the three open pull requests keep the earlier version.", "Correct. The version of a custom agent is the commit SHA of its profile. A new task uses the latest version, and a pull request stays with the version that created it."),
  ],
  answer=["d"],
  explanation="Custom agents are versioned by the Git commit SHA of the agent profile. A task that is assigned to the agent uses the latest version of the profile for that repository and branch. Interactions within a pull request that the agent created keep the same version, for consistency. An update therefore does not disrupt active work, and it also does not reach it: to apply the stricter tools to the open pull requests, start new tasks.",
  takeaway="Agent profile update: new tasks get it, open pull requests keep the version that created them.",
  evidence=[lq("Agent lifecycle management follows a continuous sequence of deployment, monitoring, updating, and eventual retirement.", "M6U7"),
            dn("Custom agent versioning is based on Git commit SHAs for the agent profile file. When you assign a custom agent to a task, the agent is instantiated using the latest version of the agent profile for that repository and branch. When the agent creates a pull request, interactions within the pull request use the same version of the custom agent for consistency.", "custom-agents")]),
]
