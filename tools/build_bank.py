#!/usr/bin/env python3
"""Generate data/questions.json from data/inventory.json + data/notables.json.
Run: python3 tools/build_bank.py"""
import json, os, re
from galatians import verses, section, SECTIONS

D = os.path.join(os.path.dirname(__file__), '..', 'data')
inv = json.load(open(os.path.join(D, 'inventory.json')))
nb = json.load(open(os.path.join(D, 'notables.json')))
PARTS = ' or '.join(label for _, _, label in SECTIONS)

def chapter(ref): return verses(ref)[0][0]
def base(id_, type_, ref, q, a, source):
    ch = chapter(ref)
    return {'id': id_, 'type': type_, 'question': q, 'answer': a, 'reference': f'Galatians {ref}',
            'chapter': ch, 'section': section(ch), 'source': source}

bank = []
for p in inv:
    ch = chapter(p['ref'])
    bank.append(base(f"ch-{p['id']}", 'which_chapter', p['ref'],
        f"Which chapter? ({p['type']}) {p['title']}",
        f"Chapter {ch}. {p['summary']}", p['id']))
    bank.append(base(f"sec-{p['id']}", 'which_section', p['ref'],
        f"Which section: {PARTS}? ({p['type']}) {p['title']}",
        f"{section(ch)}, chapter {ch}. {p['summary']}", p['id']))

for q in nb['quotes']:
    paul = q['speaker'] == 'Paul'
    if paul:
        bank.append(base(f"ctx-{q['id']}", 'context', q['ref'],
            f"What was the context? Paul wrote: “{q['text']}”",
            f"{q['context']} (Chapter {chapter(q['ref'])})", q['id']))
    elif not q['speaker'].startswith('Scripture'):
        bank.append(base(f"who-{q['id']}", 'who_said', q['ref'],
            f"Who said: “{q['text']}”",
            f"{q['speaker']}. {q['context']}", q['id']))
    if q.get('ot'):
        bank.append(base(f"ot-{q['id']}", 'ot_passage', q['ref'],
            f"Which Old Testament passage is Paul quoting? “{q['text']}”",
            f"{q['ot']}. {q['context']}", q['id']))

for v in nb['verses']:
    blanks = re.findall(r'\[\[(.+?)\]\]', v['text'])
    assert blanks, v['id']
    prompt = re.sub(r'\[\[(.+?)\]\]', lambda m: '_' * max(6, min(16, len(m[1]))), v['text'])
    full = re.sub(r'\[\[(.+?)\]\]', r'\1', v['text'])
    bank.append(base(f"fill-{v['id']}", 'fill_blank', v['ref'],
        f"Fill in the blank{'s' if len(blanks) > 1 else ''} (Galatians {v['ref']}): “{prompt}”",
        f"{' / '.join(blanks)}. Full verse: “{full}”", v['id']) | {'blanks': blanks})

json.dump(bank, open(os.path.join(D, 'questions.json'), 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(bank), 'questions', dict(Counter(q['type'] for q in bank)))
