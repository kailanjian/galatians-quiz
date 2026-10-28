# Galatians Quiz
10 random questions per quiz from a bank of ~200 on Paul's letter to the Galatians (ESV), built from the [Matthew Quiz](https://github.com/kailanjian/matthew-quiz) template.

Question types: **which chapter** and **which section** (every section of the letter), **who said / what was the context / which Old Testament passage** (notable quotes), **fill in the blank** (notable verses).
Filter by the letter's three parts: Personal defense (1–2), Doctrinal argument (3–4), Practical living (5–6).
Shortcuts: Cmd/Ctrl+Enter shows the answer; G / P / M grade Got it / Partly / Missed.

## Data
- `data/inventory.json` – 35 short sections typed narrative, argument, illustration, exhortation, greeting or closing. Together they cover every verse of Galatians (1:1–6:18, 149 verses).
- `data/notables.json` – notable quotes (speaker, context, and the Old Testament source for quotes Paul cites), fill-in verses (`[[blank]]` marks the blank), people and places, key events.
- `data/questions.json` – generated; don't edit by hand.

The Index tab in the app lets you browse all of it.

## Commands
- Run locally: `python3 -m http.server`, then open http://localhost:8000
- Rebuild the bank after editing the data: `python3 tools/build_bank.py`
- Validate (verse coverage, refs, ids, bank in sync): `python3 tests/validate_bank.py`

Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved.
