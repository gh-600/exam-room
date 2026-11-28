"""Domain 1 · Agent architecture and SDLC (Learn modules 1 and 2, with module 6 unit 4 for human intervention). Eight standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO, PART

QUESTIONS = [

Q("x2-d1-task-contract", "match", "D1", "M2U3", "apply",
  stem="You are writing a task contract for an agent that remediates a vulnerable dependency in a GitHub repository named Repo1.\n\n"
       "Which part of the task contract should contain each item?",
  choices=[{"id": "in", "text": "Inputs"}, {"id": "out", "text": "Outputs"}, {"id": "ok", "text": "Success criteria"}],
  targets=[
      {"id": "t1", "text": "The link to the security alert that describes the vulnerability", "answer": "in",
       "rationale": "The alert is context that the agent needs before it starts, so it is an input."},
      {"id": "t2", "text": "A pull request that contains a structured plan, a bounded set of commits, and links to the workflow run", "answer": "out",
       "rationale": "The plan, the pull request and the evidence are what the agent produces."},
      {"id": "t3", "text": "The vulnerable version is no longer in use, and the required checks pass", "answer": "ok",
       "rationale": "This states how the result is evaluated, and it reflects the real intent of the task."},
      {"id": "t4", "text": "The rule that workflow files must stay unchanged unless the platform team reviews the change", "answer": "in",
       "rationale": "A constraint is given to the agent with the task. It is an input, even though it reads like a condition for acceptance."},
  ],
  explanation="A task contract has three parts. Inputs are what the agent needs: the context of the issue, the constraints and the boundaries. Outputs are what the agent produces: the plan, the pull request and the evidence. Success criteria say how the result is evaluated. Constraints belong to the inputs, which is the item that is easiest to misplace.",
  takeaway="Inputs = context, constraints, boundaries. Outputs = plan, pull request, evidence. Success criteria = how the result is evaluated.",
  evidence=[lq("Inputs: what the agent needs (issue context, constraints, boundaries).", "M2U3"),
            lq("Outputs: what the agent produces (plan + PR + evidence).", "M2U3"),
            lq("Success criteria: how results are evaluated (checks, scans, review outcomes).", "M2U3"),
            lq("Constraints: no workflow changes without platform review; no secrets introduced; no direct-to-main pushes.", "M2U3")]),

Q("x2-d1-auto-merge", "single", "D1", "M2U6", "apply", also_units=["M6U4"], docs=["auto-merge"],
  stem="An agent opens pull requests in a GitHub repository named Repo1. A ruleset for `main` requires a pull request and a status check named `build`. The ruleset does not require a review. Pull requests that change only files in `docs/` wait an average of one day until a maintainer merges them.\n\n"
       "You need to remove the delay for these pull requests. The `build` check must still pass before the changes are merged.\n\n"
       "What should you do?",
  options=[
      opt("a", "Enable auto-merge for these pull requests.", "Correct. Auto-merge merges a pull request when all required reviews and status checks have passed, so nobody has to wait for the result and merge by hand."),
      opt("b", "Add the agent to the bypass list of the ruleset.", "Incorrect. A bypass actor can merge without meeting the rules, so `build` would no longer have to pass."),
      opt("c", "Remove `build` from the required status checks.", "Incorrect. The requirement says that the check must still pass before the changes are merged."),
      opt("d", "Require a code owner review for the files in `docs/`.", "Incorrect. That adds a human approval to low-risk changes and increases the delay."),
  ],
  answer=["a"],
  explanation="Human intervention belongs at decision points, not at every step. For low-risk paths such as `docs/`, the module's autonomy model automates the merge once the required checks pass. Auto-merge does exactly that, and it keeps the control: the pull request is merged only after every requirement of the ruleset is met.",
  takeaway="Low-risk changes: let auto-merge wait for the required checks. Keep people for the decisions that carry risk.",
  evidence=[lq("merge can be automated using GitHub automerge after required checks (and reviews, if configured) pass", "M2U6"),
            lq("Put humans at decision points (merge, deploy, secret access), not at every step (analysis, formatting, routine checks).", "M6U4"),
            dq("Auto-merge merges a pull request automatically after all required reviews and status checks pass.", "auto-merge")]),

Q("x2-d1-evidence-jobs", "dropdown", "D1", "M2U7", "apply", docs=["store-data"],
  stem="A workflow in a GitHub repository named Repo1 has a job named `test` that runs the tests for an agent's pull request and writes a report to `results/`. A second job named `review-gate` evaluates the report. The jobs run on different runners.\n\n"
       "You need to make the report available to `review-gate` and keep it inspectable after the run. Generated files must not be committed to the repository.\n\n"
       "How should you complete the workflow?",
  template="jobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: ./scripts/run-tests.sh\n      - uses: actions/[[up]]@v4\n        with:\n          name: test-results\n          path: results/\n\n"
           "  review-gate:\n    runs-on: ubuntu-latest\n    [[dep]]: test\n    steps:\n      - uses: actions/[[down]]@v4\n        with:\n          name: test-results\n      - run: ./scripts/check-results.sh\n",
  blanks={
      "up": {"options": ["cache", "download-artifact", "upload-artifact"], "answer": "upload-artifact",
             "rationale": "The report is uploaded in the job that produces it. It becomes an artifact of the run, which stays available after the run ends. A cache stores dependencies for reuse and is not evidence."},
      "dep": {"options": ["environment", "needs", "uses"], "answer": "needs",
              "rationale": "`needs` makes `review-gate` wait until `test` has finished, so the artifact exists when the job starts."},
      "down": {"options": ["cache", "download-artifact", "upload-artifact"], "answer": "download-artifact",
               "rationale": "The second job runs on another runner with an empty workspace, so it downloads the artifact by name."},
  },
  explanation="Evidence is uploaded where it is produced and downloaded where it is reviewed or deployed. The artifact is tied to the workflow run, so a reviewer can still open it after the run, and nothing generated is committed to the repository. A job output would carry only a string, not the files.",
  takeaway="Upload artifacts where they are produced. Download them where they are reviewed.",
  evidence=[lq("Upload artifacts where they are produced", "M2U7"),
            lq("Download them where they are reviewed or deployed", "M2U7"),
            lq("This keeps outputs inspectable and usable without committing generated files back to the repo.", "M2U7"),
            dq("You can use the `upload-artifact` and `download-artifact` actions to share data between jobs in a workflow.", "store-data")]),

Q("x2-d1-plan-elements", "multiple", "D1", "M1U3", "understand", select=3,
  stem="You are defining the plan that an agent must include in the description of each pull request in a GitHub repository named Repo1.\n\n"
       "You need to make the plans reviewable. Which three elements should each plan include? " + PART,
  options=[
      opt("a", "The scope, which states what will change.", "Correct. A reviewer can compare the scope with the files that the pull request changes."),
      opt("b", "The agent's confidence score for the change.", "Incorrect. Evaluation is grounded in system signals, not in the agent's confidence."),
      opt("c", "The success criteria, which state how the result will be verified.", "Correct. Without them, nobody can tell whether the plan worked."),
      opt("d", "The full transcript of the agent session.", "Incorrect. A transcript is raw material. A plan is a structured artifact that a reviewer can assess quickly."),
      opt("e", "A rollback or escalation path.", "Correct. It says what happens if the change fails or if the agent cannot finish."),
      opt("f", "The name of the model that the agent used.", "Incorrect. The model name does not make the approach easier to review."),
  ],
  answer=["a", "c", "e"],
  explanation="A plan is a structured, reviewable artifact, not a hidden internal state. It becomes reviewable when it states the scope, the success criteria and a rollback or escalation path. The pull request template of the next module has a field for each of them.",
  takeaway="A reviewable plan states scope, success criteria, and a rollback or escalation path.",
  evidence=[lq("Plans become more reviewable when they include scope (what will change), success criteria (how you'll know it worked), and a rollback or escalation path.", "M1U3"),
            lq("In high-quality systems, plans aren't hidden internal states. They're structured, reviewable artifacts that make the approach understandable and assessable.", "M1U3")]),

Q("x2-d1-plan-gate", "single", "D1", "M2U5", "apply",
  stem="A GitHub repository named Repo1 has the following pull request template.\n\n"
       "```md\n## Plan (required)\n- **Goal:**\n- **Scope (paths/files):**\n- **Success criteria (verifiable):**\n- **Rollback / escalation plan:**\n```\n\n"
       "Agents sometimes open pull requests in which the Plan section is empty, and reviewers approve and merge them. A ruleset for `main` requires a pull request and one approving review.\n\n"
       "You need to guarantee that a pull request cannot be merged into `main` unless it contains a plan.\n\n"
       "What should you do?",
  options=[
      opt("a", "Add a comment to the template that states that the Plan section is mandatory.", "Incorrect. A comment is a process expectation. Nothing stops a pull request that ignores it."),
      opt("b", "Add a workflow that fails when the plan is missing, and require its status check.", "Correct. A required status check turns the expectation into a condition that the platform enforces before merging."),
      opt("c", "Add an instruction to the custom instructions of Repo1 to complete the Plan section.", "Incorrect. An instruction guides the agent. It does not block a pull request in which the agent did not follow it."),
      opt("d", "Increase the number of required approving reviews in the ruleset to two.", "Incorrect. Reviewers already approve pull requests without a plan. A second approval does not check for one."),
  ],
  answer=["b"],
  explanation="A template asks for a plan, and a required status check enforces it. A workflow that fails when the plan is missing, selected as a required check in the ruleset, means that the pull request cannot be merged until the plan exists.",
  takeaway="Template = expectation. Required status check = guarantee.",
  evidence=[lq("In addition to templates, you can enforce plan gating as a required status check. This turns a process expectation (\"include a plan\") into a system guarantee.", "M2U5"),
            lq("A repository administrator can mark Plan Gate as a required status check using rulesets/branch protection, ensuring PRs can't merge unless the plan exists.", "M2U5")]),

Q("x2-d1-anti-patterns", "match", "D1", "M1U5", "apply",
  stem="You are reviewing how agents work in a GitHub organization named Org1, and you find three anti-patterns.\n\n"
       "Which mitigation should you use for each anti-pattern?",
  choices=[{"id": "tpl", "text": "A pull request template that has a required plan section, and a review before merging"},
           {"id": "lp", "text": "A least-privilege `GITHUB_TOKEN`, and environments that have required reviewers"},
           {"id": "rev", "text": "CODEOWNERS, required reviews, and risk-based approvals in addition to the checks"},
           {"id": "ret", "text": "A longer retention period for workflow logs"}],
  targets=[
      {"id": "t1", "text": "The workflow that runs an agent can write to the repository and can read every secret.", "answer": "lp",
       "rationale": "This is an over-permissioned agent. The mitigation reduces what the token can do and puts secrets behind an approval."},
      {"id": "t2", "text": "Pull requests are merged as soon as CI passes, because passing checks are taken as proof that a change is appropriate.", "answer": "rev",
       "rationale": "This is blind trust in automation. Checks only validate what they are designed to detect, so human review by the right owners is added."},
      {"id": "t3", "text": "Agents begin to change code without a visible approach.", "answer": "tpl",
       "rationale": "This is planless execution. The template makes the plan part of every pull request, and the review reads it."},
  ],
  explanation="The module maps each anti-pattern to GitHub controls. Over-permissioned agents are answered with a least-privilege token and environments. Blind trust in automation is answered by combining checks with CODEOWNERS, required reviews and risk-based approvals. Planless execution is answered with a plan section in the pull request template. Longer log retention mitigates none of the three.",
  takeaway="Over-permissioned → least privilege and environments. Blind trust → reviews next to checks. Planless → plan section in the template.",
  evidence=[lq("Over-permissioned agents: The agent (or its workflow token/tooling credentials) has broader access than necessary.", "M1U5"),
            lq("Blind trust in automation: Passing CI matters, but checks only validate what they're designed to detect.", "M1U5"),
            lq("Combine checks with CODEOWNERS, required reviews, and risk-based approvals", "M1U5"),
            lq("Require a plan section via PR template; require review before merge", "M1U5")]),

Q("x2-d1-plan-boundaries", "statements", "D1", "M2U4", "understand",
  stem="You are separating planning from execution for the agents in a GitHub repository named Repo1.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "In a plan and execution workflow, code changes can be merged before the plan has been validated.", "answer": "no",
       "explanation": "Code is generated immediately, but validation is still required before the merge. The GitHub controls are the same as in a plan-first workflow."},
      {"id": "s2", "statement": "A deliberate handoff to an implementation agent after the plan is approved keeps execution from starting during planning.", "answer": "yes",
       "explanation": "An explicit transition is one of the ways to enforce the boundary: execution occurs only after the plan is approved."},
      {"id": "s3", "statement": "In an automated orchestration, planning can run without tool execution, and the tools can be enabled only after the plan is accepted.", "answer": "yes",
       "explanation": "This is tool gating in an orchestrator. The plan is produced first, and tools become available afterwards."},
  ],
  explanation="The two workflows differ in when code is generated, not in whether it is validated. In both, nothing merges before the checks and the reviews pass. The boundary between planning and execution is enforced with capability limits: read-only planning agents, an explicit handoff, tool gating in orchestrators, and plan modes that pause before changes are applied.",
  takeaway="Both workflows validate before merge. Handoffs and tool gating enforce the planning boundary.",
  evidence=[lq("Option B (Plan + execution): Code is generated immediately, but validation is still required before merge.", "M2U4"),
            lq("Execution should occur only after plan approval, using a deliberate handoff.", "M2U4"),
            lq("you can force planning to run without tool execution and then enable tools only after the plan is accepted.", "M2U4")]),

Q("x2-d1-scope-complete", "single", "D1", "M2U2", "analyse",
  stem="A dependency remediation agent in a GitHub repository named Repo1 is scoped to the implementation stage of the SDLC. The agent detects a vulnerable dependency, creates a branch, and updates the dependency and the lock file.\n\n"
       "You need to define the last step that the agent performs before its scoped responsibility is complete. Which step should you define?",
  options=[
      opt("a", "The agent merges the branch into `main` after the required checks pass.", "Incorrect. Acceptance belongs to the reviewers and to repository policy, not to the agent."),
      opt("b", "The agent approves the pull request on behalf of the security team.", "Incorrect. Approval is human judgment. An agent that approves its own work removes the boundary."),
      opt("c", "The agent opens a pull request that includes a structured plan and the expected success signals.", "Correct. With the pull request, the implementation stage ends. Validation and acceptance happen through checks, reviews and policy."),
      opt("d", "The agent deploys the fix to production and verifies the result.", "Incorrect. Deployment is the stage that is usually restricted for agents and gated by approvals."),
  ],
  answer=["c"],
  explanation="An agent that is scoped to implementation proposes, and humans and policy accept. Its work ends when the pull request is open with a plan and the signals by which success will be judged. Merging, approving and deploying are later stages with their own controls.",
  takeaway="Scoped to implementation: the agent's last step is the pull request. Agents propose; humans and policy accept.",
  evidence=[lq("The agent opens a pull request that includes a structured plan and expected success signals.", "M2U2"),
            lq("At that point, the agent's scoped responsibility can be considered complete. Validation and acceptance happen through checks, reviews, and policy controls.", "M2U2"),
            lq("A common design boundary is: agents propose; humans and policy accept.", "M2U2")]),
]
