# GH-600 Exam Room

A browser-based exam simulator for GitHub exam GH-600 (Developing in Agentic AI Systems).
Original practice questions, checked against the GH-600 study guide and GitHub Docs. These are not real exam questions.

- `index.html`: the simulator (Exam, Practice and Learn modes). Works offline too.
- `questions.json`: the bank loaded by default.
- `banks/`: more banks; `banks/index.json` lists them in the app.

## Add a bank
1. Add `banks/<name>.json` (format: see "Question file format" at the bottom of the app).
2. Add an entry to `banks/index.json`.
3. Commit to `main`. GitHub Pages republishes automatically.
