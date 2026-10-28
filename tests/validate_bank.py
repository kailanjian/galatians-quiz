#!/usr/bin/env python3
"""Validate the Galatians data. Run: python3 tests/validate_bank.py
- every verse of Galatians (1:1-6:18) is covered by at least one inventory section
- every ref parses and is in range; ids unique
- questions.json is in sync: which chapter + which section per inventory section, a question per quote,
  an Old Testament question per OT quote, and a fill-in per notable verse"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from galatians import VERSES, verses

D = os.path.join(os.path.dirname(__file__), '..', 'data')
inv = json.load(open(os.path.join(D, 'inventory.json')))
nb = json.load(open(os.path.join(D, 'notables.json')))
bank = json.load(open(os.path.join(D, 'questions.json')))
TYPES = ('narrative', 'argument', 'illustration', 'exhortation', 'greeting', 'closing')
errs = []

covered = set()
for p in inv:
    try: covered |= set(verses(p['ref']))
    except ValueError as e: errs.append(f"{p['id']}: {e}")
    if p['type'] not in TYPES: errs.append(f"{p['id']}: bad type {p['type']!r}")
    if not p.get('title') or not p.get('summary'): errs.append(f"{p['id']}: missing title/summary")
missing = [(c, v) for c in range(1, len(VERSES) + 1) for v in range(1, VERSES[c - 1] + 1) if (c, v) not in covered]
if missing: errs.append('uncovered verses: ' + ', '.join(f'{c}:{v}' for c, v in missing))

for kind, items in (('quote', nb['quotes']), ('verse', nb['verses']), ('event', nb['events'])):
    for x in items:
        for r in x['ref'].split(';'):
            try: verses(r)
            except ValueError as e: errs.append(f'{kind} {x.get("id", x.get("event"))}: {e}')
for n in nb['names']:
    for r in n['refs'].replace(';', ',').split(','):
        try: verses(r)
        except ValueError as e: errs.append(f"name {n['name']}: {e}")

for name, items in (('inventory', inv), ('quotes', nb['quotes']), ('verses', nb['verses']), ('questions', bank)):
    ids = [x['id'] for x in items]
    if len(ids) != len(set(ids)): errs.append(f'duplicate ids in {name}')
all_src = [x['id'] for x in inv + nb['quotes'] + nb['verses']]
if len(all_src) != len(set(all_src)): errs.append('duplicate ids across inventory/quotes/verses')

ids = {q['id'] for q in bank}
need = [f'ch-{p["id"]}' for p in inv] + [f'sec-{p["id"]}' for p in inv] + [f'fill-{v["id"]}' for v in nb['verses']]
need += [f'ot-{q["id"]}' for q in nb['quotes'] if q.get('ot')]
need += [f'ctx-{q["id"]}' if q['speaker'] == 'Paul' else f'who-{q["id"]}' for q in nb['quotes'] if not q['speaker'].startswith('Scripture')]
for i in need:
    if i not in ids: errs.append(f'missing question {i} (rerun tools/build_bank.py)')
sources = {q['source'] for q in bank}
for x in inv + nb['quotes'] + nb['verses']:
    if x['id'] not in sources: errs.append(f"no question for {x['id']} (rerun tools/build_bank.py)")
for q in bank:
    if not q['question'].strip() or not q['answer'].strip(): errs.append(f"empty question/answer {q['id']}")

total = sum(VERSES)
print(f"{len(inv)} sections covering {len(covered)}/{total} verses; {len(nb['quotes'])} quotes, "
      f"{len(nb['verses'])} fill-in verses, {len(nb['names'])} names, {len(nb['events'])} events; {len(bank)} questions")
print('\n'.join(errs) or 'OK'); sys.exit(1 if errs else 0)
