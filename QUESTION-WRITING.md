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
- **Format:** spread across `single`, `multiple`, `statements`, `yesno` (problem-solution), `build`, `match`, `dropdown` and `case`. Spread the correct letter evenly. No cues: the correct option isn't the longest, and options are grammatically parallel.
- **Originality:** never copy the module's knowledge-check questions or real exam questions.
- **Density:** 4–6 questions per unit, and every lesson has at least one question (`nugget`, or `also` for a second lesson a question covers).

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
