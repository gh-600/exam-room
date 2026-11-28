# GH-600 Exam Room

A browser-based exam simulator for GitHub exam GH-600 (Developing in Agentic AI Systems).
Original practice questions, checked against the GH-600 study guide and GitHub Docs. These are not real exam questions.

- `index.html`: the simulator (Exam, Practice and Learn modes). Works offline too.
- `questions.json`: the bank loaded by default (the 6-question sample, `banks/sample.json`).
- `banks/`: more banks; `banks/index.json` lists them in the app. Module banks with lessons for Learn mode will be added per module.
- `QUESTION-WRITING.md`: how lessons and questions are written. `SOURCES.md`: the source inventory.
- `banks/exam1.json`: full exam 1, 60 questions in Microsoft exam style across the six domains, with one case study, and 50 lessons for Learn mode (one per concept that the exam tests).
- `banks/exam2.json`: full exam 2, 60 new questions with a case study of ten questions and more YAML, JSON and command-line items. It has no lessons yet, so that it can be taken cold in Exam mode.
- `tools/`: build scripts. `build_m3.py` regenerates the former Module 3 bank (`python3 tools/build_m3.py`) if it is needed again. `tools/exam1/` and `tools/exam2/`: the builders of the full exams and `verify.py`, their quality gate.

## Add a bank
1. Add `banks/<name>.json` (format: see "Question file format" at the bottom of the app).
2. Add an entry to `banks/index.json`.
3. Commit to `main`. GitHub Pages republishes automatically.
