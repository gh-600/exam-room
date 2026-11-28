"""Quality gate for an exam bank: structure, counts, verbatim quotes, source links, Microsoft-style lint.
Usage: python3 verify.py BANK.json [--expect D1=11,D2=13,...]"""
import json, re, sys, os, glob, collections

BANK = sys.argv[1]
# LEARN_DIR: one file per Learn unit, first line "URL: <unit url>", then the unit text as fetched (not kept in this repository: it is Microsoft's content).
# DOCS_DIR: a clone of github/docs (content/ and data/reusables/).
LEARN_DIR = os.environ.get("GH600_LEARN_DIR", "/home/claude/gh600-exam/learn/")
DOCS_DIR = os.environ.get("GH600_DOCS_DIR", "/home/claude/github/docs/")
bank = json.load(open(BANK))
errs, warns = [], []

def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace(" ", " ")
    s = re.sub(r"[`*\\]", "", s)
    return re.sub(r"\s+", " ", s).strip()

# ---------- screens ----------
screens = []  # (qid, type, domain, obj, parent)
for q in bank["questions"]:
    if q["type"] == "yesno":
        for it in q["items"]:
            screens.append((q["id"] + "/" + it["id"], "yesno", q["domain"], it, q))
    elif q["type"] == "case":
        for s in q["questions"]:
            screens.append((q["id"] + "/" + s["id"], s["type"], s["domain"], s, q))
    else:
        screens.append((q["id"], q["type"], q["domain"], q, None))
print("top-level questions:", len(bank["questions"]), "| screens:", len(screens))
bydom = collections.Counter(d for _, _, d, _, _ in screens)
bytype = collections.Counter(t for _, t, _, _, _ in screens)
print("by domain:", dict(sorted(bydom.items())), {k: "%.1f%%" % (100 * v / len(screens)) for k, v in sorted(bydom.items())})
print("by type:", dict(bytype))
WEIGHTS = {"D1": (15, 20), "D2": (20, 25), "D3": (10, 15), "D4": (15, 20), "D5": (15, 20), "D6": (10, 15)}
for d, (lo, hi) in WEIGHTS.items():
    pct = 100 * bydom[d] / len(screens)
    if not lo <= pct <= hi: errs.append("domain %s is %.1f%%, outside %d-%d%%" % (d, pct, lo, hi))

# ---------- structure ----------
ids = [q["id"] for q in bank["questions"]]
if len(ids) != len(set(ids)): errs.append("duplicate ids")
def all_q():
    for q in bank["questions"]:
        yield q, None
        if q["type"] == "case":
            for s in q["questions"]: yield s, q
letters = collections.Counter()
for q, parent in all_q():
    t, qid = q["type"], (parent["id"] + "/" if parent else "") + q["id"]
    if t in ("single", "multiple"):
        oid = [o["id"] for o in q["options"]]
        if len(oid) != len(set(oid)): errs.append(qid + ": duplicate option ids")
        for a in q["answer"]:
            if a not in oid: errs.append(qid + ": answer not an option")
        if t == "single":
            if len(q["answer"]) != 1: errs.append(qid + ": single needs one answer")
            if len(q["options"]) != 4: warns.append(qid + ": %d options" % len(q["options"]))
            letters["ABCDE"[oid.index(q["answer"][0])]] += 1
        else:
            if q.get("select") != len(q["answer"]): errs.append(qid + ": select mismatch")
        for o in q["options"]:
            r = o.get("rationale", "")
            ok = o["id"] in q["answer"]
            if not r.startswith("Correct." if ok else "Incorrect."): errs.append(qid + "/" + o["id"] + ": rationale prefix doesn't match the key")
    elif t == "statements":
        if len(q["items"]) != 3: warns.append(qid + ": %d statements" % len(q["items"]))
        for it in q["items"]:
            if it["answer"] not in ("yes", "no") or not it.get("explanation"): errs.append(qid + ": bad statement item")
    elif t == "yesno":
        for it in q["items"]:
            if it["answer"] not in ("yes", "no") or not it.get("solution") or not it.get("explanation"): errs.append(qid + ": bad series item")
    elif t == "build":
        iid = [i["id"] for i in q["items"]]
        if not set(q["answer"]) <= set(iid) or len(q["answer"]) >= len(iid): errs.append(qid + ": build needs distractors and valid answer")
    elif t == "match":
        cid = [c["id"] for c in q["choices"]]
        for tg in q["targets"]:
            if tg["answer"] not in cid or not tg.get("rationale"): errs.append(qid + ": bad target")
    elif t == "dropdown":
        names = re.findall(r"\[\[(\w+)\]\]", q["template"])
        if sorted(names) != sorted(q["blanks"]): errs.append(qid + ": blanks don't match the template")
        for k, b in q["blanks"].items():
            if b["answer"] not in b["options"] or not b.get("rationale"): errs.append(qid + ": bad blank " + k)
            if b["options"] != sorted(b["options"]): warns.append(qid + ": options of blank %s aren't in alphabetical order" % k)
    if t != "case":
        for f in ("explanation", "takeaway", "sources", "evidence", "module", "unit", "level", "domain"):
            if not q.get(f): errs.append(qid + ": missing " + f)
print("correct letter for single-answer questions:", dict(sorted(letters.items())))
if max(letters.values()) - min(letters.values()) > 2: warns.append("letters are unevenly spread")

UK_EARLY = r"\b(organis\w+|behaviour\w*|colour\w*|licence\w*|authoris\w+|summaris\w+|analys(e|ed|es|ing)\b|catalogue\w*|centre\w*|favour\w*|programme\w*|whilst|cancelled|cancelling|labelled|modelling|prioritis\w+|recognis\w+|customis\w+|minimis\w+|optimis\w+|serialis\w+|artefact\w*|defence|neighbour\w*)\b"
# ---------- quotes ----------
learn = {}
for f in glob.glob(LEARN_DIR + "m*-u*.md"):
    txt = open(f).read()
    url = txt.split("\n", 1)[0].replace("URL: ", "").strip()
    learn[url] = norm(txt)
docs = {}
for root in ("content", "data/reusables"):
    for dp, _, fs in os.walk(DOCS_DIR + root):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(dp, f)
                docs[p[len(DOCS_DIR):]] = open(p, errors="ignore").read()
docs_norm = {k: norm(v) for k, v in docs.items()}
def doc_file(url):
    path = url.split("docs.github.com/en/")[1].split("#")[0].strip("/")
    for cand in ("content/" + path + ".md", "content/" + path + "/index.md"):
        if cand in docs: return cand
    return None
def includes(page, reusable, depth=0):
    key = "reusables." + reusable[len("data/reusables/"):-3].replace("/", ".")
    txt = docs[page]
    if re.search(re.escape(key) + r"\s*%}", txt): return True
    if depth > 3: return False
    for m in set(re.findall(r"reusables\.([\w.\-]+)\s*%}", txt)):
        sub = "data/reusables/" + m.replace(".", "/") + ".md"
        if sub in docs and includes(sub, reusable, depth + 1): return True
    return False
nq = nn = 0
for q, parent in all_q():
    if q["type"] == "case": continue
    qid = (parent["id"] + "/" if parent else "") + q["id"]
    for s in q["sources"]:
        if "learn.microsoft.com" in s and s not in learn: errs.append(qid + ": Learn unit text not saved for " + s)
        if "docs.github.com" in s and not doc_file(s): errs.append(qid + ": no docs page for " + s)
    for e in q["evidence"]:
        src = e["source"]
        if src not in q["sources"]: errs.append(qid + ": evidence source isn't listed in sources: " + src)
        if "note" in e: nn += 1; continue
        nq += 1
        qt = norm(e["quote"])
        if "learn.microsoft.com" in src:
            if qt not in learn.get(src, ""): errs.append(qid + ": Learn quote not found verbatim: " + e["quote"][:80])
        elif "docs.github.com" in src:
            page = doc_file(src)
            hits = [k for k, v in docs_norm.items() if qt in v]
            if not hits: errs.append(qid + ": docs quote not found: " + e["quote"][:80])
            elif page not in hits and not any(h.startswith("data/reusables/") and page and includes(page, h) for h in hits):
                errs.append(qid + ": docs quote is on another page (%s), not on %s" % (hits[:3], page))
        else:
            errs.append(qid + ": quotation from a source that can't be checked: " + src)
print("evidence: %d verbatim quotes checked, %d documentation summaries" % (nq, nn))

# ---------- lessons ----------
nug = {n["id"]: n for n in bank.get("nuggets", [])}
if nug:
    used = collections.Counter()
    for q, parent in all_q():
        if q["type"] == "case": continue
        qid = (parent["id"] + "/" if parent else "") + q["id"]
        if q.get("nugget") not in nug: errs.append(qid + ": lesson missing or unknown: %s" % q.get("nugget"))
        for x in [q.get("nugget")] + q.get("also", []):
            if x not in nug: errs.append(qid + ": unknown lesson " + str(x))
            used[x] += 1
    order = [(n["module"], n["unit"]) for n in bank["nuggets"]]
    if order != sorted(order): warns.append("lessons aren't in module and unit order")
    for n in bank["nuggets"]:
        if not used[n["id"]]: errs.append(n["id"] + ": lesson without a question")
        for f in ("title", "body", "watch", "skill", "domain", "learn"):
            if not n.get(f): errs.append(n["id"] + ": lesson lacks " + f)
        if n["learn"] not in learn: errs.append(n["id"] + ": Learn unit text not saved for " + n["learn"])
        if (n["status"] == "confirmed") != bool(n.get("depth")): errs.append(n["id"] + ": status and depth disagree")
        if n.get("depth") and not n.get("sources"): errs.append(n["id"] + ": depth without a documentation source")
        for s in n.get("sources", []):
            if "docs.github.com" in s and not doc_file(s): errs.append(n["id"] + ": no docs page for " + s)
        for f in ("title", "body", "example", "depth", "watch"):
            m = re.search(UK_EARLY, n.get(f, ""))
            if m: errs.append(n["id"] + ": British spelling '%s'" % m.group(0))
        if n["body"].count("```") % 2 or n.get("example", "").count("```") % 2: errs.append(n["id"] + ": unbalanced code fence")
    words = sum(len((n["body"] + " " + n.get("example", "") + " " + n.get("depth", "") + " " + n.get("watch", "")).split()) for n in bank["nuggets"])
    print("lessons: %d (%d confirmed in docs, %d from Learn only), %d words, questions per lesson %d-%d" % (len(nug), sum(n["status"] == "confirmed" for n in bank["nuggets"]), sum(n["status"] != "confirmed" for n in bank["nuggets"]), words, min(used.values()), max(used.values())))

# ---------- Microsoft style lint ----------
UK = r"\b(organis\w+|behaviour\w*|colour\w*|licence\w*|authoris\w+|summaris\w+|analys(e|ed|es|ing)\b|catalogue\w*|centre\w*|favour\w*|programme\w*|whilst|cancelled|cancelling|labelled|modelling|prioritis\w+|recognis\w+|customis\w+|minimis\w+|optimis\w+|serialis\w+|artefact\w*|defence)\b"
CLOSERS = r"(What should you (do|use|configure|add|include|recommend|adjust)[^?]*\?|What should the agent do[^?]*\?|What should occur next\?|What (is the cause|stopped the command|produced the block)\?|Which [^?]+\?|How should you complete the [^?]+\?|Where should you store [^?]+\?)"
def text_fields(q):
    out = [q.get("stem", ""), q.get("scenario", ""), q.get("explanation", ""), q.get("takeaway", "")]
    for o in q.get("options", []): out += [o["text"], o["rationale"]]
    for it in q.get("items", []): out += [it.get("statement", ""), it.get("solution", ""), it.get("text", ""), it.get("explanation", "")]
    for tg in q.get("targets", []): out += [tg["text"], tg["rationale"]]
    for b in q.get("blanks", {}).values(): out.append(b["rationale"])
    return out
for q, parent in all_q():
    qid = (parent["id"] + "/" if parent else "") + q["id"]
    for tx in text_fields(q):
        m = re.search(UK, tx)
        if m: errs.append(qid + ": British spelling '%s'" % m.group(0))
        if re.search(r"\b(all|none) of the above\b", tx, re.I): errs.append(qid + ": 'all/none of the above'")
        if re.search(r"\b(we|our|I)\b", tx) and "our" not in ("",): 
            if re.search(r"\b(We|we|I) ", tx): warns.append(qid + ": first person in '%s'" % tx[:50])
    seen = [q.get("stem", ""), q.get("scenario", "")] + [o["text"] for o in q.get("options", [])] + [it.get("statement", "") + it.get("solution", "") + it.get("text", "") for it in q.get("items", [])] + [tg["text"] for tg in q.get("targets", [])]
    for tx in seen:
        m = re.search(r"\b\w+n't\b|\bit's\b", tx)
        if m: errs.append(qid + ": contraction '%s' in candidate-facing text" % m.group(0))
    t = q["type"]
    if t == "case":
        for h in ("### Overview", "### Existing environment", "### Planned changes", "### Technical requirements"):
            if h not in q["scenario"]: errs.append(qid + ": case study lacks section " + h)
        continue
    stem = q.get("stem") or q.get("scenario")
    body = stem.split("NOTE:")[0].strip()
    if t in ("single", "multiple", "match", "build", "dropdown"):
        tail = body.replace("Each correct answer presents part of the solution.", "").replace("Each correct answer presents a complete solution.", "").strip()
        last = tail.split("\n\n")[-1].strip()
        closing = re.split(r"(?<=[.!])\s+", last)[-1]
        if not re.fullmatch(CLOSERS, closing): errs.append(qid + ": closing question isn't a standard one: '%s'" % closing[:90])
        if re.search(r"\b(NOT|EXCEPT|not)\b", closing): errs.append(qid + ": negative closing question")
    if t == "multiple":
        if "Each correct answer presents" not in stem or "NOTE: Each correct selection is worth one point." not in stem: errs.append(qid + ": multiple-answer wording missing")
        word = {2: "two", 3: "three", 4: "four"}[q["select"]]
        if ("Which " + word) not in stem: errs.append(qid + ": the question doesn't say 'Which %s'" % word)
    if t == "statements" and "For each of the following statements, select Yes if the statement is true. Otherwise, select No." not in stem:
        errs.append(qid + ": statements wording missing")
    if t == "build" and not re.search(r"Which (three|four|five) actions should (you perform|be performed) in sequence", stem): errs.append(qid + ": build-list wording")
    if t == "dropdown" and not re.search(r"How should you complete the (workflow|configuration|job)\?$", body): errs.append(qid + ": drop-down wording")
    if t == "yesno":
        if "You need to" not in q["scenario"]: errs.append(qid + ": the series has no 'You need to' goal")
        if q.get("goal"): warns.append(qid + ": custom goal line replaces 'Does this meet the goal?'")
        if len(q["items"]) != 3: warns.append(qid + ": series of %d" % len(q["items"]))
    if t in ("single", "multiple", "dropdown") and not parent and "You need to" not in stem and q["level"] != "understand":
        warns.append(qid + ": no 'You need to' requirement in the stem")
    if t in ("single", "multiple"):
        texts = [o["text"] for o in q["options"]]
        ends = {x.rstrip("*`").endswith(".") for x in texts}
        if len(ends) > 1: errs.append(qid + ": options aren't parallel (some end with a full stop, some don't)")
        if t == "single":
            c = [o for o in q["options"] if o["id"] in q["answer"]][0]
            others = [len(o["text"]) for o in q["options"] if o["id"] not in q["answer"]]
            if len(c["text"]) > 1.45 * max(others): warns.append(qid + ": the correct option is much longer than every distractor (%d vs max %d)" % (len(c["text"]), max(others)))
            if len(c["text"]) < 0.5 * min(others): warns.append(qid + ": the correct option is much shorter than every distractor")
yn = collections.Counter()
for sid, t, d, obj, par in screens:
    if t == "yesno": yn[obj["answer"]] += 1
    if t == "statements":
        for it in obj["items"]: yn["st-" + it["answer"]] += 1
print("yes/no balance:", dict(yn))
levels = collections.Counter(obj.get("level") or par.get("level") for _, _, _, obj, par in screens)
print("levels:", dict(levels), "| recall share: %.0f%%" % (100 * (levels.get("understand", 0) + levels.get("remember", 0)) / len(screens)))
print("\nERRORS (%d)" % len(errs)); [print(" -", e) for e in errs]
print("WARNINGS (%d)" % len(warns)); [print(" -", w) for w in warns]
sys.exit(1 if errs else 0)
