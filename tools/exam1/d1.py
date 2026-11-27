"""Domain 1 · Agent architecture and SDLC integration (Learn modules 1 and 2). Eight standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO, PART

QUESTIONS = [

Q("x1-d1-plan-first", "single", "D1", "M2U4", "apply",
  stem="An agent will change the authentication flow of a production service in a GitHub repository named Repo1. The change is difficult to reverse.\n\n"
       "You need to ensure that the reviewers agree on the intent of the change before any code is generated. Which workflow should you use?",
  options=[
      opt("a", "A plan-first workflow, in which the agent opens a pull request that contains only the plan", "Correct. People validate the intent before any code is written, which is the approach for high-risk changes that are difficult to reverse."),
      opt("b", "A plan and execution workflow, in which the plan and the first commits are in the same pull request", "Incorrect. Code is generated at once, so the intent is validated only together with the changes. That suits low-risk, reversible work."),
      opt("c", "A workflow in which the agent pushes to `main` and records the plan in the commit message", "Incorrect. A direct push skips the pull request, which is where the plan and the change are reviewed."),
      opt("d", "A workflow in which the agent implements the change and a reviewer writes the plan afterwards", "Incorrect. A plan written after the change can't be used to validate intent before the change."),
  ],
  answer=["a"],
  explanation="Both workflows are reviewed before merge. They differ in when a person validates the work relative to the code. Plan-first puts that validation before any code exists, which reduces early exposure for high-risk work such as authentication, infrastructure, workflows and production.",
  takeaway="High risk or hard to reverse → plan-first. Low risk and reversible → plan and execution.",
  evidence=[lq("The agent opens a pull request that contains only the plan (no code changes yet).", "M2U4"),
            lq("Use plan-first for high-risk work (workflows, infra, auth, production).", "M2U4"),
            lq("changes are high-risk or difficult to reverse", "M2U4")]),

Q("x1-d1-read-only-planner", "single", "D1", "M2U4", "analyse",
  stem="You configure a planning agent. The agent's instructions contain the following text: \"Do not edit files. Produce a plan only.\" During a planning session, the agent modifies two source files.\n\n"
       "You need to guarantee that the planning agent cannot modify files. What should you do?",
  options=[
      opt("a", "Repeat the instruction at the start and at the end of the agent's instructions.", "Incorrect. An instruction is still guidance, however often it is repeated. The model can fail to follow it."),
      opt("b", "Add a required Plan section to the pull request template.", "Incorrect. A template makes the plan visible. It doesn't take away the agent's ability to edit files."),
      opt("c", "Ask the reviewers to reject every plan that is delivered together with code changes.", "Incorrect. That detects the edit after it happened and depends on people noticing it."),
      opt("d", "Limit the planning agent to read-only tools.", "Correct. Without a tool that can write, the agent has no way to modify a file, whatever it decides to do."),
  ],
  answer=["d"],
  explanation="This is the difference between guidance and enforcement. An instruction asks the agent to behave in a certain way. A capability boundary removes the ability: a planning agent that only has read-only tools cannot change files.",
  takeaway="Instructions are guidance. Tool allowlists and gates are enforcement.",
  evidence=[lq("A planning agent should be limited to read-only tools so it cannot modify files during planning.", "M2U4"),
            lq("Treat \"instructions not to edit\" as guidance; treat tool allowlists and gates as enforcement.", "M2U4")]),

Q("x1-d1-control-plane-statements", "statements", "D1", "M1U4", "understand", docs=["control-deployments"],
  stem="You are describing how GitHub acts as the control plane for the work of agents.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "CODEOWNERS routes review requests based on the paths that a pull request changes.", "answer": "yes",
       "explanation": "CODEOWNERS maps paths to owners, and the owners are requested as reviewers when those paths change."},
      {"id": "s2", "statement": "A job that targets an environment with required reviewers starts immediately and requests approval after it finishes.", "answer": "no",
       "explanation": "The job waits. It starts only after a required reviewer approves, which is what protects the environment's secrets."},
      {"id": "s3", "statement": "Required status checks turn evaluation into a policy that is enforced before merging.", "answer": "yes",
       "explanation": "A required check must pass before the merge, so the evidence from CI becomes a condition and not just information."},
  ],
  explanation="GitHub is the control plane because it has enforcement points that shape what an agent's contribution can do: pull requests, required reviews, required status checks, CODEOWNERS, rulesets and environments. Each one enforces something specific, and each has to be turned on.",
  takeaway="CODEOWNERS routes, required checks enforce evidence, environments hold a job until approval.",
  evidence=[lq("If a workflow job targets an environment with required reviewers, the job waits until approval is granted.", "M1U4"),
            lq("The supervision model works everywhere; enforcement requires the controls to be turned on.", "M1U4"),
            dq("Jobs that reference an environment configured with required reviewers will wait for an approval before starting.", "control-deployments")]),

Q("x1-d1-job-outputs", "dropdown", "D1", "M2U6", "apply", docs=["job-outputs"],
  stem="You are building a workflow in which a job named `plan` generates a plan and a job named `implement` uses it.\n\n"
       "You need to pass the plan from the `plan` job to the `implement` job as a structured value.\n\n"
       "How should you complete the workflow?",
  template="jobs:\n  plan:\n    runs-on: ubuntu-latest\n    outputs:\n      plan: ${{ steps.generate_plan.outputs.plan }}\n    steps:\n      - id: generate_plan\n        run: echo \"plan=...\" >> \"[[file]]\"\n\n"
           "  implement:\n    runs-on: ubuntu-latest\n    [[dep]]: plan\n    steps:\n      - run: echo \"Using plan: ${{ [[expr]] }}\"\n",
  blanks={
      "file": {"options": ["$GITHUB_ENV", "$GITHUB_OUTPUT", "$GITHUB_STEP_SUMMARY"], "answer": "$GITHUB_OUTPUT",
               "rationale": "A step sets an output by writing `name=value` to `$GITHUB_OUTPUT`. `$GITHUB_ENV` sets an environment variable for later steps of the same job, and `$GITHUB_STEP_SUMMARY` writes the run summary."},
      "dep": {"options": ["if", "needs", "uses"], "answer": "needs",
              "rationale": "`needs` makes `implement` depend on `plan`, which orders the jobs and gives access to the outputs of `plan`."},
      "expr": {"options": ["env.plan", "needs.plan.outputs.plan", "steps.generate_plan.outputs.plan"], "answer": "needs.plan.outputs.plan",
               "rationale": "A dependent job reads a job output through the `needs` context. The `steps` context only reaches steps of the same job."},
  },
  explanation="Data moves through a workflow in two stages. A step writes an output to `$GITHUB_OUTPUT`, and the job publishes it under `outputs`. Another job declares `needs` and reads the value from `needs.<job>.outputs.<name>`. Environment variables configure a job and aren't a substitute for this.",
  takeaway="Step output → job `outputs` → `needs.<job>.outputs.<name>` in the dependent job.",
  evidence=[lq("Step outputs pass values between steps in the same job.", "M2U6"),
            lq("Job outputs pass values across jobs (through job dependencies).", "M2U6"),
            lq("Environment variables configure runtime behavior but shouldn't replace outputs for structured data flow.", "M2U6")]),

Q("x1-d1-critical-tier", "single", "D1", "M2U6", "apply", docs=["environments"],
  stem="You are defining a risk-based autonomy model for an agent in a GitHub repository named Repo1. One class of tasks changes production deployment settings and uses production secrets.\n\n"
       "You need to ensure that the agent cannot run the deployment itself, and that the production secrets are released to a job only after a person approves.\n\n"
       "Which autonomy design should you apply to this class of tasks?",
  options=[
      opt("a", "Automatic merge after the required checks pass", "Incorrect. That is the design for low-risk work such as documentation and formatting."),
      opt("b", "A pull request with required checks and at least one review", "Incorrect. That is the design for medium-risk work. It gates the merge, not the deployment or the secrets."),
      opt("c", "Environment approvals, where the agent prepares the change but cannot execute it", "Correct. A job that targets a protected environment waits for approval, and the environment's secrets aren't available before that."),
      opt("d", "CODEOWNERS review with multiple reviews and stricter rulesets", "Incorrect. That is the design for high-risk paths such as `infra/`. It controls who approves a merge, not access to secrets."),
  ],
  answer=["c"],
  explanation="Autonomy is designed per risk level. Critical work, such as production deployments and secrets, is controlled at the point of execution: the job targets an environment with required reviewers, so it pauses until a person approves, and only then can it read the environment's secrets. The agent prepares the change and can't carry it out.",
  takeaway="Critical risk → environment approvals: the agent prepares, a person releases.",
  evidence=[lq("If an environment is configured with required reviewers, a job targeting that environment will pause until approval is granted.", "M2U6"),
            lq("This design allows the agent to prepare changes while preventing it from executing production-impacting actions independently.", "M2U6"),
            dq("Secrets stored in an environment are only available to workflow jobs that reference the environment. If the environment requires approval, a job cannot access environment secrets until one of the required reviewers approves it.", "environments")]),

Q("x1-d1-evidence", "multiple", "D1", "M2U7", "apply", select=2,
  stem="An agent's pull request in a GitHub repository named Repo1 passes all checks and is merged. One week later, an auditor asks which workflow run produced the test report and against which commit. The report was written only to the job log.\n\n"
       "You need to make the evidence durable and traceable for future pull requests. Which two actions should you perform? " + PART,
  options=[
      opt("a", "Upload the test report as a workflow artifact.", "Correct. An artifact keeps the report as a file that belongs to the run, instead of text inside a log."),
      opt("b", "Link the workflow run and its artifacts in an Evidence section of the pull request.", "Correct. The link ties the evidence to a specific run, and the run is tied to a specific commit."),
      opt("c", "Commit the generated test report to the pull request branch.", "Incorrect. Generated files don't belong in the repository. Artifacts keep outputs inspectable without committing them."),
      opt("d", "Ask the agent to summarize the test results in a pull request comment.", "Incorrect. A summary is the agent's account of the results, not the evidence itself."),
      opt("e", "Increase the level of detail of the job log.", "Incorrect. More log text doesn't make the report a durable file or link it to the pull request."),
  ],
  answer=["a", "b"],
  explanation="Observability means that every meaningful action leaves an artifact that someone can inspect later. Uploading the report makes it durable, and linking the run and the artifact from the pull request makes it traceable: which run produced it, and against which code state.",
  takeaway="Upload evidence as artifacts, and link the run from the pull request.",
  evidence=[lq("Uploading artifacts makes evidence durable and reviewable, even when logs scroll away.", "M2U7"),
            lq("Evidence should be traceable to a specific workflow run and a specific commit.", "M2U7"),
            lq("This keeps outputs inspectable and usable without committing generated files back to the repo.", "M2U7")]),

Q("x1-d1-plan-first-sequence", "build", "D1", "M2U4", "apply",
  stem="You are implementing a plan-first workflow for high-risk changes that an agent makes in a GitHub repository named Repo1.\n\nWhich four actions should be performed in sequence?",
  items=[
      {"id": "gen", "text": "A plan is generated for the task, for example by assigning the issue to the agent."},
      {"id": "pr", "text": "The agent opens a pull request that contains only the plan."},
      {"id": "approve", "text": "The reviewers discuss, refine, and approve the plan in the pull request."},
      {"id": "impl", "text": "The agent implements the plan in follow-up commits or in a new pull request."},
      {"id": "both", "text": "The agent opens a pull request that contains the plan and the initial code changes."},
      {"id": "self", "text": "The agent approves the plan and merges the pull request."},
  ],
  answer=["gen", "pr", "approve", "impl"],
  explanation="In a plan-first workflow, the plan is complete and approved before any code is introduced: generate the plan, open a pull request with only the plan, let the reviewers approve it, and only then implement. A pull request that already contains code is the plan and execution workflow.",
  takeaway="Plan → plan-only pull request → approval → implementation.",
  evidence=[lq("Reviewers discuss, refine, and approve the plan directly in the PR.", "M2U4"),
            lq("After approval, the agent proceeds to implement the plan in follow-up commits or a new PR.", "M2U4"),
            lq("Human validation happens before any code is written.", "M2U4")]),

Q("x1-d1-defensive-gating", "single", "D1", "M2U6", "apply", docs=["conditions"],
  stem="A workflow named `PR Validation` is triggered by `pull_request` and by `workflow_dispatch`. One of its jobs posts a comment on the pull request. When a developer starts the workflow manually, that job fails, because the run isn't associated with a pull request.\n\n"
       "You need to ensure that the job runs only when the workflow is triggered by a pull request. Manual runs must remain possible for the other jobs.\n\n"
       "What should you add to the job?",
  options=[
      opt("a", "`if: github.ref == 'refs/heads/main'`", "Incorrect. This tests the branch of the run, not the event. A manual run from `main` would still start the job."),
      opt("b", "`if: github.event_name == 'pull_request'`", "Correct. The `github` context holds the event that triggered the run, so the job is skipped for any other event."),
      opt("c", "`if: vars.RUN_MODE == 'pull_request'`", "Incorrect. `vars` holds configuration values that are managed centrally. It doesn't say what triggered this run."),
      opt("d", "`if: github.actor != 'github-actions[bot]'`", "Incorrect. This tests who started the run. A developer who starts it manually would still start the job."),
  ],
  answer=["b"],
  explanation="A workflow can have several triggers, so behavior that depends on a pull request needs its own guard. A job-level `if` on `github.event_name` is that guard. The other jobs don't have the condition, so they still run when the workflow is started manually.",
  takeaway="Behavior that needs a pull request → `if: github.event_name == 'pull_request'` on the job.",
  evidence=[lq("You can prevent this by adding a job-level condition that ensures the workflow only runs when it's associated with a pull request.", "M2U6"),
            lq("github.* → event metadata and runtime decisions (\"what triggered this run?\")", "M2U6"),
            lq("vars.* → centrally managed configuration values designed to be reused", "M2U6")]),
]
