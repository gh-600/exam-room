"""Domain 6 · Governance, guardrails and operations (Learn module 6). Seven standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO, PART

QUESTIONS = [

Q("x1-d6-autonomy-levels", "match", "D6", "M6U2", "understand",
  stem="You are assigning an autonomy level to each agent in a GitHub organization named Org1.\n\nWhich autonomy level describes each agent?",
  choices=[{"id": "read", "text": "Read-only autonomy"}, {"id": "propose", "text": "Propose-only autonomy"},
           {"id": "guard", "text": "Execute with guardrails"}, {"id": "human", "text": "Human-authorized execution"}],
  targets=[
      {"id": "t1", "text": "An agent that runs pre-approved test, build, and staging deployment workflows within defined limits", "answer": "guard",
       "rationale": "It executes, but only workflows that were approved in advance and within limits."},
      {"id": "t2", "text": "An agent that classifies new issues and recommends labels, and that cannot modify anything", "answer": "read",
       "rationale": "It inspects, classifies and recommends. It changes nothing."},
      {"id": "t3", "text": "An agent that deploys to production only after a reviewer approves the deployment", "answer": "human",
       "rationale": "A high-impact action happens only after a human approves it."},
      {"id": "t4", "text": "An agent that creates branches and pull requests, and that cannot merge or deploy", "answer": "propose",
       "rationale": "It proposes changes through pull requests. Acceptance stays with people and policy."},
  ],
  explanation="The four levels grow with the impact of what the agent may do: inspect only, propose through pull requests, run pre-approved workflows inside limits, and perform high-impact actions only after a human approves. Autonomy is usually a combination of pull request rules, environments, workflow permissions and tool access, not one setting.",
  takeaway="Read-only → propose-only → execute with guardrails → human-authorized execution.",
  evidence=[lq("Read-only autonomy: Agent can inspect, summarize, classify, and recommend changes, but can't modify anything.", "M6U2"),
            lq("Propose-only autonomy: Agent can create branches and pull requests, but can't merge or deploy.", "M6U2"),
            lq("Execute with guardrails: Agent can run pre-approved workflows (tests, builds, staging deploys) within defined limits.", "M6U2"),
            lq("Human-authorized execution: Agent can perform high-impact actions only after a human approves (production deploy, workflow changes, secret access).", "M6U2")]),

Q("x1-d6-risk-routing", "dropdown", "D6", "M6U2", "apply", docs=["control-deployments"],
  stem="A workflow named `agent-plan-apply` has a job named `plan` that reads a machine-readable risk rating from an agent's plan and exposes it as the job output `risk`.\n\n"
       "Plans that are rated `low` must be applied automatically. All other plans must wait for the approval of the required reviewers of an environment named `approval-required`.\n\n"
       "You need to route each plan according to its risk rating.\n\n"
       "How should you complete the workflow?",
  template="  apply:\n    needs: plan\n    runs-on: ubuntu-latest\n    [[gate]]: approval-required\n    if: ${{ needs.plan.outputs.risk [[apply_if]] 'low' }}\n    steps:\n      - run: ./scripts/apply.sh out/plan.json\n\n"
           "  apply_auto:\n    needs: plan\n    runs-on: ubuntu-latest\n    if: ${{ needs.plan.outputs.risk [[auto_if]] 'low' }}\n    steps:\n      - run: ./scripts/apply.sh out/plan.json\n",
  blanks={
      "gate": {"options": ["concurrency", "environment", "permissions"], "answer": "environment",
               "rationale": "A job that references an environment with required reviewers waits until a reviewer approves it. `concurrency` only serializes runs, and `permissions` only scopes the token."},
      "apply_if": {"options": ["!=", "=="], "answer": "!=",
                   "rationale": "The gated job must run for every rating that is not `low`."},
      "auto_if": {"options": ["!=", "=="], "answer": "==",
                  "rationale": "The job without a gate must run only when the rating is `low`."},
  },
  explanation="The risk rating is a job output, so the routing is decided by the workflow and not by a description that someone has to interpret. The job for anything other than `low` targets the environment and therefore waits for approval. The job for `low` has no environment and runs at once.",
  takeaway="Route on a machine-readable risk signal: `if` picks the job, `environment` adds the approval.",
  evidence=[lq("Decision guidance: Don’t rely on narrative explanations of risk. Use a machine-readable signal and enforce routing.", "M6U2"),
            lq("High-risk plans require explicit human approval", "M6U2"),
            dq("Jobs that reference an environment configured with required reviewers will wait for an approval before starting.", "control-deployments")]),

Q("x1-d6-security-failure", "single", "D6", "M6U7", "analyse", also_units=["M4U5"],
  stem="An agent opens a pull request in a GitHub repository named Repo1. A required code scanning check fails, because the change introduces a vulnerability. The agent pushes three more commits that rearrange the code, and the check fails each time with the same alert. The team's recovery policy allows bounded retries for transient failures.\n\n"
       "You need to apply the correct recovery strategy. What should occur next?",
  options=[
      opt("a", "The agent continues to push new commits until the check passes.", "Incorrect. The failure isn't transient, and repeated attempts with the same result are a loop that the policy is meant to stop."),
      opt("b", "The check is removed from the required status checks for pull requests that agents open.", "Incorrect. That removes the control that detected the problem and creates a bypass path."),
      opt("c", "Automated iteration stops, and the failure is escalated to a human for investigation.", "Correct. A security failure is investigated, not retried, and a failure that repeats with the same signature is escalated."),
      opt("d", "The agent dismisses the alert as a false positive and requests a review.", "Incorrect. The agent would be deciding on its own evidence. A person must judge a security finding."),
  ],
  answer=["c"],
  explanation="Recovery strategies depend on the kind of failure. A transient failure, such as a network error, may be retried within a limit. A security failure isn't transient: it is investigated. And when the same required check fails repeatedly with the same signature, automation stops and a human takes over.",
  takeaway="Retry transient failures. Investigate security failures. Escalate repeated ones.",
  evidence=[lq("Investigate security failures instead of repeatedly retrying", "M6U7"),
            lq("Escalate after repeated failures", "M6U7"),
            lq("if required checks fail twice with the same failure signature, or", "M4U5")]),

Q("x1-d6-rubber-stamping", "single", "D6", "M6U7", "evaluate", also_units=["M6U4"],
  stem="In a GitHub organization named Org1, agents open about 60 pull requests each day. An audit shows that reviewers approve most of them in less than a minute, without opening the changes. The pull requests are large, and they contain no test or scan results.\n\n"
       "You need to restore meaningful review without adding more approval steps. What should you do?",
  options=[
      opt("a", "Require three approving reviews instead of one for every pull request.", "Incorrect. More approvals of the same kind add friction and fatigue. Three quick clicks aren't a review."),
      opt("b", "Add the reviewers to the bypass list of the ruleset so that merging is faster.", "Incorrect. A bypass list is a way around the policy, which is the opposite of oversight."),
      opt("c", "Allow the agents to merge their own pull requests when all checks pass.", "Incorrect. That removes human judgment instead of restoring it."),
      opt("d", "Require evidence in pull requests, route reviews by using CODEOWNERS, and keep pull requests small.", "Correct. Evidence makes review fast, CODEOWNERS sends each change to people who have the context, and small pull requests can actually be read."),
  ],
  answer=["d"],
  explanation="This is rubber-stamping: approvals have become a click to unblock. The cause is governance fatigue, so the remedy is to make each review easier, not to add reviews. Require evidence such as tests and scans, route reviews through CODEOWNERS, and keep pull requests small and scoped.",
  takeaway="Rubber-stamping → better evidence, CODEOWNERS routing, smaller pull requests.",
  evidence=[lq("require evidence (tests, scans, artifacts) so review is fast", "M6U4"),
            lq("route reviews via CODEOWNERS so reviewers have context", "M6U4"),
            lq("keep PRs small and scoped", "M6U4")]),

Q("x1-d6-cli-tool-scope", "multiple", "D6", "M6U2", "apply", docs=["copilot-cli"], select=2,
  stem="You run GitHub Copilot CLI from a script by using the following command.\n\n"
       "```bash\ncopilot -p \"Summarize the last 10 commits and highlight breaking changes.\"\n```\n\n"
       "The command has the following requirements:\n\n- Copilot must be able to run `git` commands without asking for approval.\n- Copilot must never run `git push`.\n- No other tool may be approved automatically.\n\n"
       "You need to meet the requirements. Which two options should you add to the command? " + PART,
  options=[
      opt("a", "`--allow-tool='shell(git)'`", "Correct. This approves `git` commands only, so every other tool still needs approval."),
      opt("b", "`--allow-all-tools`", "Incorrect. This approves every tool, including file edits and any shell command."),
      opt("c", "`--deny-tool='shell(git push)'`", "Correct. A deny rule takes precedence over allow rules, so `git push` is blocked although `git` is allowed."),
      opt("d", "`--allow-tool='write'`", "Incorrect. This approves tools that modify files, which the task doesn't need."),
      opt("e", "`--allow-tool='shell'`", "Incorrect. Without a command in parentheses, this approves every shell command."),
  ],
  answer=["a", "c"],
  explanation="For a terminal-based agent, tool access is the governance boundary. Allow exactly what the task needs, here the `git` command, and deny the one subcommand that has consequences. Because `--deny-tool` takes precedence over `--allow-tool`, the two options combine safely.",
  takeaway="Allow narrowly with `--allow-tool='shell(COMMAND)'`. `--deny-tool` wins over any allow.",
  evidence=[lq("Decision guidance: Match tool access to consequence. Low-risk tasks shouldn't inherit high-risk capabilities.", "M6U2"),
            lq("This pattern helps you support read-only analysis (like commit summarization) without granting broad write capability or auto-approving unrelated tools.", "M6U2"),
            dq("This option takes precedence over the `--allow-all-tools` and `--allow-tool` options.", "copilot-cli")]),

Q("x1-d6-progressive-autonomy", "build", "D6", "M6U2", "apply",
  stem="Your team plans to increase the autonomy of an agent step by step as the agent proves reliable.\n\nWhich four actions should you perform in sequence?",
  items=[
      {"id": "p1", "text": "Allow the agent to open pull requests but not to merge them."},
      {"id": "p2", "text": "Allow the agent to merge low-risk pull requests after the checks pass."},
      {"id": "p3", "text": "Allow the agent to deploy to staging automatically."},
      {"id": "p4", "text": "Allow the agent to deploy to production only through an environment approval."},
      {"id": "x1", "text": "Allow the agent to push low-risk changes directly to the default branch."},
      {"id": "x2", "text": "Remove the required status checks for pull requests that the agent opens."},
  ],
  answer=["p1", "p2", "p3", "p4"],
  explanation="Progressive autonomy starts with strict controls and relaxes them as the agent earns trust: first proposals only, then merging low-risk changes, then automatic deployment to staging, and production only behind an environment approval. At no stage does the agent get a way around pull requests or checks.",
  takeaway="Open pull requests → merge low risk → deploy to staging → production with approval.",
  evidence=[lq("Phase 1: agent can only open PRs, can't merge", "M6U2"), lq("Phase 2: agent can merge low-risk PRs after checks", "M6U2"),
            lq("Phase 3: agent can deploy to staging automatically", "M6U2"), lq("Phase 4: agent can deploy to production only through environment approval", "M6U2")]),

Q("x1-d6-governance-statements", "statements", "D6", "M6U4", "understand", also_units=["M6U3"],
  stem="You are designing governance for agents in a GitHub organization named Org1.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "A banner that warns about dangerous commands prevents an agent from running them.", "answer": "no",
       "explanation": "Banners and logging inform. Only an enforceable control, such as a hook that denies the command, prevents execution."},
      {"id": "s2", "statement": "To keep oversight effective, human approval should be required at every step of a workflow, including analysis and routine checks.", "answer": "no",
       "explanation": "Oversight belongs at decision points such as merge, deployment and access to secrets. Approvals at every step slow the work and cause fatigue."},
      {"id": "s3", "statement": "A policy that exists only in documentation and is not enforced by the platform can be bypassed.", "answer": "yes",
       "explanation": "A control that the platform doesn't enforce depends on everyone following it, so it will be skipped."},
  ],
  explanation="Human-in-the-loop design puts people at the few decisions that matter and automates the rest. Enforcement has to be technical: a hook that blocks, a ruleset, an environment. Documentation, logs and warnings support those controls but don't replace them.",
  takeaway="People at decision points. Enforcement by the platform, not by documentation.",
  evidence=[lq("Put humans at decision points (merge, deploy, secret access), not at every step (analysis, formatting, routine checks).", "M6U4"),
            lq("Decision guidance: Use enforceable hooks for blocking. Logging and banners are helpful, but they don't prevent execution.", "M6U3"),
            lq("\"Controls in docs only\" is an anti-pattern. If the platform can't enforce it, it will be bypassed.", "M6U3")]),
]
