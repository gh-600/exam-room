"""Domain 2 · Tool use and environment interaction (Learn module 3, with module 2 units 6 and 7). Eleven standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO

QUESTIONS = [

Q("x2-d2-required-tools", "single", "D2", "M2U7", "apply", docs=["custom-agents"],
  stem="A custom agent named `planner` has the following agent profile in a GitHub repository named Repo1.\n\n"
       "```yaml\n---\nname: planner\ndescription: Produces an implementation plan and delegates the work\ntools: [\"read\", \"search\"]\n---\n```\n\n"
       "The planner must be able to hand the implementation to another custom agent named `implementer`. The planner must remain unable to change files or to run commands.\n\n"
       "You need to identify the tool that the planner requires. Which configuration should you use?",
  options=[
      opt("a", "`tools: [\"read\", \"search\", \"execute\"]`", "Incorrect. `execute` runs shell commands, which the planner must not be able to do."),
      opt("b", "`tools: [\"read\", \"search\", \"agent\"]`", "Correct. The `agent` alias allows a different custom agent to be invoked to accomplish a task, and it adds no ability to edit files or to run commands."),
      opt("c", "`tools: [\"read\", \"search\", \"implementer\"]`", "Incorrect. `implementer` is not a tool name. Unrecognized tool names are ignored, so nothing changes."),
      opt("d", "`tools: [\"read\", \"search\", \"edit\"]`", "Incorrect. `edit` lets the planner change files, and it does not let the planner invoke another agent."),
  ],
  answer=["b"],
  explanation="The `tools` property is the capability boundary of an agent, and delegation is a capability of its own. To hand work to another custom agent, the planner needs the `agent` tool alias. The planner stays read-only for files, because `edit` and `execute` are still absent from the list.",
  takeaway="Delegation needs the `agent` tool. Keep `edit` and `execute` away from planning agents.",
  evidence=[lq("Delegation boundary: which subagents can be invoked and how handoffs occur", "M2U7"),
            lq("Use read-only toolsets for planning and review agents.", "M2U7"),
            dn("The reference lists the tool aliases for custom agents. `agent` allows a different custom agent to be invoked to accomplish a task, `execute` runs a command in the shell, and `edit` allows file edits. All unrecognized tool names are ignored.", "custom-agents")]),

Q("x2-d2-mcp-rollout", "build", "D2", "M3U3", "apply",
  stem="Your company plans to let developers use only approved MCP servers in their IDEs. The developers must discover the servers from a custom MCP registry.\n\n"
       "Which four actions should be performed in sequence?",
  items=[
      {"id": "reg", "text": "The company creates or hosts an MCP registry that lists the approved servers."},
      {"id": "pol", "text": "An owner enters the registry URL in the Copilot policy settings and selects **Registry only**."},
      {"id": "disc", "text": "A developer opens an MCP-capable IDE, and the client discovers the approved servers from the registry."},
      {"id": "use", "text": "The developer enables a server, and the agent uses the tools of that server during a task."},
      {"id": "manual", "text": "Each developer adds the URLs of the servers to a local configuration file by hand."},
      {"id": "all", "text": "An owner selects **Allow all** so that the clients can read the registry."},
  ],
  answer=["reg", "pol", "disc", "use"],
  explanation="The registry must exist before its URL can be entered in the policy, and the policy must be in place before a client can discover the approved servers. The developer then enables a server, and only after that can the agent use its tools. **Allow all** removes the restriction, and manual configuration is the unmanaged discovery that a registry replaces.",
  takeaway="Registry → policy with the registry URL and Registry only → discovery in the client → use.",
  evidence=[lq("An organization configures an MCP registry", "M3U3"),
            lq("The organization defines an allow list policy for approved servers", "M3U3"),
            lq("The client discovers approved servers from the registry", "M3U3"),
            lq("Registry only → only servers from the registry are allowed", "M3U3")]),

Q("x2-d2-ci-invoke", "dropdown", "D2", "M3U4", "apply", docs=["cli-programmatic"],
  stem="You are adding a job to a workflow in a GitHub repository named Repo1. The job runs GitHub Copilot CLI, which is already installed and authenticated on the runner. The step that runs the agent has the following requirements:\n\n"
       "- It must use the custom agent named `security-reviewer`.\n"
       "- It must pass the prompt on the command line and exit when the task is complete.\n"
       "- It must not pause to ask for user input, because nobody is present during the run.\n\n"
       "You need to complete the step.\n\n"
       "How should you complete the workflow?",
  template="jobs:\n  agent-task:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Run the security review\n        run: |\n"
           "          copilot [[agent]] security-reviewer \\\n            [[prompt]] \"Review the changes on this branch for vulnerabilities\" \\\n            [[noask]]\n",
  blanks={
      "agent": {"options": ["--add-dir", "--agent", "--model"], "answer": "--agent",
                "rationale": "`--agent` selects a custom agent. `--model` chooses the AI model, and `--add-dir` adds a directory to the allowed paths."},
      "prompt": {"options": ["-i", "-p", "-s"], "answer": "-p",
                 "rationale": "`-p` executes the prompt in non-interactive mode, and the CLI exits after completion. `-i` starts an interactive session, and `-s` only reduces the output."},
      "noask": {"options": ["--allow-all-tools", "--no-ask-user", "--share"], "answer": "--no-ask-user",
                "rationale": "`--no-ask-user` prevents the agent from pausing to seek user input. `--allow-all-tools` is about tool permissions, and it is broader than this job needs."},
  },
  explanation="To run an agent as part of CI, you invoke it inside a workflow, and the workflow becomes the execution boundary. In a job, nobody can answer a question, so the prompt is passed with `-p` and the agent is told not to ask with `--no-ask-user`. `--agent` runs the task with the custom agent's profile, and therefore with its tools.",
  takeaway="Agent in CI: `--agent NAME`, `-p \"PROMPT\"`, `--no-ask-user`.",
  evidence=[lq("To run agent-driven tasks as part of CI, you invoke them inside a workflow. In this setup, the workflow becomes the execution boundary, and the agent runs within the runner using defined steps and permissions.", "M3U4"),
            dq("Execute a prompt in non-interactive mode.", "cli-programmatic"),
            dq("Prevent the agent from pausing to seek additional user input.", "cli-programmatic")]),

Q("x2-d2-github-mcp-scope", "single", "D2", "M3U3", "apply", docs=["mcp-config"],
  stem="GitHub Copilot cloud agent works on issues in a GitHub repository named Repo1. For some tasks, the agent must read issues in a second repository named Repo2 by using the GitHub MCP server. The agent reports that it cannot access Repo2.\n\n"
       "You need to give the agent read access to Repo2 through the GitHub MCP server.\n\n"
       "What should you do?",
  options=[
      opt("a", "Add `github.com` to the custom allowlist of the agent's firewall, and start a new agent session.", "Incorrect. The network is not what limits the agent. The token that the GitHub MCP server uses can read only Repo1."),
      opt("b", "Set `\"tools\": [\"*\"]` for the GitHub MCP server in the MCP configuration of Repo1.", "Incorrect. `tools` selects which tools of a server the agent may use. It does not change what the server's token can access."),
      opt("c", "Configure the GitHub MCP server in the MCP configuration of Repo1, and add an Agents secret named `COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN` that holds a token with read access to Repo2.", "Correct. By default, the server uses a token that is scoped to the current repository. A personal access token with wider access, stored under this name, widens what the server can read."),
      opt("d", "Add a GitHub Actions secret named `GH_TOKEN` that holds a token with read access to Repo2, and reference the secret in `copilot-setup-steps.yml`.", "Incorrect. The agent cannot read secrets that were created for GitHub Actions, and `GH_TOKEN` is not the name that the GitHub MCP server looks for."),
  ],
  answer=["c"],
  explanation="The GitHub MCP server is built into the cloud agent. By default it connects with a specially scoped token that has read-only access to the current repository. To reach data outside that repository, you configure the server with a personal access token that has wider access, or with a GitHub App. GitHub recommends a fine-grained token that is limited to read-only permissions on the repositories that the agent needs.",
  takeaway="Built-in GitHub MCP server = read-only on the current repository. Wider access = `COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN` or a GitHub App.",
  evidence=[lq("The GitHub MCP server is one example. It connects AI clients to GitHub capabilities such as repositories, issues, and pull requests.", "M3U3"),
            dn("The GitHub MCP server is enabled by default and connects to GitHub with a specially scoped token that only has read-only access to the current repository. To allow Copilot to access data outside the current repository, you can configure a personal access token with wider access or a GitHub App. For a personal access token, you add a secret called `COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN`.", "mcp-config")]),

Q("x2-d2-tools-statements", "statements", "D2", "M2U7", "understand", docs=["custom-agents"],
  stem="You are reviewing the `tools` property in the agent profiles of GitHub Copilot cloud agent for a GitHub repository named Repo1. An MCP server named `tickets` is configured in the settings of Repo1.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "An agent profile that omits the `tools` property gives the agent all available tools, including the tools of `tickets`.", "answer": "yes",
       "explanation": "If no tools are specified, all available tools are enabled. That includes the tools of the MCP servers that are configured in the repository settings."},
      {"id": "s2", "statement": "A tool name in the `tools` property that is not recognized prevents the agent profile from being loaded.", "answer": "no",
       "explanation": "Unrecognized tool names are ignored. The profile loads, and the agent simply does not get that tool."},
      {"id": "s3", "statement": "With `tools: [\"read\", \"tickets/get_ticket\"]`, the agent can use the `get_ticket` tool of `tickets` and no other tool of that server.", "answer": "yes",
       "explanation": "A specific list enables only the tools that it names. A tool of an MCP server is named with the server name, a slash, and the tool name."},
  ],
  explanation="The `tools` list filters the tools that an agent gets, both the built-in ones and the ones from MCP servers. No list means every tool, an empty list means no tool, and a specific list means only the named tools. Because an omitted property is the widest setting, an allowlist is the safer default for an agent profile.",
  takeaway="`tools` omitted = all tools. `tools: []` = none. A list = only those tools, with `server/tool` for MCP tools.",
  evidence=[lq("Capability boundary: which tools are allowed (prefer allowlists)", "M2U7"),
            dq("If no tools are specified, all available tools are enabled", "custom-agents"),
            dq("Tool names from specific MCP servers can be prefixed with the server name followed by a `/`.", "custom-agents"),
            dq("All unrecognized tool names are ignored", "custom-agents")]),

Q("x2-d2-repo-access", "single", "D2", "M3U4", "apply", docs=["manage-cloud-agent"],
  stem="A GitHub organization named Org1 has 40 repositories. GitHub Copilot cloud agent is enabled for the members of Org1 and is available in every repository.\n\n"
       "You need to ensure that the agent can be used only in two repositories named Repo1 and Repo2. The members must keep their access to the other features of Copilot.\n\n"
       "What should you do?",
  options=[
      opt("a", "In the settings of Org1, set the repository access of the cloud agent to **Selected repositories**, and select Repo1 and Repo2.", "Correct. The \"Repository access\" control defines which repositories allow the agent. The other Copilot features are not affected."),
      opt("b", "In the Copilot policies of Org1, disable the policy for the cloud agent.", "Incorrect. That blocks the agent in all 40 repositories, including Repo1 and Repo2."),
      opt("c", "In each of the other repositories, add a ruleset that blocks branches whose names start with `copilot/`.", "Incorrect. That only makes the agent's sessions fail in 38 repositories. It does not scope where the agent is available, and it must be maintained for every new repository."),
      opt("d", "In Repo1 and Repo2, add a custom agent profile that sets the `target` property to the repository name.", "Incorrect. `target` selects the environment of a custom agent, such as `vscode` or `github-copilot`. It does not limit repositories."),
  ],
  answer=["a"],
  explanation="Repository scope is the first boundary of an agent's execution context. By default, the cloud agent is available in all repositories of an organization in which it is enabled. An organization owner narrows this with the \"Repository access\" control. In a repository where the agent is available, any user who has access to Copilot and write permission can delegate work to it.",
  takeaway="Scope the cloud agent with Repository access → Selected repositories in the organization settings.",
  evidence=[lq("Repository scope is the first boundary that limits agent behavior.", "M3U4"),
            dq("Use the \"Repository access\" control to define which repositories allow the agent.", "manage-cloud-agent"),
            dn("By default, the cloud agent is available in all repositories in an organization where it is enabled. An organization owner can block the agent from being used in some or all repositories, for example by choosing \"Selected repositories\".", "manage-cloud-agent")]),

Q("x2-d2-error-handling", "single", "D2", "M3U5", "apply", docs=["syntax"],
  stem="A workflow in a GitHub repository named Repo1 contains the following steps.\n\n"
       "```yaml\n- name: Run agent task\n  run: copilot -p \"Update the API reference in docs/\" --no-ask-user\n  continue-on-error: true\n- name: Open pull request\n  run: ./scripts/open-pr.sh\n```\n\n"
       "Last night, the agent step failed halfway, and the workflow opened a pull request that contained incomplete changes.\n\n"
       "You need to ensure that the job stops when the agent step fails. What should you do?",
  options=[
      opt("a", "Add `if: always()` to the `Open pull request` step.", "Incorrect. `always()` makes the step run even after a failure, which is the opposite of what is required."),
      opt("b", "Add `timeout-minutes: 10` to the `Run agent task` step.", "Incorrect. A timeout limits how long the step may run. With `continue-on-error: true`, the job still continues after the step fails."),
      opt("c", "Set `fail-fast: false` in the `strategy` of the job.", "Incorrect. `fail-fast` controls whether the other jobs of a matrix are canceled. It does not affect the steps of this job."),
      opt("d", "Remove `continue-on-error: true` from the `Run agent task` step.", "Correct. Without it, a failed step fails the job, and the later steps do not run."),
  ],
  answer=["d"],
  explanation="Error handling starts with failing fast. `continue-on-error: true` lets a job pass when the step fails, so the next step ran on a half-finished result. Without the setting, the default applies: the job stops at the failed step, and no partial change reaches a pull request.",
  takeaway="Agent steps must fail fast. `continue-on-error: true` turns an error into a silent continuation.",
  evidence=[lq("This ensures that errors stop execution instead of silently continuing.", "M3U5"),
            lq("Preventing partial or inconsistent changes", "M3U5"),
            dq("Prevents a job from failing when a step fails. Set to `true` to allow a job to pass when this step fails.", "syntax")]),

Q("x2-d2-contexts", "dropdown", "D2", "M2U6", "apply", docs=["contexts"],
  stem="A workflow in a GitHub repository named Repo1 validates the pull requests of an agent. The workflow has the following requirements:\n\n"
       "- The `validate` job must run only when the run was triggered by a pull request.\n"
       "- The build configuration must come from a repository variable named `BUILD_CONFIGURATION` that is managed in the settings of Repo1.\n"
       "- The test step must use the verbosity that the job sets in an environment variable named `TEST_VERBOSITY`.\n\n"
       "You need to use the correct context for each value.\n\n"
       "How should you complete the workflow?",
  template="on:\n  pull_request:\n    branches: [main]\n  workflow_dispatch:\n\njobs:\n  validate:\n    if: [[event]].event_name == 'pull_request'\n    runs-on: ubuntu-latest\n    env:\n      TEST_VERBOSITY: minimal\n    steps:\n      - uses: actions/checkout@v4\n"
           "      - run: dotnet build --configuration ${{ [[config]].BUILD_CONFIGURATION }}\n      - run: dotnet test --verbosity ${{ [[level]].TEST_VERBOSITY }}\n",
  blanks={
      "event": {"options": ["env", "github", "secrets", "vars"], "answer": "github",
                "rationale": "The `github` context holds information about the workflow run, including the event that triggered it."},
      "config": {"options": ["env", "github", "secrets", "vars"], "answer": "vars",
                 "rationale": "The `vars` context contains the configuration variables that are set at the repository, organization, or environment level."},
      "level": {"options": ["env", "github", "secrets", "vars"], "answer": "env",
                "rationale": "The `env` context contains the variables that are set in the workflow, the job, or the step. `TEST_VERBOSITY` is set on the job."},
  },
  explanation="Each context has one purpose. `github` answers what triggered the run and is used for runtime decisions such as defensive gating. `vars` holds configuration that is managed centrally and reused. `env` holds the variables that the workflow itself defines. `secrets` is for sensitive values, and none of the three values is one.",
  takeaway="`github` = the event and the run. `vars` = managed configuration. `env` = variables set in the workflow.",
  evidence=[lq("github.* → event metadata and runtime decisions (\"what triggered this run?\")", "M2U6"),
            lq("vars.* → centrally managed configuration values designed to be reused", "M2U6"),
            lq("env.* → job-level environment variables and runtime configuration", "M2U6"),
            dq("Contains variables set at the repository, organization, or environment levels.", "contexts")]),

Q("x2-d2-base-branch", "single", "D2", "M3U4", "apply", docs=["agent-task"],
  stem="A GitHub repository named Repo1 has a default branch named `main` and a maintenance branch named `release/2.4`. You delegate a bug fix for version 2.4 to GitHub Copilot cloud agent from the GitHub CLI.\n\n"
       "You need to ensure that the agent creates its working branch from `release/2.4` and not from `main`.\n\n"
       "Which command should you run?",
  options=[
      opt("a", "`gh agent-task create \"Fix the rounding error in invoice totals\" --base release/2.4`", "Correct. `--base` chooses a base branch for the task, instead of the default branch of the repository."),
      opt("b", "`gh agent-task create \"Fix the rounding error in invoice totals\" --repo release/2.4`", "Incorrect. `--repo` selects a repository, not a branch."),
      opt("c", "`gh agent-task create \"Fix the rounding error in invoice totals on release/2.4\" --follow`", "Incorrect. `--follow` streams the session log. Naming the branch in the prompt is guidance, and the task still starts from the default branch."),
      opt("d", "`gh agent-task view release/2.4 --log`", "Incorrect. `view` shows an existing session. It does not start a task."),
  ],
  answer=["a"],
  explanation="Branch-based scope is set by the system that runs the agent, not by the agent's own configuration. When you delegate a task, you can select the base branch. The agent then creates its working branch from that branch and opens a pull request that targets it. From the GitHub CLI, the option is `--base`.",
  takeaway="Base branch for an agent task: select it when you delegate. In the CLI, `gh agent-task create … --base BRANCH`.",
  evidence=[lq("When delegating tasks to the Copilot coding agent, you can select a specific base branch.", "M3U4"),
            lq("Branch-based scope is always enforced by the execution context, not the custom agent itself.", "M3U4"),
            dq("Choose a base branch, instead of using the repository's default branch (`--base`)", "agent-task")]),

Q("x2-d2-retries", "single", "D2", "M3U5", "apply", also_units=["M2U7"],
  stem="A scheduled workflow in a GitHub repository named Repo1 runs an agent task. About one run in ten fails, because the package registry returns a temporary network error. The same run succeeds when a maintainer starts it again.\n\n"
       "You need to ensure that the workflow recovers from this failure without manual intervention. The workflow must not loop indefinitely, and a failure that persists must remain visible.\n\n"
       "What should you do?",
  options=[
      opt("a", "Set `continue-on-error: true` on the step that runs the agent task.", "Incorrect. The job would pass whether the task succeeded or not, so a persistent failure would be hidden."),
      opt("b", "Run the step in a loop of at most three attempts, and fail the step if every attempt fails.", "Correct. A bounded retry absorbs a transient error, and the final failure keeps a persistent problem visible."),
      opt("c", "Add a second workflow that starts the first workflow again each time that it fails.", "Incorrect. Nothing limits the number of restarts, so a persistent failure would loop indefinitely."),
      opt("d", "Assign every failed run to a maintainer, who investigates it before a new attempt.", "Incorrect. That is manual intervention for a failure that a retry resolves."),
  ],
  answer=["b"],
  explanation="Retries are for temporary failures, such as network issues. They must be bounded, and the last attempt must still be able to fail. A retry loop that ends without an error after the final attempt reports success for a run that failed. Escalation to a person is the next stage, for failures that repeat.",
  takeaway="Transient failure → bounded retry that still fails at the end. Repeated failure → escalation.",
  evidence=[lq("Retries help handle temporary failures such as network issues or transient errors.", "M3U5"),
            lq("Using retry logic in scripts", "M3U5"),
            lq("Bounded retries for transient failures", "M2U7"),
            lq("This policy helps prevent infinite loops and makes failures actionable.", "M2U7")]),

Q("x2-d2-registry-cloud-agent", "single", "D2", "M3U3", "analyse", docs=["mcp-registry", "mcp-config"],
  stem="An owner of a GitHub organization named Org1 configures a custom MCP registry and selects **Registry only** to restrict MCP access. In Visual Studio Code, developers can now use only the servers that the registry lists. An audit finds that GitHub Copilot cloud agent in a repository named Repo1 still uses an MCP server that the registry does not list. The server is defined in the MCP configuration of Repo1.\n\n"
       "You need to explain the audit finding. What is the cause?",
  options=[
      opt("a", "The policy applies to remote MCP servers only, and the server in Repo1 is a local server.", "Incorrect. Under **Registry only**, the enforcement applies to both remote and local MCP servers."),
      opt("b", "A change of the policy is applied to the cloud agent only after 24 hours.", "Incorrect. A selected policy is applied immediately. Waiting does not change the finding."),
      opt("c", "MCP private registry enforcement is not supported for GitHub Copilot cloud agent.", "Correct. The reference lists the supported surfaces. Copilot CLI and the IDEs are supported, and the cloud agent is not."),
      opt("d", "The server sets `\"tools\": [\"*\"]`, which exempts the server from the policy.", "Incorrect. `tools` selects the tools of a server that the agent may use. It has no effect on the registry policy."),
  ],
  answer=["c"],
  explanation="The registry policy governs the Copilot clients that developers use: the IDEs and Copilot CLI. The cloud agent takes its MCP servers from the MCP configuration of the repository, which a repository administrator maintains, and the registry policy is not enforced there. To govern those servers, control who administers the repository and review the MCP configuration and the agent profiles.",
  takeaway="Registry only covers the IDEs and Copilot CLI. The cloud agent's MCP servers come from the repository's MCP configuration.",
  evidence=[lq("GitHub supports MCP allowlist enforcement at the organization and enterprise level, tied to the Copilot seat that governs the user.", "M3U3"),
            lq("Once a policy is selected, it is applied immediately to all developers.", "M3U3"),
            dn("The reference lists the surfaces on which MCP private registry features are supported. Registry display and allowlist enforcement are supported in Copilot CLI and in the IDEs (VS Code, Visual Studio, JetBrains, Eclipse, Xcode). Both are marked as not supported for Copilot cloud agent. Enforcement applies to both remote and local MCP servers.", "mcp-registry"),
            dn("As a repository administrator, you can configure MCP servers for use within your repository.", "mcp-config")]),
]
