"""Shared helpers: Galatians verse counts, reference parsing, the three parts of the letter."""
import re

# Verses per chapter (ESV numbering). Total 149.
VERSES = [24, 21, 29, 31, 26, 18]

SECTIONS = [  # (first chapter, last chapter, label)
    (1, 2, 'Personal defense (1-2)'),
    (3, 4, 'Doctrinal argument (3-4)'),
    (5, 6, 'Practical living (5-6)'),
]

def section(ch):
    return next(label for a, b, label in SECTIONS if a <= ch <= b)

def verses(ref):
    """'2:11-14' / '5:1' / '4:28-5:1' -> list of (chapter, verse). Raises on invalid refs."""
    m = re.fullmatch(r'(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?', ref.strip())
    if not m: raise ValueError(f'bad ref {ref!r}')
    c1, v1 = int(m[1]), int(m[2])
    c2 = int(m[3]) if m[3] else c1
    v2 = int(m[4]) if m[4] else v1
    if (c2, v2) < (c1, v1): raise ValueError(f'backwards ref {ref!r}')
    out, c, v = [], c1, v1
    while (c, v) <= (c2, v2):
        if not (1 <= c <= len(VERSES) and 1 <= v <= VERSES[c - 1]): raise ValueError(f'ref out of range {ref!r}')
        out.append((c, v))
        c, v = (c, v + 1) if v < VERSES[c - 1] else (c + 1, 1)
    return out
