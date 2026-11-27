"""Case study · Litware, Inc. Eight screens: D1 x3, D2 x2, D5 x1, D6 x2."""
from lib import Q, opt, lq, dq, dn, PART

SCENARIO = """### Overview

Litware, Inc. is a software company that develops an order management platform. Litware has a GitHub organization named Litware.

### Existing environment

Litware has a private repository named `orders-api` that contains an ASP.NET Core service. The repository has the following configuration:

- The default branch is `main`. A ruleset named RS1 targets `main`. RS1 requires a pull request, one approving review, and a status check named `build-test`. In RS1, **Require review from Code Owners** is not selected.
- A workflow named `ci.yml` runs for pull requests and reports the `build-test` check.
- A workflow named `deploy.yml` runs on every push to `main` and deploys the service to Azure. The workflow signs in to Azure by using a client secret that is stored as a repository secret.
- The default permissions of the `GITHUB_TOKEN` are read and write.

The repository contains a CODEOWNERS file that has the following content.

```text
*                    @litware/orders-team
/infra/              @litware/platform-team
/.github/workflows/  @litware/platform-team
```

### Planned changes

Litware plans to implement the following changes:

- Enable GitHub Copilot cloud agent for `orders-api` and assign issues to the agent.
- Add a remote MCP server named `tracker` so that the agent can read work items from the company's issue tracking system. The server exposes the tools `get_item`, `search_items`, `create_item`, and `update_item`.
- Add two custom agents: a dependency agent that updates package references and lock files, and a documentation agent that updates the files in `/docs/`.
- Restore the NuGet packages that the agent needs from a private feed at `nuget.litware.com`.

### Problem statements

Litware identifies the following issues:

- Last month, a change to `/infra/` was approved by a member of the orders team and merged without a review by the platform team.
- Production deployments start as soon as a pull request is merged. Nobody approves them.
- In a pilot, the reviewers reported that the agent's pull requests contained a diff but no plan or rationale.

### Technical requirements

Litware identifies the following technical requirements:

- Changes to `/infra/` and `/.github/workflows/` must be approved by the platform team before they are merged.
- A production deployment must be approved by a release manager. The production credentials must be available only to the deployment job, and only after the approval.
- The deployment job must sign in to Azure by using OpenID Connect (OIDC), and must not use a stored client secret.
- The agent must be able to read work items, and must not be able to create or change them.
- The dependency agent and the documentation agent must be able to work at the same time without interfering with each other.
- All solutions must follow the principle of least privilege and must not weaken the existing controls."""

SUBS = [

Q("c1", "single", "D1", "M2U5", "analyse", also_units=["M6U3"], docs=["codeowners", "rules"],
  stem="You need to resolve the issue with the change to `/infra/` and meet the related technical requirement.\n\nWhat should you do?",
  options=[
      opt("a", "In RS1, select **Require review from Code Owners**.", "Correct. The CODEOWNERS file already names the platform team for `/infra/`. This option makes their approval a condition for merging."),
      opt("b", "Move the `/infra/` line to the top of the CODEOWNERS file.", "Incorrect. The last matching pattern takes precedence, so `*` would then win for `/infra/` and the orders team would become the owner."),
      opt("c", "Increase the number of required approving reviews in RS1 to two.", "Incorrect. Any two reviewers would satisfy the rule. Nothing requires one of them to be from the platform team."),
      opt("d", "Add the platform team as required reviewers of an environment named `production`.", "Incorrect. Environment reviewers approve jobs, such as deployments. They don't gate the merge of a pull request."),
  ],
  answer=["a"],
  explanation="CODEOWNERS only routes review requests. The platform team was requested as reviewer, but RS1 accepted an approval from anyone. With **Require review from Code Owners** selected, a pull request that changes an owned path can't merge without an approval from an owner of that path.",
  takeaway="CODEOWNERS is advisory until the ruleset requires review from code owners.",
  evidence=[lq("This ensures that a plan and changeset affecting high-risk paths can't be merged without visibility from the right experts (when combined with required review policies).", "M2U5"),
            lq("Decision guidance: Make sure \"require CODEOWNERS review\" is enabled, or CODEOWNERS becomes advisory only.", "M6U3"),
            dn("In a CODEOWNERS file, order is important: the last matching pattern takes the most precedence. To make the owners' review mandatory, enable **Require review from Code Owners**.", "codeowners")]),

Q("c2", "multiple", "D6", "M6U3", "apply", also_units=["M6U4"], docs=["environments", "manage-environments"], select=2,
  stem="You need to meet the technical requirements for approving production deployments and for protecting the production credentials.\n\n"
       "Which two actions should you perform? " + PART,
  options=[
      opt("a", "Create an environment named `production`, add the release managers as required reviewers, and reference the environment in the deployment job.", "Correct. A job that references the environment waits until a required reviewer approves it."),
      opt("b", "Store the production credentials as secrets of the `production` environment and remove them from the repository secrets.", "Correct. Environment secrets are available only to jobs that reference the environment, and only after its protection rules pass."),
      opt("c", "Add the release managers to the CODEOWNERS file as the owners of `deploy.yml`.", "Incorrect. Code owners review changes to the workflow file. They don't approve each deployment."),
      opt("d", "Increase the number of required approving reviews in RS1 to two.", "Incorrect. That gates the merge. The deployment would still start without approval as soon as the merge happens."),
      opt("e", "Rename the repository secrets so that their names start with `PROD_`.", "Incorrect. A name doesn't restrict which jobs can read a repository secret."),
  ],
  answer=["a", "b"],
  explanation="An environment is the control for the point of execution. Required reviewers make the deployment job wait for a release manager. Moving the credentials into the environment's secrets ties them to that approval: a job gets them only if it references the environment and only after the approval.",
  takeaway="Production gate = environment with required reviewers, plus environment secrets.",
  evidence=[lq("require reviewers for production deploys", "M6U3"),
            lq("restrict production secrets to production environment only", "M6U3"),
            dq("Secrets stored in an environment are only available to workflow jobs that reference the environment. If the environment requires approval, a job cannot access environment secrets until one of the required reviewers approves it.", "environments")]),

Q("c3", "single", "D2", "M2U7", "apply", also_units=["M3U3"], docs=["mcp-config"],
  stem="You need to configure the `tracker` MCP server for GitHub Copilot cloud agent to meet the technical requirements.\n\nWhat should you include in the MCP configuration of the server?",
  options=[
      opt("a", "`\"tools\": [\"*\"]`, together with a custom instruction that forbids creating or changing work items", "Incorrect. All four tools are enabled, and the instruction is only guidance. The agent uses configured tools without asking for approval."),
      opt("b", "`\"tools\": [\"get_item\", \"search_items\", \"update_item\"]`", "Incorrect. `update_item` lets the agent change work items."),
      opt("c", "`\"type\": \"local\"`, so that the server runs in the agent's environment", "Incorrect. The server type decides how the agent reaches the server. It doesn't limit which tools the agent can call."),
      opt("d", "`\"tools\": [\"get_item\", \"search_items\"]`", "Correct. Only the two read tools are enabled, so the agent has no tool with which it could create or change a work item."),
  ],
  answer=["d"],
  explanation="The `tools` key is an allowlist. Whatever is listed there, the cloud agent can call autonomously, without asking for approval first. Listing only the read tools enforces the requirement technically, which an instruction can't do.",
  takeaway="Restrict an MCP server with a specific `tools` list, never with `*` plus an instruction.",
  evidence=[lq("Namespace control: prefer enabling a narrow tool subset rather than broad wildcards.", "M2U7"),
            lq("Adding or expanding MCP tools increases blast radius and should be reviewed like a high-risk dependency.", "M2U7"),
            dq("We strongly recommend that you allowlist specific read-only tools, since the agent will be able to use these tools autonomously and will not ask you for approval first.", "mcp-config")]),

Q("c4", "single", "D2", "M3U4", "analyse", docs=["firewall"],
  stem="During a test session, a warning in the agent's pull request states that a request to `nuget.litware.com` was blocked.\n\n"
       "You need to allow the agent to restore packages from the private feed. The agent's access to the internet must remain restricted.\n\nWhat should you do?",
  options=[
      opt("a", "Disable the firewall for the agent in the settings of the repository.", "Incorrect. The feed would be reachable, but so would every other host, which removes the restriction."),
      opt("b", "Add the URL of the feed to the custom instructions of the repository.", "Incorrect. An instruction tells the agent where the feed is. It doesn't open the firewall."),
      opt("c", "Add `nuget.litware.com` to the custom allowlist of the agent's firewall.", "Correct. Only this host is added to what the agent may reach, and the rest of the internet stays blocked."),
      opt("d", "Create an Agents secret that contains the URL of the feed.", "Incorrect. A secret passes a value to the agent. It doesn't change which hosts the agent can reach."),
  ],
  answer=["c"],
  explanation="By default, the cloud agent's access to the internet is limited by a firewall with a recommended allowlist for common package registries. A private feed isn't on that list, so the request is blocked and reported in the pull request. Adding the host to the custom allowlist is the least-privilege fix. It applies to new sessions.",
  takeaway="Blocked host for the agent → add that host to the firewall's custom allowlist.",
  evidence=[lq("Network isolation and allowlisted outbound access", "M3U4"),
            dn("By default, Copilot's access to the internet is limited by a firewall, and a recommended allowlist lets the agent download dependencies. If a request is blocked, a warning with the blocked address is added to the pull request. If Copilot needs to reach a host that isn't on the allowlist, add the host to the allowlist, then start a new session.", "firewall")]),

Q("c5", "single", "D5", "M4U3", "evaluate", also_units=["M4U4", "M4U2"],
  stem="You need to recommend an orchestration design for the dependency agent and the documentation agent.\n\nWhich design should you recommend?",
  options=[
      opt("a", "Run the agents in parallel, each on a dedicated branch and limited to its own paths.", "Correct. The two agents change different paths, so they can't collide, and a branch for each keeps their work separate and attributable."),
      opt("b", "Run the agents in parallel on one shared branch to reduce the number of pull requests.", "Incorrect. A shared branch interleaves their commits and makes ownership and rollback unclear."),
      opt("c", "Run the documentation agent only after the pull request of the dependency agent is merged.", "Incorrect. Nothing in the documentation work depends on the dependency update, and the agents must be able to work at the same time."),
      opt("d", "Replace both agents with one general-purpose agent that can change any path.", "Incorrect. A general-purpose agent has no scope boundary, which is the situation that responsibility mapping is meant to avoid."),
  ],
  answer=["a"],
  explanation="Parallel orchestration is safe when scope boundaries prevent overlap. Lock files and package references on one side and `/docs/` on the other are separate paths, so the agents can run at the same time. Sequential orchestration is for work whose input is another agent's output.",
  takeaway="Separate paths → parallel, with a branch per agent. Dependent outputs → sequential.",
  evidence=[lq("Parallel orchestration is appropriate when scope boundaries prevent overlap. For example, a documentation agent and a refactoring agent can work simultaneously if they operate in separate paths.", "M4U3"),
            lq("The core design requirement for parallel orchestration is isolation: if agents can collide on the same files, parallelism will increase instability rather than throughput.", "M4U3")]),

Q("c6", "dropdown", "D6", "M6U5", "apply", docs=["oidc-azure", "syntax"],
  stem="You need to complete the deployment job in `deploy.yml` to meet the technical requirements.\n\nHow should you complete the job?",
  template="jobs:\n  deploy:\n    runs-on: ubuntu-latest\n    [[gate]]: production\n    permissions:\n      contents: read\n      [[perm]]: write\n    steps:\n      - uses: actions/checkout@v4\n      - uses: azure/login@v2\n        with:\n"
           "          client-id: ${{ secrets.AZURE_CLIENT_ID }}\n          tenant-id: ${{ secrets.AZURE_TENANT_ID }}\n          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}\n",
  blanks={
      "gate": {"options": ["concurrency", "environment", "needs"], "answer": "environment",
               "rationale": "Referencing the `production` environment makes the job wait for the release manager's approval and gives it the environment's secrets afterwards."},
      "perm": {"options": ["deployments", "id-token", "packages"], "answer": "id-token",
               "rationale": "A job needs `id-token: write` to request an OIDC token. It doesn't grant write access to any resource. Every permission that isn't listed is set to `none`."},
  },
  explanation="The job gets exactly what it needs. `environment: production` applies the approval and releases the environment's secrets. `id-token: write` lets the job request the OIDC token that `azure/login` exchanges for an Azure access token, so no client secret is stored. Because a `permissions` block is present, all other scopes are `none`.",
  takeaway="OIDC sign-in needs `id-token: write`. Declare permissions on the job that needs them.",
  evidence=[lq("Set a read-only default at the workflow level, then elevate write permissions only for the job that must write.", "M6U5"),
            dq("If you specify the access for any of these permissions, all of those that are not specified are set to `none`.", "syntax"),
            dn("The `id-token` permission is used to fetch an OpenID Connect (OIDC) token, and this requires `id-token: write`. The `azure/login` action receives a JWT from the GitHub OIDC provider and then requests an access token from Azure.", "oidc-azure")]),

Q("c7", "single", "D1", "M1U5", "apply", also_units=["M2U5"],
  stem="You need to resolve the issue that the reviewers reported during the pilot.\n\nWhat should you do?",
  options=[
      opt("a", "Increase the number of required approving reviews in RS1 to two.", "Incorrect. Two reviewers would look at the same diff without a plan."),
      opt("b", "Add a pull request template that contains a required Plan section.", "Correct. The template makes every agent pull request state its goal, scope, steps and success criteria, so intent can be reviewed."),
      opt("c", "Allow the agent to merge its own pull requests after the checks pass.", "Incorrect. That removes the review in which the missing plan was noticed."),
      opt("d", "Increase the retention period of the workflow logs.", "Incorrect. Logs show what ran. They don't state what the agent intended to do or why."),
  ],
  answer=["b"],
  explanation="A pull request with a diff and no plan or rationale is the anti-pattern called planless execution. The mitigation uses a GitHub control: a pull request template with a plan section, reviewed before merge. RS1 already requires a review, so the missing piece is the plan.",
  takeaway="Diff without a plan → pull request template with a required Plan section.",
  evidence=[lq("Planless execution: The agent begins changing code without a clear, inspectable approach.", "M1U5"),
            lq("Require a plan section via PR template; require review before merge", "M1U5"),
            lq("A pull request template ensures that every agent PR provides consistent plan and evidence sections.", "M2U5")]),

Q("c8", "single", "D1", "M2U2", "understand",
  stem="You need to recommend the SDLC stages to which GitHub Copilot cloud agent is scoped at first. The solution must minimize risk and use the stages in which GitHub can enforce boundaries on the agent's work.\n\nWhich stages should you recommend?",
  options=[
      opt("a", "Planning and deployment", "Incorrect. Deployment is the stage that is usually restricted and gated by approvals."),
      opt("b", "Deployment only", "Incorrect. Deployment carries the highest risk and is usually restricted for agents."),
      opt("c", "Implementation and validation", "Correct. In these stages, the pull request and the workflows are the control points for everything that the agent does."),
      opt("d", "All stages", "Incorrect. An agent that operates across the whole SDLC is hard to reason about, to limit and to audit."),
  ],
  answer=["c"],
  explanation="An agent shouldn't operate across the entire SDLC without restriction. Most teams start with implementation and validation, because there the agent's work passes through pull requests and workflow runs, which GitHub can gate. Deployment stays behind environments and approvals.",
  takeaway="Start agents in implementation and validation. Agents propose; humans and policy accept.",
  evidence=[lq("Most teams start by scoping agents to the implementation and validation stages, where pull requests and workflows provide natural control points.", "M2U2"),
            lq("Agent systems should not operate across the entire SDLC without restriction.", "M2U2")]),
]

CASE = {"id": "x1-case-litware", "type": "case", "domain": "D1", "title": "Case study: Litware, Inc.", "scenario": SCENARIO, "questions": SUBS}
