# How GH-600 lessons and questions are written

These are the instructions for generating a module bank (`banks/m<N>.json`) for the Exam Room. They replace the short protocol in `SOURCES.md`, which remains the inventory of sources.

## 1. Roles of the sources

| Role | Source | Decides |
|---|---|---|
| Driver | Microsoft Learn unit (Part 1: M1–M3, Part 2: M4–M6) | What is taught and asked, the scenario style, the vocabulary |
| Verifier and depth | GitHub Docs, gh-aw docs | Whether the answer is true; exact setting names, defaults, limits, failure modes |
| Coverage | GH-600 study guide, *Skills measured* | That every skill bullet is covered, in proportion to its weight |

**Conflict rule:** when the module and GitHub Docs disagree, no question is built on that point. It goes in the bank's `conflicts` list with both versions, and the app shows it under the lessons.

## 2. Three passes per module

1. **Extract.** Read every content unit. Split it into claims: one testable idea each, with the id `M<module>-U<unit>-C<n>`. Each claim becomes a lesson (a "nugget").
2. **Verify.** Check each claim against GitHub Docs and tag it:
   - `confirmed`: Docs agree. Put what Docs add in `depth` and the page in `sources`.
   - `learn-only`: conceptual, or no Docs page was checked. Questions on it stay at the level the module states.
   - conflict: excluded from lessons' claims and from questions; recorded in `conflicts`.
3. **Write.** Write questions from claims, never from memory. Every question carries `module`, `unit`, `nugget` (the claim it tests), `level` and `sources` (the Learn unit first, then Docs).

The fact sheet `sources/m<N>.md` is generated from the bank, so the bank is the single source of truth.

## 3. Writing a lesson

A lesson teaches one claim in under a minute of reading.

- `title`: the claim as a plain statement, not a topic label.
- `body`: 2–3 short paragraphs or a short list. Start from what the learner already knows, say what the thing is, then why it matters for agents.
- `example`: one concrete case, preferably .NET/GitHub flavoured.
- `depth` (only if confirmed): the details Docs add that the module leaves out.
- `watch`: the exam trap, meaning the wrong option this claim usually hides behind.
- Use the module's own terms. Define any term the first time it appears.

## 4. Writing a question

- **One claim per question**, in a scenario written in the unit's style, with a constraint ("least privilege", "must not weaken existing controls", "without slowing delivery") that rules out shortcuts.
- **Cognitive level:** at most 20 % `remember`/`understand` recall of wording. The rest `apply`, `analyse` or `evaluate`: what should you do, why did this fail, does this meet the goal.
- **Distractors:** each one comes from a named source and gets its own `rationale`:
  - a neighbouring concept from the same unit;
  - a control that acts at the wrong moment (merge vs deploy vs tool call vs network);
  - guidance offered as enforcement (an instruction, a comment);
  - a shortcut that loosens a control (bypass list, `write-all`, `pull_request_target`, disabling the firewall);
  - the learner's own error log.
- **Depth:** where the claim is `confirmed`, the correct answer or a distractor should turn on a Docs detail (a default, an exact setting, a failure mode).
- **Format, two tiers:**
  - *Core* (`single`, `statements`, `yesno` problem-solution): about **70 %** of a bank. These test one idea cleanly, and Learn mode's "Test me on this" uses only these. Every lesson needs at least one core question.
  - *Exam format* (`multiple`, `build`, `match`, `dropdown`, `case`): about **30 %**. They practise the mechanics of the real exam and appear in Practice and Exam when "All exam formats" is selected.
  - The tier follows from the type; set `"tier": "core"` or `"tier": "exam"` on a question only to override it.
- **Letters:** spread the correct letter evenly. No cues: the correct option isn't the longest, and options are grammatically parallel.
- **Originality:** never copy the module's knowledge-check questions or real exam questions.
- **Density:** 4–6 questions per unit or more, and every lesson has at least one core question (`nugget`, or `also` for a second lesson a question covers).

## 5. Quality gate before publishing

1. The bank loads in the app with no validation errors.
2. Every `nugget` id exists, and every lesson has a question.
3. Letter distribution and format mix are checked by the build script.
4. Each answer key is re-checked against its `sources`. Anything that can't be verified is removed or marked `learn-only`.
5. A second reader answers the bank without the key. Any disagreement is fixed or the question is dropped. If this pass wasn't independent, say so when the bank is announced.

## 6. Bank format (additions for module banks)

```json
{
  "modules": { "M3": { "title": "…", "url": "…", "units": { "U2": "…" } } },
  "nuggets": [ { "id": "M3-U3-C4", "module": "M3", "unit": "U3", "domain": "D2", "skill": "Configure MCP servers",
                 "status": "confirmed", "title": "…", "body": "…", "example": "…", "depth": "…", "watch": "…",
                 "learn": "https://learn.microsoft.com/…", "sources": ["https://docs.github.com/…"] } ],
  "conflicts": [ { "module": "M3", "unit": "U3", "learnSays": "…", "docsSay": "…", "source": "…" } ],
  "questions": [ { "id": "…", "type": "single", "domain": "D2", "module": "M3", "unit": "U3",
                   "nugget": "M3-U3-C4", "also": [], "level": "apply", "…": "…" } ]
}
```

Question types and their fields are described in the app under "Question file format". `tools/build_m3.py` is the worked example of a module build.

## 7. Microsoft exam style

Applies to full exams (`banks/exam<N>.json`) and to every exam-format question. Module banks may stay closer to the wording of the Learn unit.

**What is official and what isn't.** Microsoft doesn't publish items, and it doesn't say which question types a given exam uses ([Exam duration and exam experience](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience)). Its reference for "style, wording, and difficulty" is the practice assessment, and GH-600 doesn't have one yet. These rules therefore combine three sources of different strength:

- **Documented by Microsoft:** the question types (multiple choice, build list, drag and drop, hot area, case studies), the scoring rules ([Exam scoring and score reports](https://learn.microsoft.com/en-us/credentials/certifications/exam-scoring-reports)) and how problem-solution sets work ([Understanding questions that you can't review](https://learn.microsoft.com/en-us/credentials/certifications/posts/understanding-questions-that-you-cannot-review)).
- **Recalled, not re-fetched:** the fixed wordings that Microsoft uses in its public practice assessments and sample questions. Check them against the [exam sandbox](https://aka.ms/examdemo) when in doubt.
- **One first-hand account of the live GH-600 exam** ([blog post, August 2026](https://sameeraman.github.io/blog/2026/08/09/gh600-exam-reflections/)): 52 questions, one case study of 10, multiple choice, drag and drop, drop-downs and code completion, "not a theory exam". A single source, so it calibrates the mix and nothing more.

**Rules**

1. **Language.** US English, second person, present tense. No contractions in anything the candidate reads before answering (feedback text may use them). GitHub UI labels exactly as in the product, in bold.
2. **Stem.** The situation ("You have a GitHub repository named Repo1 that…"), then what exists or what happened, then the requirement as "You need to…", with a constraint when it rules out a shortcut ("The solution must…", "You must not…"), then one closed question.
3. **Closing question.** One of: "What should you do?", "What should you do first?", "What should you use / configure / add / include / recommend?", "Which … should you …?", "What is the cause?", "How should you complete the workflow / configuration / job?". Never negative ("NOT", "EXCEPT"). Never "all of the above" or "none of the above".
4. **Names.** Placeholders such as Repo1, Org1, RS1 and Server1, and Microsoft's fictitious companies (Contoso, Fabrikam, Litware, Adatum, Northwind Traders). No real people or companies.
5. **Self-contained and fair.** Everything needed is in the stem, and nothing is a trick. A solution that is only a first step, or that meets part of the goal, is wrong.
6. **Options.** Four for a single answer. Grammatically parallel, all sentences or all fragments, of similar length: the key is never the longest by a wide margin. Each distractor is plausible to someone who lacks the skill. Code and settings use exact product syntax.
7. **Wording per type**

   | Type | Wording |
   |---|---|
   | Several answers (`multiple`) | "Which two actions should you perform? Each correct answer presents part of the solution." (or "…a complete solution." when each answer works alone), then "NOTE: Each correct selection is worth one point." |
   | Problem-solution series (`yesno`) | A shared scenario that ends with "You need to…". Each screen shows "Solution: …" and "Does this meet the goal?". Three screens. In Exam mode the app shows Microsoft's series note and locks each screen. |
   | Statements (`statements`) | "For each of the following statements, select Yes if the statement is true. Otherwise, select No." and the NOTE. Three independent statements. Vary the Yes/No pattern from one question to the next. |
   | Build list (`build`) | "Which four actions should you perform in sequence?" The app adds "Move the appropriate actions…". Include one or two actions that don't belong. Exactly one valid order. |
   | Drag and drop (`match`) | "Which X should you use for each Y?" The app adds "Each value may be used once, more than once, or not at all." and the NOTE. |
   | Drop-down and code completion (`dropdown`) | "How should you complete the workflow?" The app adds "To answer, select the appropriate options in the answer area." and the NOTE. Two to four boxes, options in alphabetical order. |
   | Case study (`case`) | Sections: Overview, Existing environment, Planned changes, Problem statements, Technical requirements. Each question starts with "You need to…" and can be answered from the case plus the skill. Eight to ten questions. |

8. **Scoring.** One point for each correctly answered component, and no penalty for guessing. The app scores the same way.
9. **Practical weight.** About a third of the screens or more should show YAML, JSON, a command or a log, in the stem or in the options.

## 8. Full exams

- **Blueprint.** 60 screens, counted as the exam counts them: each item of a series and each case study question is one screen. The domain split stays inside the ranges of the study guide (exam 1: D1 11, D2 13, D3 7, D4 10, D5 10, D6 9; exam 2: D1 10, D2 14, D3 8, D4 10, D5 10, D6 8). About half the screens are single answer and the rest are spread over the other formats, with one case study and two series. At most 20 % recall.
- **New questions only.** Nothing is copied from a module bank, a knowledge check, a third-party test, the sample bank or an earlier full exam.
- **Coverage across exams.** A new exam first covers the study-guide bullets that the earlier exams did not touch, then returns to the others from a different angle. Exam 1 mapped to 42 of the 65 bullets. Exam 2 covers the 23 that were left, so the two exams together touch every bullet, and it has a case study of ten questions and eight drop-down items, because the one first-hand account of the live exam reports a case study of that size and code completion.
- **Evidence.** A Learn excerpt is always verbatim (`quote`). A Docs excerpt is verbatim when the sentence has no template variables; otherwise it is a summary (`note`).
- **Why it may be on the exam.** Every question carries `whyExam`: the study-guide bullet it maps to and the clues that suggest the topic is examinable (the study guide names it, the Learn unit says it is tested or flags it as decision guidance, it is repeated across modules, the unit shows it as code, a candidate reported it from the live exam, GitHub Docs define it precisely, it is a classic trap). "Strong" means the unit says it is tested, a candidate reported it, or at least two of the study guide, emphasis and repetition clues apply. None of these is knowledge of the real item pool. `tools/exam1/why.py` holds them.
- **Lessons.** A full exam can carry lessons for Learn mode (`tools/exam1/lessons.py`): one per concept that the exam tests, written as section 3 describes and ordered by Learn module and unit. Every question names its lesson (`nugget`, plus `also` for a second one), and every lesson has at least one question. "What GitHub Docs adds" holds only facts that were checked in the GitHub Docs source. From a lesson, "Test me on this" shows only that lesson's questions, including single questions of the case study.
- **Cold measurement.** A full exam is published without lessons until the learner has taken it once in Exam mode. From a lesson, "Test me on this" shows the questions of the exam, so lessons would spoil the first attempt. Exam 2 is published this way.
- **Builders.** `tools/exam1/` and `tools/exam2/` each hold one file per domain (`d1.py` to `d6.py`), `case.py`, `lib.py` (source catalogue) and `build.py`.
- **Quality gate.** `verify.py` in the builders' folder must end with no errors before a bank is published. It checks the structure of every question, the 60 screens and the domain weights, the spread of correct letters and of Yes/No answers, that every `quote` is found verbatim in the saved Learn unit or in the GitHub Docs source *and on the page that is cited*, that every Docs link resolves to a page, and the style rules of section 7. It needs a local copy of the Learn unit texts, which isn't kept in this repository because it is Microsoft's content, and a clone of `github/docs`.
- **After the gate.** Load the bank in the app and answer every screen with the key (the score must be 1000). Then read every screen once more as a candidate would. That last pass is done by the author, so say that it isn't independent when the exam is announced.
- **Facts that changed.** When GitHub Docs and an older note disagree, the Docs of the day win, and the fact bank in `SOURCES.md` is corrected in the same commit.
