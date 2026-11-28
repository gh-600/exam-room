"""Domain 3 · Memory, state and execution (Learn module 5, units 2-4). Seven screens: one series of three and four standalone questions."""
from lib import Q, opt, lq, dq, dn

QUESTIONS = [

Q("x2-d3-stale-series", "yesno", "D3", "M5U4", "evaluate", docs=["rules", "rerun"],
  scenario="You have a GitHub repository named Repo1. A ruleset for `main` requires a pull request and a status check named `build`. In the ruleset, **Require branches to be up to date before merging** is not selected. An agent opened a pull request last week, and `build` passed at that time. Since then, several other pull requests have been merged into `main`.\n\n"
           "You need to ensure that the agent's pull request can be merged only if `build` passed with the latest changes of `main`.",
  items=[
      {"id": "s1", "solution": "In the ruleset, you select **Require branches to be up to date before merging**.", "answer": "yes",
       "explanation": "The required check becomes strict. The pull request branch must be brought up to date with `main`, which adds a commit, and `build` must pass on that commit before merging."},
      {"id": "s2", "solution": "You re-run all jobs of the workflow run that reported `build` for the pull request.", "answer": "no",
       "explanation": "A re-run uses the same commit SHA and the same Git ref as the original run. It validates the code of last week again, not the code that includes the latest changes of `main`."},
      {"id": "s3", "solution": "You add a `concurrency` group with `cancel-in-progress: true` to the workflow that reports `build`.", "answer": "no",
       "explanation": "A concurrency group controls runs that overlap in time. It does not require the branch to contain the latest changes of `main`."},
  ],
  explanation="A pull request that is behind its base branch carries stale context: its check results describe code that no longer exists on `main`. A strict required status check prevents this, because the branch must be up to date before merging and the check must pass on the updated branch. Running the old run again repeats the old validation.",
  takeaway="Stale check results: require branches to be up to date before merging. A re-run uses the same commit as before.",
  evidence=[lq("A pull request is outdated compared to the base branch", "M5U4"),
            lq("GitHub enforces some of this automatically through features like required status checks and branch protection rules, which may require branches to be up to date before merging.", "M5U4"),
            dq("The topic branch must be up to date with the base branch before merging.", "rules"),
            dq("The workflow will also use the same `GITHUB_SHA` (commit SHA) and `GITHUB_REF` (git ref) of the original event that triggered the workflow run.", "rerun")]),

Q("x2-d3-scope-memory", "single", "D3", "M5U2", "apply",
  stem="An agent works on a long task in a GitHub repository named Repo1. The pull request description now contains the acceptance criteria, the design decisions, the testing approach, a list of every command that the agent tried, and two older copies of the acceptance criteria. In a new session, the agent implements one of the older copies.\n\n"
       "You need to scope the agent's memory to the information that affects the outcome of the task.\n\n"
       "What should you do?",
  options=[
      opt("a", "Keep the criteria, the decisions, and the testing approach, and remove the command list and the older copies.", "Correct. Requirements, decisions that affect the implementation, and the validation approach are relevant. Intermediate steps and duplicated context are not."),
      opt("b", "Move the entire description to a file in the repository, and link the file from the pull request.", "Incorrect. The same clutter and the same duplicates would exist in another place."),
      opt("c", "Keep everything, and add a note that tells the agent which copy of the criteria is current.", "Incorrect. The duplicates remain, and so does the risk that an outdated copy is used."),
      opt("d", "Remove the acceptance criteria from the description, and restate them in the prompt of each session.", "Incorrect. A prompt is session context. Restating criteria in prompts creates new copies that can diverge."),
  ],
  answer=["a"],
  explanation="Memory should be limited to what affects the outcome: requirements and constraints, decisions that affect the implementation, and the validation approach. Temporary intermediate steps and duplicated context should not be stored. Less memory means less confusion and a lower chance that outdated information is used.",
  takeaway="Store requirements, decisions and the validation approach. Drop intermediate steps and duplicates.",
  evidence=[lq("Memory should be limited to information that affects the outcome of the task.", "M5U2"),
            lq("Information that does not affect the outcome should not be stored. This includes temporary intermediate steps or duplicated context.", "M5U2"),
            lq("Limiting memory reduces confusion and helps prevent the use of outdated information.", "M5U2")]),

Q("x2-d3-durable-progress", "build", "D3", "M5U3", "apply",
  stem="You are setting up a task for an agent in a GitHub repository named Repo1. The progress of the task must be captured as durable state from the start.\n\n"
       "Which four actions should be performed in sequence?",
  items=[
      {"id": "issue", "text": "An issue that contains clear acceptance criteria is created."},
      {"id": "assign", "text": "The issue is assigned to the agent."},
      {"id": "pr", "text": "The agent creates a branch and opens a pull request."},
      {"id": "runs", "text": "Workflows run on each push and record the validation results."},
      {"id": "prompt", "text": "The acceptance criteria are pasted into the first prompt of the agent session."},
      {"id": "session", "text": "The agent keeps a list of the completed steps in its session context."},
  ],
  answer=["issue", "assign", "pr", "runs"],
  explanation="State is captured in GitHub artifacts. The issue holds the requirements before any work starts, the pull request tracks the implementation, the commits show incremental progress, and the workflow runs record the validation results. A prompt and the session context are not preserved across sessions, so they are not durable state.",
  takeaway="Issue → assignment → branch and pull request → workflow runs on each push.",
  evidence=[lq("Create an issue with clear acceptance criteria", "M5U3"),
            lq("Assign the task to an agent", "M5U3"),
            lq("Have the agent create a branch and open a pull request", "M5U3"),
            lq("Let workflows run on each push to validate changes", "M5U3")]),

Q("x2-d3-memory-types", "match", "D3", "M5U2", "understand",
  stem="You are classifying the information that an agent uses for its tasks in a GitHub repository named Repo1.\n\n"
       "Which type of memory does each item represent?",
  choices=[{"id": "short", "text": "Short-term memory"}, {"id": "long", "text": "Long-term memory"}, {"id": "ext", "text": "External memory"}],
  targets=[
      {"id": "t1", "text": "The review feedback that the agent received earlier in the current session", "answer": "short",
       "rationale": "Recent instructions and feedback are the working context of the current task. They are not preserved across sessions."},
      {"id": "t2", "text": "The issue that holds the acceptance criteria of the task", "answer": "ext",
       "rationale": "An issue is stored outside the agent in a durable system, and it can be reviewed at any time."},
      {"id": "t3", "text": "A curated summary of key decisions and patterns that is reused across tasks", "answer": "long",
       "rationale": "Curated knowledge that is reused across tasks is long-term memory."},
      {"id": "t4", "text": "The workflow outputs that record the results of validation", "answer": "ext",
       "rationale": "Workflow outputs are durable GitHub artifacts, which makes them external memory."},
  ],
  explanation="Short-term memory is the working context of the current task. Long-term memory is curated knowledge that is reused across tasks. External memory is stored outside the agent in durable systems such as issues, pull requests, documentation and workflow outputs, and it acts as the source of truth.",
  takeaway="Short-term = this session. Long-term = curated and reused. External = durable GitHub artifacts, the source of truth.",
  evidence=[lq("Short-term memory is the working context for the current task. It includes recent instructions, feedback, and the immediate steps needed to proceed.", "M5U2"),
            lq("Long-term memory contains curated knowledge that can be reused across tasks.", "M5U2"),
            lq("External memory is stored outside the agent in durable systems. In GitHub, this includes artifacts such as issues, pull requests, documentation, and workflow outputs.", "M5U2")]),

Q("x2-d3-summarize", "single", "D3", "M5U3", "apply",
  stem="An agent's pull request in a GitHub repository named Repo1 has more than 100 comments, many of which contain pasted logs. The requirements and the approach have not changed. New agent sessions overlook the final decisions, which are spread over the comments.\n\n"
       "You need to keep the history manageable and preserve traceability.\n\n"
       "What should you do?",
  options=[
      opt("a", "Close the pull request, and open a new pull request for the same branch.", "Incorrect. That is a reset, which is used when the requirements or the approach change. Nothing changed here."),
      opt("b", "Delete the workflow runs and the artifacts that the pasted logs came from.", "Incorrect. That is pruning of evidence that is still needed, and deleted artifacts cannot be restored."),
      opt("c", "Update the description with the final decisions, and link to the workflow runs instead of pasting logs.", "Correct. This is summarization: the description carries the decisions, and links keep the full evidence reachable."),
      opt("d", "Increase the retention period for workflow logs and artifacts in Repo1.", "Incorrect. Retention decides how long evidence is kept. It does not make the decisions easier to find."),
  ],
  answer=["c"],
  explanation="The module names four ways to maintain memory: expiration, pruning, summarization and reset. When the detailed history is too long but still valid, the answer is summarization. The pull request description holds the final decisions, key commits are referenced, and workflow runs are linked, not copied.",
  takeaway="Long but valid history → summarize in the description and link to the evidence.",
  evidence=[lq("Update the pull request description with final decisions", "M5U3"),
            lq("Link to workflow runs instead of storing full logs", "M5U3"),
            lq("This preserves traceability while keeping memory manageable.", "M5U3")]),
]
