"""Domain 3 · Memory, state and continuity (Learn module 5, units 2-4). Seven screens."""
from lib import Q, opt, lq, dq, dn, YESNO

QUESTIONS = [

Q("x1-d3-source-of-truth", "match", "D3", "M5U4", "apply", also_units=["M5U2"],
  stem="An agent works on tasks in a GitHub repository named Repo1 from an IDE, from the CLI, and in a GitHub-hosted environment. You are defining a single source of truth for each type of information.\n\n"
       "Where should you store each type of information?",
  choices=[{"id": "issue", "text": "Issue"}, {"id": "pr", "text": "Pull request"},
           {"id": "instr", "text": "Repository instructions"}, {"id": "runs", "text": "Workflow runs and artifacts"}],
  targets=[
      {"id": "t1", "text": "The validation rules that apply to every task in the repository", "answer": "instr",
       "rationale": "Rules that hold for every task belong in repository instructions, not in one issue or pull request."},
      {"id": "t2", "text": "The requirements that define a task before any work starts", "answer": "issue",
       "rationale": "Requirements live in the issue, which exists before a branch or pull request does."},
      {"id": "t3", "text": "The results of the tests that validated a change", "answer": "runs",
       "rationale": "Execution results are produced and kept by workflow runs and their artifacts."},
      {"id": "t4", "text": "The decisions taken and the progress made while implementing a task", "answer": "pr",
       "rationale": "The pull request gathers commits, checks and discussion, so decisions and progress are recorded there."},
  ],
  explanation="Each type of information gets one location, so every tool reads the same value. Requirements go in the issue, decisions and progress in the pull request, validation rules in repository instructions, and results in workflow runs and artifacts.",
  takeaway="Issue = requirements. Pull request = decisions and progress. Instructions = rules. Runs = results.",
  evidence=[lq("Requirements live in issues", "M5U4"), lq("Decisions and progress live in pull requests", "M5U4"),
            lq("Validation rules live in repository instructions", "M5U4"), lq("Execution results live in workflow runs and artifacts", "M5U4")]),

Q("x1-d3-resume", "single", "D3", "M5U3", "apply",
  stem="An agent started work on an issue in a GitHub repository named Repo1 and opened a pull request. The session ended before the work was complete. A new agent session must now finish the task.\n\n"
       "You need to ensure that the new session continues the work without repeating completed steps. What should the agent do first?",
  options=[
      opt("a", "Create a new branch from `main` and implement the issue again from its description.", "Incorrect. This discards the commits already made and repeats the work."),
      opt("b", "Ask the user to paste the chat history of the earlier session into the prompt.", "Incorrect. Chat history is session context. It may be incomplete, and it isn't the recorded state of the work."),
      opt("c", "Open the existing pull request and review its description, linked issue, commits, and check results.", "Correct. The pull request holds the plan, the work done and the validation results, so the agent can continue from the latest state."),
      opt("d", "Close the pull request and open a new one that references the same issue.", "Incorrect. Recreating the pull request is a reset, used when requirements or the approach change. Nothing changed here."),
  ],
  answer=["c"],
  explanation="State is stored in GitHub artifacts, not in the session. To resume, the agent opens the existing pull request, reads the description and linked issue, checks the commits and the results in the Checks tab, and continues from there.",
  takeaway="To resume, re-anchor to the pull request, never to the previous session.",
  evidence=[lq("Agent workflows may pause or move between environments. To resume work correctly, the agent should rely on stored state instead of starting over.", "M5U3"),
            lq("Because GitHub preserves commit history and workflow runs, the agent can identify completed work and avoid duplication.", "M5U3")]),

Q("x1-d3-drift", "single", "D3", "M5U3", "analyse",
  stem="An agent is implementing an issue in a GitHub repository named Repo1. The acceptance criteria require input validation for one API endpoint. After several iterations, the pull request also contains a refactoring of the logging subsystem, and the latest commits contradict a design decision that is recorded in the pull request description.\n\n"
       "You need to correct the context drift. What should the agent do first?",
  options=[
      opt("a", "Re-read the issue and the pull request description, and compare the current changes with the acceptance criteria.", "Correct. Drift is corrected by returning to the source of truth and measuring the changes against it."),
      opt("b", "Update the acceptance criteria in the issue so that they include the logging refactoring.", "Incorrect. That changes the goal to match the drift. The requirement didn't change."),
      opt("c", "Start a new session that continues from the agent's own summary of its earlier work.", "Incorrect. The agent's summary carries the same drifted context forward."),
      opt("d", "Merge the pull request and create a follow-up issue for the logging changes.", "Incorrect. That accepts changes that don't match the acceptance criteria."),
  ],
  answer=["a"],
  explanation="Two signs of drift appear here: changes that go beyond the acceptance criteria and commits that contradict an earlier decision. The correction starts by re-reading the issue and the pull request description, then comparing the changes with the criteria.",
  takeaway="Drift is corrected against the source of truth, not against the agent's own account.",
  evidence=[lq("Context drift occurs when the agent’s actions no longer align with the original goal or prior decisions.", "M5U3"),
            lq("To correct drift, the agent should be re-aligned with the source of truth.", "M5U3"),
            lq("Compare current changes with acceptance criteria", "M5U3")]),

Q("x1-d3-retention", "single", "D3", "M5U3", "apply", docs=["retention", "store-data"],
  stem="A private GitHub repository named Repo1 has a workflow that uploads test reports as workflow artifacts for an agent's pull requests. The repository uses the default retention setting, and the organization doesn't limit the retention period.\n\n"
       "An auditor requires that every report uploaded from now on is available for 180 days after the run.\n\n"
       "You need to meet the requirement. What should you do?",
  options=[
      opt("a", "Take no action. Artifacts are kept until someone deletes them.", "Incorrect. By default, artifacts and logs are deleted automatically after 90 days."),
      opt("b", "Change the visibility of Repo1 to public, and then set the retention period to 180 days.", "Incorrect. A public repository allows a retention period of 1 to 90 days only."),
      opt("c", "Add `retention-days: 180` to the upload step and keep the repository setting unchanged.", "Incorrect. The value on the step can't exceed the repository's retention limit, which is still 90 days."),
      opt("d", "Change the artifact and log retention period of Repo1 to 180 days.", "Correct. A private repository accepts a retention period of 1 to 400 days, and the new period applies to artifacts created from now on."),
  ],
  answer=["d"],
  explanation="Workflow artifacts are memory that expires. The default is 90 days. The period can be changed: up to 90 days for public repositories and up to 400 days for private ones. A change applies only to new artifacts, which is what the auditor asks for.",
  takeaway="Default 90 days. Public: 1 to 90. Private: 1 to 400. Not retroactive.",
  evidence=[lq("Public repositories typically allow 1-90 days, while private repositories can extend retention up to 400 days", "M5U3"),
            dq("By default, checks, workflow runs, commit statuses, and the artifacts and log files generated by workflows are retained for 90 days before they are automatically deleted.", "retention"),
            dq("The `retention-days` value cannot exceed the retention limit set by the repository, organization, or enterprise.", "store-data")]),

Q("x1-d3-continuity-statements", "statements", "D3", "M5U4", "understand",
  stem="An agent works on the same task from an IDE, from the CLI, and in a GitHub-hosted environment.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "Referring to the pull request number, the branch name, and commit SHAs allows each tool to retrieve the same state without transferring session context.", "answer": "yes",
       "explanation": "These are durable references. Every environment can resolve them against the same repository data."},
      {"id": "s2", "statement": "A pull request branch that is behind its base branch is a source of stale context.", "answer": "yes",
       "explanation": "The work is based on code that is no longer current, so earlier results may no longer be valid."},
      {"id": "s3", "statement": "Restating the acceptance criteria in the prompt of each tool prevents conflicting context.", "answer": "no",
       "explanation": "Copies are what cause conflicting context. Keep the criteria in the issue or pull request and update them there."},
  ],
  explanation="Continuity across tools comes from durable references and a single source of truth, not from copying context. Conflicting context is the same information in several places with different values. Stale context is outdated information used during execution.",
  takeaway="Share references, not copies. One source per type of information.",
  evidence=[lq("Agent state should be shared using durable references, not copied context.", "M5U4"),
            lq("Don't redefine acceptance criteria in multiple prompts", "M5U4"),
            lq("A pull request is outdated compared to the base branch", "M5U4")]),

Q("x1-d3-reset", "single", "D3", "M5U3", "apply",
  stem="An agent has an open pull request that implements a caching layer described in an issue. The product owner rewrites the issue: caching is no longer wanted, and the same performance problem must be solved by reducing the number of database queries.\n\n"
       "You need to prevent the agent from carrying its earlier assumptions into the new work. What should you do?",
  options=[
      opt("a", "Add the new requirement to the agent's next prompt and leave the pull request unchanged.", "Incorrect. The pull request would still describe the caching plan, so the agent would have two conflicting sources."),
      opt("b", "Rewrite the pull request description to state the new direction before the agent continues.", "Correct. This is a reset: the recorded plan is replaced, so the agent re-anchors to the new approach."),
      opt("c", "Delete the workflow artifacts that the earlier runs produced.", "Incorrect. That is pruning. It removes old outputs but leaves the caching plan in the pull request."),
      opt("d", "Add a comment that summarizes the caching work and continue with the existing plan.", "Incorrect. Summarizing keeps the history readable. It doesn't replace a plan that is no longer valid."),
  ],
  answer=["b"],
  explanation="When requirements change significantly or a new approach is chosen, memory must be reset so that old assumptions aren't carried over. In practice you update or rewrite the pull request description, or close the pull request and create a new one, and document the new direction before work continues.",
  takeaway="Requirements changed → reset: rewrite the description or recreate the pull request.",
  evidence=[lq("Requirements in the issue change significantly", "M5U3"),
            lq("Update or rewrite the pull request description", "M5U3"),
            lq("Clearly document the new direction before continuing", "M5U3")]),

Q("x1-d3-memory-vs-instructions", "single", "D3", "M5U2", "apply", docs=["memory"],
  stem="Copilot Memory holds a repository-level fact for a GitHub repository named Repo1: code must be formatted with `dotnet format` before each commit. In some sessions, GitHub Copilot cloud agent commits code without formatting it.\n\n"
       "You need to ensure that the formatting rule is provided to the agent consistently in every session. What should you do?",
  options=[
      opt("a", "Add the rule to the custom instructions of the repository.", "Correct. Custom instructions are given to the agent in every session. A stored fact is only used when Copilot judges it relevant and still accurate."),
      opt("b", "Ask Copilot to store the rule again as a user-level preference.", "Incorrect. A user-level preference describes how one person likes to work, and it is still a memory, not a guaranteed rule."),
      opt("c", "Increase the expiry period of repository-level facts.", "Incorrect. The expiry period decides how long a fact is kept without reinforcement. It doesn't make Copilot apply the fact."),
      opt("d", "Delete the fact so that Copilot learns it again from the codebase.", "Incorrect. A newly learned fact has the same status as the old one: Copilot may use it, with no guarantee."),
  ],
  answer=["a"],
  explanation="Long-term memory is curated knowledge that the agent may reuse. Before Copilot uses a repository-level fact, it checks the fact's citations against the current branch and judges whether the fact still holds. That is a judgment, not an enforced rule. A rule that must reach the agent every time belongs in repository instructions.",
  takeaway="Memory = facts Copilot may use. Instructions = rules given every time.",
  evidence=[lq("Validation rules → Repository instructions", "M5U2"),
            lq("Repeatable processes should be stored as instructions or reusable skills. This avoids redefining the same workflow for every task.", "M5U2"),
            dn("When Copilot finds a repository-level fact relevant to its current work, it checks the fact's citations against the current branch to judge whether the information is still accurate. This is a judgment, not a guarantee enforced by the system, so a stored fact should not be relied on as a rule that will always be followed. To provide instructions consistently, use custom instructions.", "memory")]),
]
