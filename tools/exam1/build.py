"""Assemble banks/exam1.json from the domain builders. Usage: python3 build.py OUT.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import M, UNITS, learn
import d1, d2, d3, d4, d5, d6, case

UNIT_TITLES = {
    "M1": {"U2": "Define agentic AI in the SDLC", "U3": "Explain the agent lifecycle: plan, act, evaluate", "U4": "Describe GitHub as the system of record and control plane",
           "U5": "Identify responsibilities, risks, anti-patterns, and traceability needs", "U6": "Apply the contributor model to agent-generated work"},
    "M2": {"U2": "Map agent responsibilities to the SDLC", "U3": "Define inputs, outputs, and success criteria", "U4": "Separate planning, reasoning, and execution",
           "U5": "Pull request governance controls", "U6": "Build reliable workflows", "U7": "Control and operate agents"},
    "M3": {"U2": "How agents interact with GitHub APIs and workflows", "U3": "MCP servers, registries, and allow lists", "U4": "Execution context and boundaries",
           "U5": "Agent execution limits and protections"},
    "M4": {"U2": "Define multi-agent responsibilities in the SDLC", "U3": "Orchestrate agents using GitHub workflows", "U4": "Isolate execution",
           "U5": "Detect and resolve conflicts", "U6": "Make the system observable", "U7": "Operate reliably at scale"},
    "M5": {"U2": "Implement agent memory strategies", "U3": "Persist agent state and manage context drift", "U4": "Ensure continuity across tools and environments",
           "U5": "Define evaluation signals and enforce quality gates", "U6": "Analyze agent failures and improve behavior"},
    "M6": {"U2": "Define risk-based autonomy and action boundaries", "U3": "Enforce governance with GitHub controls", "U4": "Design human-in-the-loop workflows",
           "U5": "Control agent capabilities using least privilege", "U6": "Make actions observable, traceable, and auditable", "U7": "Maintain governance and operational reliability"},
}
DOMAINS = {
    "D1": "Agent architecture and SDLC",
    "D2": "Tool use and environment interaction",
    "D3": "Memory, state and execution",
    "D4": "Evaluation, error analysis and tuning",
    "D5": "Multi-agent coordination",
    "D6": "Guardrails and accountability",
}
import re
CONTR = {"doesn't": "does not", "don't": "do not", "isn't": "is not", "aren't": "are not", "hasn't": "has not", "haven't": "have not", "can't": "cannot",
         "won't": "will not", "didn't": "did not", "wasn't": "was not", "weren't": "were not", "shouldn't": "should not", "couldn't": "could not", "it's": "it is"}
def formal(t):
    """Microsoft exam items don't use contractions. Feedback text keeps them."""
    def sub(m):
        w = m.group(0); r = CONTR[w.lower()]
        return r[0].upper() + r[1:] if w[0].isupper() else r
    return re.sub(r"\b(" + "|".join(re.escape(k) for k in CONTR) + r")\b", sub, t, flags=re.I)
def formalize(q):
    for k in ("stem", "scenario"):
        if k in q: q[k] = formal(q[k])
    for o in q.get("options", []): o["text"] = formal(o["text"])
    for it in q.get("items", []):
        for k in ("statement", "solution", "text"):
            if k in it: it[k] = formal(it[k])
    for tg in q.get("targets", []): tg["text"] = formal(tg["text"])
    for sub in q.get("questions", []): formalize(sub)
for mod in (d1, d2, d3, d4, d5, d6):
    for q in mod.QUESTIONS: formalize(q)
formalize(case.CASE)

# Interleave the domains so that a fixed-order run doesn't group them; the case study closes the exam.
pools = [list(m.QUESTIONS) for m in (d2, d1, d5, d4, d6, d3)]
order = []
while any(pools):
    for p in pools:
        if p:
            order.append(p.pop(0))
questions = order + [case.CASE]

CONFLICTS = [
    {"module": "M4", "unit": "U4", "learnSays": "Job-level `concurrency` only applies within a workflow run, not across runs.",
     "docsSay": "`jobs.<job_id>.concurrency` ensures that only a single job or workflow using the same concurrency group runs at a time, across runs.",
     "source": "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax"},
    {"module": "M6", "unit": "U4", "learnSays": "Production deployments are serialized with `concurrency: group: production` and `cancel-in-progress: true`.",
     "docsSay": "`cancel-in-progress: true` cancels the run that is already in progress when a new one starts. Without it, the new run waits as pending.",
     "source": "https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency"},
    {"module": "M6", "unit": "U3", "learnSays": "A `preToolUse` hook is one JSON object with `hook`, `tools` and `rules`; a guardrail workflow tests for `github-copilot[bot]`; `copilot agent run CodeAgent --allow-tool 'read,search'` gates tools.",
     "docsSay": "Hook files use `version: 1` with a `hooks` object and commands that return a `permissionDecision`. The examples in the module are illustrative; check the hooks reference and the Copilot CLI reference for real syntax.",
     "source": "https://docs.github.com/en/copilot/reference/hooks-reference"},
    {"module": "M3", "unit": "U5", "learnSays": "Copilot in the cloud only has access to the repository where it is working.",
     "docsSay": "That holds for sessions that run on GitHub Actions. Sessions that run in a cloud sandbox can work across multiple repositories.",
     "source": "https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github"},
]

bank = {
    "title": "GH-600 · Full exam 1 · 60 questions",
    "version": 1,
    "author": "Claude. Questions follow the Microsoft Learn modules for GH-600; answers checked against the GitHub Docs source of 26 November 2026. Not reviewed by an independent expert.",
    "passingScore": 700,
    "durationMinutes": 120,
    "domains": DOMAINS,
    "modules": {k: {"title": v[1], "url": "https://learn.microsoft.com/en-us/training/modules/" + v[0] + "/", "units": UNIT_TITLES[k]} for k, v in M.items()},
    "conflicts": CONFLICTS,
    "questions": questions,
}
out = sys.argv[1] if len(sys.argv) > 1 else "exam1.json"
json.dump(bank, open(out, "w"), ensure_ascii=False, indent=1)
print("written", out, len(questions), "questions")
