"""Domain 2 · Tool use and environment interaction (Learn module 3, with module 1 and 2 units on controls). Eleven standalone screens."""
from lib import Q, opt, lq, dq, dn, YESNO

QUESTIONS = [

Q("x1-d2-mcp-secret-series", "yesno", "D2", "M2U7", "evaluate", also_units=["M3U3"], docs=["mcp-config", "agent-resources"],
  scenario="You add a remote MCP server named Server1 to the MCP configuration of GitHub Copilot cloud agent for a GitHub repository named Repo1. Server1 requires an API key in the `Authorization` header.\n\n"
           "You need to ensure that the agent can authenticate to Server1. The API key must not appear in plain text in the MCP configuration or in any file in the repository.",
  items=[
      {"id": "s1", "solution": "You create a GitHub Actions repository secret named `SERVER1_API_KEY`, and you reference it in the `headers` of the MCP configuration.", "answer": "no",
       "explanation": "The cloud agent can't read secrets that were created for GitHub Actions. It has its own Agents secrets."},
      {"id": "s2", "solution": "You create an Agents secret named `COPILOT_MCP_SERVER1_API_KEY`, and you reference it in the `headers` of the MCP configuration as `$COPILOT_MCP_SERVER1_API_KEY`.", "answer": "yes",
       "explanation": "An Agents secret whose name starts with `COPILOT_MCP_` is available to the MCP configuration, and the key itself stays out of the configuration."},
      {"id": "s3", "solution": "You create an Agents secret named `SERVER1_API_KEY`, and you reference it in the `headers` of the MCP configuration as `$SERVER1_API_KEY`.", "answer": "no",
       "explanation": "It is an Agents secret, but only names that start with `COPILOT_MCP_` are passed to the MCP configuration."},
  ],
  explanation="The agent's runtime has its own secret boundary. Secrets for GitHub Actions, Codespaces and Dependabot aren't visible to it. An MCP server gets a credential only from an Agents secret or variable whose name starts with `COPILOT_MCP_`, referenced from the configuration, so the token is injected at run time and never stored in the configuration.",
  takeaway="MCP credential for the cloud agent = an Agents secret named `COPILOT_MCP_…`.",
  evidence=[lq("\"The agent's runtime environment has its own secret boundary; don't assume it automatically inherits repository CI secrets.\"", "M2U7"),
            lq("Authentication: tokens should be injected at runtime via protected secret boundaries.", "M2U7"),
            dq("Only Agents secrets and variables with names prefixed with `COPILOT_MCP_` will be available to your MCP configuration.", "mcp-config")]),

Q("x1-d2-setup-steps", "single", "D2", "M3U5", "apply", docs=["agent-env"],
  stem="GitHub Copilot cloud agent works on a .NET repository named Repo1. In each session, the agent spends several minutes discovering and installing the .NET SDK and restoring NuGet packages, and the installation sometimes fails.\n\n"
       "You need to preinstall the tools and the dependencies in the agent's environment before the agent starts working. What should you do?",
  options=[
      opt("a", "Add the installation commands to the custom instructions file of the repository.", "Incorrect. Instructions tell the agent what to run. The agent would still install everything itself during the session, by trial and error."),
      opt("b", "Add a `preToolUse` hook that installs the SDK and the packages before each tool call.", "Incorrect. A `preToolUse` hook approves or denies a tool call. It isn't the place to build the environment."),
      opt("c", "Add a `copilot-setup-steps.yml` workflow file that installs them, and commit it to the default branch.", "Correct. The steps of its `copilot-setup-steps` job run in the agent's environment before the agent starts, so the SDK and the packages are already there."),
      opt("d", "Create a workflow that runs on `push` and caches the NuGet packages for later runs.", "Incorrect. That workflow runs in its own runner for its own event. It doesn't prepare the environment of an agent session."),
  ],
  answer=["c"],
  explanation="The cloud agent works in an ephemeral environment that is powered by GitHub Actions. You prepare that environment with a workflow file at a fixed path that contains a single job with a fixed name, `copilot-setup-steps`. The file must exist on the default branch.",
  takeaway="Prepare the agent's environment with `copilot-setup-steps.yml`: fixed path, fixed job name, default branch.",
  evidence=[lq("On GitHub, Copilot in the cloud works in a GitHub Actions-powered environment, creates changes on a branch, and prepares those changes for review.", "M3U5"),
            dn("You customize Copilot's environment with a workflow file located at `.github/workflows/copilot-setup-steps.yml`. It must contain a single `copilot-setup-steps` job, whose steps run before Copilot starts working, and it won't trigger unless it is present on the default branch.", "agent-env")]),

Q("x1-d2-mcp-config", "dropdown", "D2", "M3U3", "apply", also_units=["M2U7"], docs=["mcp-config"],
  stem="You are adding a remote MCP server for a ticketing system to the MCP configuration of GitHub Copilot cloud agent for a GitHub repository named Repo1. The agent must be able to use only the tools named `get_ticket` and `search_tickets`.\n\n"
       "You need to configure the MCP server for the agent.\n\n"
       "How should you complete the configuration?",
  template="{\n  \"[[root]]\": {\n    \"tickets\": {\n      \"type\": \"[[type]]\",\n      \"[[endpoint]]\": \"https://mcp.contoso.com/tickets\",\n      \"tools\": [\"get_ticket\", \"search_tickets\"]\n    }\n  }\n}\n",
  blanks={
      "root": {"options": ["mcpServers", "servers", "tools"], "answer": "mcpServers",
               "rationale": "The cloud agent's configuration is a JSON object with an `mcpServers` object, in which each key is a server name. `servers` is the root key of the VS Code configuration file."},
      "type": {"options": ["http", "local", "stdio"], "answer": "http",
               "rationale": "A remote server is reached over the network. `local` and `stdio` start a process from a `command` with `args`."},
      "endpoint": {"options": ["args", "command", "url"], "answer": "url",
                   "rationale": "A remote server requires `url`. `command` and `args` are the required keys of a local server."},
  },
  explanation="An MCP server exposes tools, and the configuration decides which of them the agent gets. For the cloud agent, every server needs `type` and `tools`. A remote server also needs `url`, and a local one needs `command` and `args`. Listing the two read-only tools, and not `*`, keeps the agent's reach narrow, which matters because the agent uses configured tools without asking for approval.",
  takeaway="Cloud agent MCP: `mcpServers` → server → `type`, `tools`, and `url` or `command` with `args`.",
  evidence=[lq("Namespace control: prefer enabling a narrow tool subset rather than broad wildcards.", "M2U7"),
            lq("A remote MCP server is hosted elsewhere and accessed over the network.", "M3U3"),
            dq("The JSON must contain an `mcpServers` object, where the key is the name of the MCP server (for example, `sentry`), and the value is an object with the configuration for that MCP server.", "mcp-config")]),

Q("x1-d2-app-token", "single", "D2", "M3U5", "analyse", docs=["trigger", "github-token"],
  stem="A scheduled workflow in a GitHub repository named Repo1 runs an agent that commits generated documentation to a branch by using the `GITHUB_TOKEN`. A second workflow that runs on `push` and publishes the documentation never starts after these commits.\n\n"
       "You need to ensure that the publishing workflow runs after the agent's commits. The solution must not use long-lived personal credentials.\n\n"
       "What should you do?",
  options=[
      opt("a", "Grant the `contents: write` permission to the `GITHUB_TOKEN`.", "Incorrect. The token can already push. The limit is that events caused by `GITHUB_TOKEN` don't start new workflow runs."),
      opt("b", "Push the commits by using an installation access token of a GitHub App.", "Correct. A push made with an app token creates the `push` event that starts the workflow, and the token is short-lived and not tied to a person."),
      opt("c", "Push the commits by using a personal access token of a repository administrator.", "Incorrect. It would trigger the workflow, but it is a long-lived personal credential."),
      opt("d", "Change the trigger of the publishing workflow from `push` to `pull_request`.", "Incorrect. No pull request is involved, so the workflow would still not start."),
  ],
  answer=["b"],
  explanation="Events that are triggered with the repository's `GITHUB_TOKEN` don't create new workflow runs, which protects against recursive runs. To start one workflow from another on purpose, use a different credential. A GitHub App installation token does that without a personal credential, and the design must then avoid loops.",
  takeaway="`GITHUB_TOKEN` pushes don't trigger workflows. Use a GitHub App token when one must.",
  evidence=[lq("Most actions performed with this token don't trigger extra workflow runs, which helps prevent unintended loops or repeated execution.", "M3U5"),
            lq("Other authentication methods, such as GitHub App tokens or personal access tokens (PATs), can trigger extra workflow runs depending on configuration.", "M3U5"),
            dq("For example, if a workflow run pushes code using the repository's `GITHUB_TOKEN`, a new workflow will not run even when the repository contains a workflow configured to run when `push` events occur.", "trigger")]),

Q("x1-d2-approve-workflows", "single", "D2", "M1U4", "apply", docs=["agent-risks"],
  stem="GitHub Copilot cloud agent opens a pull request in a GitHub repository named Repo1. The repository uses the default settings for the agent. On the pull request, the CI workflow hasn't started.\n\n"
       "You review the changes and find no problems. You need to run the CI workflow for the pull request. What should you do?",
  options=[
      opt("a", "Ask the agent to push an empty commit to the branch of the pull request.", "Incorrect. A new commit from the agent is held back in the same way."),
      opt("b", "Close the pull request and reopen it.", "Incorrect. Reopening doesn't approve the runs. They still wait for a person."),
      opt("c", "Add Copilot as a bypass actor in the ruleset for `main`.", "Incorrect. A ruleset bypass concerns branch rules. It has nothing to do with the approval of workflow runs."),
      opt("d", "Select **Approve and run workflows** as a user who has write access.", "Correct. By default, workflows don't run on the agent's code until a user with write access has reviewed it and approves the runs."),
  ],
  answer=["d"],
  explanation="Workflows can have access to secrets and to a token with write permissions, so code written by an agent is treated as untrusted until a person has looked at it. By default the runs wait for **Approve and run workflows**. The repository can be configured to run them automatically, which is a decision about risk.",
  takeaway="CI not starting on an agent pull request → a user with write access must approve the runs.",
  evidence=[lq("In some agent PR workflows, a human may need to explicitly approve running workflows (for example, an \"Approve and run workflows\" action). This is a built-in guardrail: it reduces the risk of privileged workflows running automatically for untrusted changes.", "M1U4"),
            dn("By default, workflows are not triggered until Copilot cloud agent's code is reviewed and a user with write access to the repository clicks the **Approve and run workflows** button. Optionally, you can configure Copilot to allow workflows to run automatically.", "agent-risks")]),

Q("x1-d2-hook-events", "match", "D2", "M2U7", "apply", docs=["hooks"],
  stem="You are adding repository hooks for GitHub Copilot CLI in `.github/hooks/`.\n\nWhich hook should you use for each requirement?",
  choices=[{"id": "pre", "text": "`preToolUse`"}, {"id": "post", "text": "`postToolUse`"},
           {"id": "err", "text": "`errorOccurred`"}, {"id": "start", "text": "`sessionStart`"}],
  targets=[
      {"id": "t1", "text": "Record the result of every tool call for an audit trail.", "answer": "post",
       "rationale": "`postToolUse` runs after a tool completes, whether it succeeded or failed, so it can log the result."},
      {"id": "t2", "text": "Send an alert when the agent's run fails with an error.", "answer": "err",
       "rationale": "`errorOccurred` runs when an error occurs during agent execution."},
      {"id": "t3", "text": "Block a shell command that matches a destructive pattern before it runs.", "answer": "pre",
       "rationale": "`preToolUse` runs before the agent uses a tool, and it can approve or deny the execution."},
      {"id": "t4", "text": "Write an audit record when a new agent session begins.", "answer": "start",
       "rationale": "`sessionStart` runs when a session begins or is resumed."},
  ],
  explanation="A hook runs code at a fixed point of the agent's execution, independently of the model. Only a hook that runs before the tool call can stop it, which makes `preToolUse` the enforcement point. The hooks that run afterwards observe: they log results, report errors and record sessions.",
  takeaway="Block with `preToolUse`. Log with `postToolUse`. Alert with `errorOccurred`.",
  evidence=[lq("Pre-action hooks Validate or block unsafe actions before execution", "M2U7"),
            lq("Post-action hooks Log tool usage, outputs, or decisions for auditing", "M2U7"),
            lq("Error hooks Capture failures and trigger escalation or alerting", "M2U7"),
            dn("Hook events include `sessionStart` (a session begins or is resumed), `preToolUse` (before the agent uses any tool; it can approve or deny tool executions), `postToolUse` (after a tool completes, whether successful or failed) and `errorOccurred` (an error occurs during agent execution). Repository hooks are defined in `.github/hooks/*.json`.", "hooks")]),

Q("x1-d2-cloud-agent-statements", "statements", "D2", "M3U5", "understand", docs=["agent-risks", "firewall"],
  stem="GitHub Copilot cloud agent is enabled for a GitHub repository named Repo1 with the default settings. A ruleset for `main` requires one approving review.\n\n" + YESNO,
  items=[
      {"id": "s1", "statement": "The agent's changes are pushed to a separate branch and not directly to the default branch.", "answer": "yes",
       "explanation": "The agent works on its own branch, so every change is isolated until it has been reviewed."},
      {"id": "s2", "statement": "The user who asked the agent to create a pull request can provide the required approval for that pull request.", "answer": "no",
       "explanation": "That user is prevented from approving it, so that the required approval comes from someone else."},
      {"id": "s3", "statement": "The agent's firewall restricts the network access of every MCP server that is configured for the repository.", "answer": "no",
       "explanation": "The firewall covers processes that the agent starts through its Bash tool. It doesn't apply directly to the MCP servers that you configure."},
  ],
  explanation="The cloud agent runs inside built-in limits: it pushes only to its own branch, it can't approve or merge, and the person who started the task can't approve the result. Its firewall limits internet access for the commands that the agent runs, but its coverage is partial, so it isn't a complete security boundary.",
  takeaway="Own branch, no self-approval, no approval by the requester. The firewall doesn't cover your MCP servers.",
  evidence=[lq("Its changes are made on a separate branch, not directly on the default branch such as main.", "M3U5"),
            dn("GitHub prevents the user who asked Copilot cloud agent to create a pull request from approving it, which maintains the expected controls of the required approvals rule and branch protection.", "agent-risks"),
            dn("The firewall applies to processes started by the agent through its Bash tool. It does not apply directly to other MCP servers.", "firewall")]),

Q("x1-d2-hook-log", "single", "D2", "M4U7", "analyse", docs=["hooks", "hooks-ref"],
  stem="An agent session in a GitHub repository named Repo1 stops. The session log ends with the following lines.\n\n"
       "```text\nError: Command blocked by policy\nReason: destructive_operation_detected\n[agent] Escalating to human review...\n```\n\n"
       "The repository contains hook configuration files in `.github/hooks/`.\n\n"
       "You need to identify the control that stopped the command. What stopped the command?",
  options=[
      opt("a", "A `preToolUse` hook that denied the tool call before it ran", "Correct. The command was blocked before execution, with a policy reason. Only a hook that runs before the tool call can do that."),
      opt("b", "A `postToolUse` hook that reported the result of the command", "Incorrect. A `postToolUse` hook runs after the tool has completed, so it can't prevent the command."),
      opt("c", "The agent's firewall", "Incorrect. The firewall blocks network requests to hosts that aren't allowed. It doesn't classify a command as destructive."),
      opt("d", "A ruleset that targets the default branch", "Incorrect. A ruleset rejects pushes and merges. It doesn't see the commands that an agent runs in its session."),
  ],
  answer=["a"],
  explanation="The log shows a block before execution, a policy reason and a handoff to a person. That is the signature of a pre-execution hook: `preToolUse` receives the requested tool call and can deny it. In the cloud agent nobody is present to answer a prompt, so a hook decision of `ask` is treated as `deny`.",
  takeaway="\"Blocked by policy\" before execution → a `preToolUse` hook.",
  evidence=[lq("This pre-execution (preToolUse) hook ensures risky actions, like deleting infrastructure, trigger a human handoff.", "M4U7"),
            dn("`preToolUse` is executed before the agent uses any tool and can approve or deny tool executions. `postToolUse` is executed after a tool completes. Under cloud agent, a `permissionDecision` of `ask` is treated as `deny`, because no user is available to answer.", "hooks-ref")]),

Q("x1-d2-lock-file", "single", "D2", "M3U2", "analyse", docs=["gh-aw-faq", "gh-aw-how"],
  stem="A GitHub repository named Repo1 contains a GitHub Agentic Workflow in the file `daily-report.md`. You change the `safe-outputs` section of the frontmatter so that the workflow adds a label to the issues that it creates, and you commit only the Markdown file. The next scheduled run uses the previous configuration.\n\n"
       "You need to apply the new configuration. What should you do?",
  options=[
      opt("a", "Re-run the last workflow run with debug logging enabled.", "Incorrect. A re-run executes the same compiled workflow again."),
      opt("b", "Compile the workflow again, and commit the updated lock file.", "Correct. GitHub Actions executes the compiled lock file, and frontmatter is embedded in it at compile time."),
      opt("c", "Grant the `issues: write` permission to the agent job in the frontmatter.", "Incorrect. The agent job stays read-only by design. Writes go through safe outputs, and a frontmatter change would again need compiling."),
      opt("d", "Add a `workflow_dispatch` trigger to the frontmatter, and start the workflow manually.", "Incorrect. The trigger is frontmatter too, so it has no effect until the workflow is compiled, and a manual run would use the old lock file."),
  ],
  answer=["b"],
  explanation="An agentic workflow has two parts: frontmatter for configuration, such as triggers, permissions, tools and safe outputs, and Markdown instructions. GitHub Actions doesn't run the Markdown file. It runs the lock file that is compiled from it, so a change to the frontmatter takes effect only after you compile again and commit both files.",
  takeaway="Changed the frontmatter of an agentic workflow → recompile and commit the lock file.",
  evidence=[lq("The workflow is then compiled into a lock file that GitHub Actions executes.", "M3U2"),
            lq("Frontmatter for configuration such as triggers, permissions, tools, and safe outputs", "M3U2"),
            dn("Frontmatter (tools, permissions, triggers, network rules) is embedded at compile time and requires `gh aw compile` after edits. The Markdown body is loaded at run time, so edits to it take effect on the next run. Commit both files.", "gh-aw-faq")]),
]
