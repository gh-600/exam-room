"""Shared helpers and source catalogue for the GH-600 full exam 1 builders."""

L = "https://learn.microsoft.com/en-us/training/modules/"
M = {
    "M1": ("foundations-agentic-ai", "Foundations of agentic AI in GitHub"),
    "M2": ("design-agent-architecture-integration", "Design agent architecture and SDLC integration"),
    "M3": ("agent-tooling-mcp-execution-environments", "Agent tooling, MCP and execution environments"),
    "M4": ("multi-agent-systems-orchestration", "Multi-agent systems and orchestration"),
    "M5": ("memory-state-evaluation", "Memory, state and evaluation"),
    "M6": ("governance-guardrails-operations", "Governance, guardrails and operations"),
}
UNITS = {
    "M1U2": "2-define-agentic-ai", "M1U3": "3-explain-agent-lifecycle-plan-act-evaluate",
    "M1U4": "4-describe-github-system-record-control-plane", "M1U5": "5-identify-risks-traceability",
    "M1U6": "6-apply-contributor-model-agent-generated-work",
    "M2U2": "2-agent-responsibilities", "M2U3": "3-inputs-outputs-success-criteria", "M2U4": "4-plan-reason-execution",
    "M2U5": "5-pull-request-governance-controls", "M2U6": "6-reliable-workflows", "M2U7": "7-agent-operations-controls",
    "M3U2": "2-interact-github-apis-workflows", "M3U3": "3-model-context-protocol-servers-registries-allow-lists",
    "M3U4": "4-execution-context-boundaries", "M3U5": "5-agent-execution-limits-protections",
    "M4U2": "2-multi-agent-responsibilities", "M4U3": "3-agent-orchestration-github-workflows",
    "M4U4": "4-execution-isolation-permissions-concurrency", "M4U5": "5-conflict-resolution-github-arbitration",
    "M4U6": "6-system-observability-evidence-workflows", "M4U7": "7-scale-failure-recovery",
    "M5U2": "2-agent-memory-strategies", "M5U3": "3-agent-state-context-drift", "M5U4": "4-memory-state-continuity",
    "M5U5": "5-evaluation-signals-quality-gates", "M5U6": "6-agent-failures-behavior-improvement",
    "M6U2": "2-define-risk-based-autonomy", "M6U3": "3-enforce-governance-github-controls",
    "M6U4": "4-design-human-workflows", "M6U5": "5-control-agent-capabilities",
    "M6U6": "6-make-actions-observable-traceable-auditable", "M6U7": "7-maintain-governance-operational-reliability",
}


def learn(key):
    return L + M[key[:2]][0] + "/" + UNITS[key]


G = "https://docs.github.com/en/"
DOCS = {
    "concurrency": G + "actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency",
    "syntax": G + "actions/reference/workflows-and-actions/workflow-syntax",
    "events": G + "actions/reference/workflows-and-actions/events-that-trigger-workflows",
    "conditions": G + "actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions",
    "status-checks": G + "pull-requests/reference/status-checks",
    "retention": G + "repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository",
    "remove-artifacts": G + "actions/how-tos/manage-workflow-runs/remove-workflow-artifacts",
    "store-data": G + "actions/tutorials/store-and-share-data",
    "github-token": G + "actions/concepts/security/github_token",
    "trigger": G + "actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow",
    "job-outputs": G + "actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs",
    "environments": G + "actions/reference/workflows-and-actions/deployments-and-environments",
    "control-deployments": G + "actions/how-tos/deploy/configure-and-manage-deployments/control-deployments",
    "manage-environments": G + "actions/how-tos/deploy/configure-and-manage-deployments/manage-environments",
    "codeowners": G + "repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners",
    "rules": G + "repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets",
    "ruleset-bypass": G + "repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository",
    "branch-protection": G + "repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule",
    "agent-risks": G + "copilot/concepts/security-governance-and-network-settings/risks-and-mitigations",
    "copilot-on-github": G + "copilot/concepts/copilot-surfaces/copilot-on-github",
    "copilot-cli": G + "copilot/concepts/copilot-surfaces/copilot-cli",
    "custom-agents": G + "copilot/reference/custom-agents-configuration",
    "hooks": G + "copilot/concepts/customizations/hooks",
    "hooks-ref": G + "copilot/reference/hooks-reference",
    "mcp-config": G + "copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers",
    "agent-env": G + "copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment",
    "agent-resources": G + "copilot/tutorials/cloud-agent/give-access-to-resources",
    "firewall": G + "copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall",
    "mcp-registry": G + "copilot/reference/enterprise-administrators/mcp-private-registry-enforcement",
    "agent-task": G + "copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli",
    "dependency-review": G + "code-security/concepts/supply-chain-security/dependency-review",
    "protect-threats": G + "code-security/tutorials/secure-your-organization/protect-against-threats",
    "audit-log": G + "organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/audit-log-events-for-your-organization",
    "oidc": G + "actions/concepts/security/openid-connect",
    "oidc-azure": G + "actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure",
    "memory": G + "copilot/concepts/prompting-and-context/copilot-memory",
    "gh-aw-faq": "https://github.github.com/gh-aw/reference/faq/",
    "gh-aw-how": "https://github.github.com/gh-aw/introduction/how-they-work/",
}

YESNO = "For each of the following statements, select Yes if the statement is true. Otherwise, select No.\n\nNOTE: Each correct selection is worth one point."
PART = "Each correct answer presents part of the solution.\n\nNOTE: Each correct selection is worth one point."
POINT = "NOTE: Each correct selection is worth one point."


def opt(i, text, why):
    return {"id": i, "text": text, "rationale": why}


def lq(text, key):
    """Verbatim quotation from a Microsoft Learn unit (checked by verify.py)."""
    return {"quote": text, "source": learn(key), "label": "Microsoft Learn · %s, unit %s" % (key[:2], key[3:])}


def dq(text, doc):
    """Verbatim quotation from GitHub Docs (checked by verify.py against the docs source)."""
    return {"quote": text, "source": DOCS[doc], "label": "GitHub Docs"}


def dn(text, doc):
    """Summary of what the documentation says (not a quotation)."""
    return {"note": text, "source": DOCS[doc], "label": "GitHub Agentic Workflows docs" if doc.startswith("gh-aw") else "GitHub Docs"}


def Q(qid, typ, domain, key, level, **kw):
    """key is the driving Learn unit, for example 'M4U3'."""
    q = {"id": qid, "type": typ, "domain": domain, "module": key[:2], "unit": key[2:], "level": level}
    docs = kw.pop("docs", [])
    extra = kw.pop("also_units", [])
    q.update(kw)
    q["sources"] = [learn(key)] + [learn(k) for k in extra] + [DOCS[d] for d in docs]
    return q
