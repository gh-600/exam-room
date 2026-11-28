"""Domain 6 · Guardrails and accountability (Learn module 6). Seven screens: one series of three and four standalone questions."""
from lib import Q, opt, lq, dq, dn, PART

QUESTIONS = [

Q("x2-d6-hook-series", "yesno", "D6", "M6U3", "evaluate", also_units=["M2U7"], docs=["hooks-ref", "use-hooks"],
  scenario="A GitHub repository named Repo1 contains Terraform files. GitHub Copilot cloud agent works on issues in Repo1. A company policy states that agents must never run a shell command that contains `terraform destroy`.\n\n"
           "A developer writes the following hook configuration file, which is named `policy.json`. For a command that contains `terraform destroy`, the script returns a `permissionDecision` of `deny` and a reason.\n\n"
           "```json\n{\n  \"version\": 1,\n  \"hooks\": {\n    \"preToolUse\": [\n      { \"type\": \"command\", \"bash\": \"./scripts/deny-destroy.sh\" }\n    ]\n  }\n}\n```\n\n"
           "You need to guarantee that the agent cannot run such a command in its sessions for Repo1.",
  items=[
      {"id": "s1", "solution": "You add the following sentence to the custom instructions of Repo1: \"Never run terraform destroy.\" You do not use `policy.json`.", "answer": "no",
       "explanation": "An instruction is guidance for the model. Nothing blocks the command when the agent does not follow it."},
      {"id": "s2", "solution": "You commit `policy.json` to the `.github/hooks/` folder on the default branch of Repo1.", "answer": "yes",
       "explanation": "The cloud agent loads hook configuration from `.github/hooks/*.json` in the repository. The `preToolUse` hook runs before each tool call, and a decision of `deny` blocks the call."},
      {"id": "s3", "solution": "You save `policy.json` in the `~/.copilot/hooks/` folder on your computer.", "answer": "no",
       "explanation": "That is the user-level folder of Copilot CLI on one machine. The cloud agent runs in its own sandbox, which contains only the hook files of the cloned repository."},
  ],
  explanation="A policy is enforced only by a control that runs independently of the model. A `preToolUse` hook is that control: it inspects each tool call before execution and can deny it. Where the hook file is stored decides which surface it governs. For the cloud agent, the only hook configuration that exists is the one in `.github/hooks/` of the repository, and the file must be on the default branch.",
  takeaway="Blocking needs a `preToolUse` hook that denies. For the cloud agent, the hook file lives in `.github/hooks/` on the default branch.",
  evidence=[lq("Decision guidance: Use enforceable hooks for blocking. Logging and banners are helpful, but they don't prevent execution.", "M6U3"),
            lq("Hooks provide enforceable control points that operate independently of the model's reasoning. Instead of relying on instructions, they ensure that certain rules are always applied during execution.", "M2U7"),
            dq("Hook configuration is loaded from `.github/hooks/*.json` files in the cloned repository.", "hooks-ref"),
            dq("The sandbox does not ship with user-level hook files, `settings.json`, `config.json`, or installed plugins.", "hooks-ref"),
            dn("The hooks configuration file must be present on the default branch of the repository to be used by Copilot cloud agent.", "use-hooks")]),

Q("x2-d6-job-permissions", "dropdown", "D6", "M6U5", "apply", docs=["syntax"],
  stem="A workflow in a private GitHub repository named Repo1 has two jobs. The `analyze` job runs an agent that reads the code and produces a report. The `publish` job commits the report to a branch and updates the pull request.\n\n"
       "You need to configure the permissions of the `GITHUB_TOKEN`. Each job must have only the permissions that it needs.\n\n"
       "How should you complete the workflow?",
  template="permissions:\n  contents: [[default]]\n\njobs:\n  analyze:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v5\n      - run: ./scripts/analyze.sh\n\n"
           "  publish:\n    runs-on: ubuntu-latest\n    needs: analyze\n    [[key]]:\n      contents: write\n      [[scope]]: write\n    steps:\n      - uses: actions/checkout@v5\n      - run: ./scripts/publish.sh\n",
  blanks={
      "default": {"options": ["none", "read", "write"], "answer": "read",
                  "rationale": "The default for the workflow is read-only. `analyze` inherits it and can check out the code. With `none`, the job could not read the private repository, and with `write`, the agent's job could push."},
      "key": {"options": ["env", "permissions", "with"], "answer": "permissions",
              "rationale": "A `permissions` block on a job replaces the workflow default for that job only."},
      "scope": {"options": ["id-token", "pull-requests", "security-events"], "answer": "pull-requests",
                "rationale": "Updating a pull request needs `pull-requests: write`. `id-token` is for OIDC tokens, and `security-events` is for code scanning results."},
  },
  explanation="Least privilege is implemented in two steps: a read-only default at the workflow level, and an elevation only on the job that must write. The job that runs the agent never holds a token that can push. `pull-requests: write` is an elevated capability, so it appears only where the pull request is updated.",
  takeaway="Read-only default for the workflow. Write permissions only on the job that writes.",
  evidence=[lq("Set a read-only default at the workflow level, then elevate write permissions only for the job that must write.", "M6U5"),
            lq("Decision guidance: Granting pull-requests: write should be treated as elevated capability. Use it only when the workflow must create/update PRs.", "M6U5"),
            dq("If you specify the access for any of these permissions, all of those that are not specified are set to `none`.", "syntax")]),

Q("x2-d6-small-diff", "single", "D6", "M6U2", "analyse",
  stem="An agent in a GitHub repository named Repo1 rates the risk of its own plans, and low-risk plans are applied automatically. For a plan that contains the following change to `.github/workflows/ci.yml`, the agent reports a low risk, because the diff is one line.\n\n"
       "```diff\n       - name: Run tests\n-        run: dotnet test --no-build\n+        run: dotnet test --no-build || true\n```\n\n"
       "You need to classify the change correctly and apply the matching control.\n\n"
       "Which classification and control should you use?",
  options=[
      opt("a", "Low risk: full automation after the required checks pass", "Incorrect. The size of a diff says little about its consequence. This line makes the test step succeed even when tests fail."),
      opt("b", "Medium risk: a pull request and the required checks", "Incorrect. That is the control for dependency updates and safe refactoring. The change weakens the very checks that this control relies on."),
      opt("c", "High risk: a review by the code owners, explicit approvals, and stronger checks", "Correct. Changes to `.github/workflows/` are high risk by default, because they affect the entire pipeline."),
      opt("d", "Critical risk: an environment gate with explicit reviewers for each workflow run", "Incorrect. The critical level is for production deployments and access to production secrets. An environment gates jobs, not the merge of a change to a workflow file."),
  ],
  answer=["c"],
  explanation="Risk depends on where a change is applied, how easily it can be reversed, and how quickly it affects users or systems. Workflow files, `infra/` and `security/` are \"small diff, big consequence\" areas and are treated as high risk by default. The matching control is CODEOWNERS with explicit approvals and stronger checks. It also shows why an agent's own rating should not decide the routing for such paths.",
  takeaway="`.github/workflows/`, `infra/`, `security/` = high risk by default, whatever the size of the diff.",
  evidence=[lq("Treat changes to `.github/workflows/`, `infra/`, and `security/` as high risk by default. These are \"small diff, big consequence\" areas.", "M6U2"),
            lq("CODEOWNERS + explicit approvals + stronger checks", "M6U2"),
            lq("For example, editing a README file has minimal impact, while modifying `.github/workflows/` affects the entire pipeline.", "M6U2")]),

Q("x2-d6-human-judgment", "multiple", "D6", "M6U4", "apply", also_units=["M6U3"], select=2,
  stem="You are designing a human-in-the-loop workflow for an agent in a GitHub repository named Repo1. The agent searches the codebase, formats code, and runs unit tests. A workflow that the agent triggers deploys to production, and one of its jobs reads the password of the production database.\n\n"
       "You need to require human approval only where it reduces risk. Which two actions should require human approval? " + PART,
  options=[
      opt("a", "Searching the codebase", "Incorrect. Reading and searching are low-risk actions that can be automated."),
      opt("b", "Deploying to production", "Correct. A deployment is a decision point with an impact on live systems."),
      opt("c", "Formatting code", "Incorrect. Formatting is routine work. Its result is reviewed with the pull request."),
      opt("d", "Running the job that reads the password of the production database", "Correct. Access to a production secret is a decision point. A workflow that accesses production secrets is treated as critical risk and gated."),
      opt("e", "Running unit tests", "Incorrect. Routine checks produce evidence. An approval before each run would add friction without reducing risk."),
  ],
  answer=["b", "d"],
  explanation="Human oversight is placed at decision points: merge, deployment and access to secrets. Analysis, formatting and routine checks proceed automatically. Approvals at every step do not add control. They add friction, and they train reviewers to approve without looking.",
  takeaway="People decide at merge, deploy and secret access. Everything routine runs without approval.",
  evidence=[lq("Put humans at decision points (merge, deploy, secret access), not at every step (analysis, formatting, routine checks).", "M6U4"),
            lq("Decision guidance: If a workflow accesses production secrets, treat it as critical risk and gate it.", "M6U3")]),

Q("x2-d6-self-review", "single", "D6", "M6U4", "apply", docs=["environments"],
  stem="A workflow in a GitHub repository named Repo1 deploys to an environment named `production`. The environment has three required reviewers. An audit finds that one of the required reviewers started a deployment of an agent's change and then approved the same deployment.\n\n"
       "You need to ensure that the user who starts a deployment cannot approve it. What should you do?",
  options=[
      opt("a", "Add a wait timer of 30 minutes to the `production` environment.", "Incorrect. A wait timer delays the job. It does not change who may approve it."),
      opt("b", "Select **Prevent self-review** for the `production` environment.", "Correct. With this setting, a user who initiates a deployment cannot approve the deployment job, even as a required reviewer."),
      opt("c", "Increase the number of required reviewers of the environment to six.", "Incorrect. Only one of the required reviewers needs to approve a job, and that one can still be the user who started it."),
      opt("d", "Limit the deployment branches of the environment to `main`.", "Incorrect. That restricts which branches can deploy. It says nothing about who approves."),
  ],
  answer=["b"],
  explanation="A production approval must be explicit, auditable and owned by an accountable role. An approval by the person who started the deployment is not an independent decision. Environments have a setting for this case: with self-review prevented, a deployment to a protected environment is always reviewed by a second person.",
  takeaway="Independent production approval → **Prevent self-review** on the environment.",
  evidence=[lq("Decision guidance: Production approvals should be explicit, auditable, and owned by accountable roles.", "M6U4"),
            dq("If you enable this setting, users who initiate a deployment cannot approve the deployment job, even if they are a required reviewer.", "environments"),
            dq("Only one of the required reviewers needs to approve the job for it to proceed.", "environments")]),
]
