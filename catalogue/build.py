#!/usr/bin/env python3
"""Build the KLBD Archive catalogue.

Structure comes from files.py (Carol's per-file listing — authoritative).
Detail comes from source.tsv (Carol's earlier description export), matched on
name with the aliases below for the cases where the two sheets word things
differently.
"""
import csv, re, html, collections, datetime, difflib
import files as F

ALIASES = {
    'beachcroft 1990': (1, 'Beachcroft (1967)'),
    'beis din guideline of kashrus of various foods ingredients':
        (1, 'Beis Din Guidelines of Kashrus & Food Ingredients'),
    'bestfoods uniliver': (1, 'BestFoods / Unilever'),
    'biotechnology kashrus': (1, 'Biotechnology and Kashrus'),
    'chief rabbinate of israel': (2, 'Chief Rabbinate'),
    'certification process project': (4, 'Factory Visits Review (Certification Process Project)'),
    'factory reviews': (4, 'Factory Visits Review (Certification Process Project)'),
    'rabbi shindler marriage': (5, 'Marriage'),
    'newspaper articles copies of articles': (6, 'Newspaper Articles'),
    'medicine kashrus': (7, 'Medicines'),
    'kashrus guide': (14, 'Policy Decisions with Regard to the Kashrus Guide'),
    'gelatine project': (4, 'Gelatine'),
    'court cases': (13, 'Court Cases (JFS, Rosie Ben Shushan)'),
    'rabbi conway presentation synopsis products ingredients':
        (13, 'Rabbi Conway: Presentation, Synopsis and Brief Biography'),
    'overview of kashrus division current proposed procedures':
        (7, 'Overview of Kashrus Division Procedure'),
}
for L in 'bcefghjk':
    ALIASES[f'list info of fish {L}'] = (21, 'List & Info of Fish B–K')
for L in 'lmoprs':
    ALIASES[f'list info of fish {L}'] = (22, 'List & Info of Fish L–S')

def norm(s):
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split())

# ---- detail ------------------------------------------------------------
raw = {}
for r in list(csv.reader(open('source.tsv'), delimiter='\t'))[1:]:
    if not any(c.strip() for c in r):
        continue
    name, d = (r + ['', ''])[:2]
    items = [re.sub(r'^\*\s*', '', l).strip() for l in d.split('\n')]
    items = [i for i in items if i]
    if items:
        raw.setdefault(norm(name), items)

detail = collections.defaultdict(list)
lookup = {norm(e): (n, e) for n, es in F.FILES.items() for e in es}
for key, items in raw.items():
    target = ALIASES.get(key) or lookup.get(key)
    if not target:
        close = difflib.get_close_matches(key, list(lookup), n=1, cutoff=0.72)
        target = lookup[close[0]] if close else None
    if target:
        for i in items:
            if i not in detail[target]:
                detail[target].append(i)

# ---- index -------------------------------------------------------------
STOPWORDS = {'report', 'reports', 'various letters', 'background', 'problems'}

def is_name_like(s):
    if len(s) > 34 or len(s.split()) > 4 or s.lower() in STOPWORDS:
        return False
    # dates and year ranges are not subjects
    if re.match(r'^\d{4}\s*[-–]\s*\d{2,4}$', s) or re.match(r'^\d', s):
        return False
    if not re.search(r'[A-Za-z]{3}', s):
        return False
    if s.count('(') != s.count(')'):
        return False
    if re.search(r'\b(re|the|and|of|for|with|from|by|to)\b', s, re.I) and len(s.split()) > 2:
        return False
    return bool(re.match(r"^[A-Z0-9][\w&'’\-. ()]*$", s)) and not s.endswith(':')

def sort_key(s):
    s = re.sub(r'^(the|a|an)\s+', '', s.strip(), flags=re.I)
    return (re.sub(r'[^a-z0-9 ]', '', s.lower()), s.lower())

terms = collections.defaultdict(set)
for n, entries in F.FILES.items():
    for e in entries:
        terms[e].add(n)
        for sub in F.SUBLISTS.get(e, []):
            terms[sub].add(n)
        for it in detail.get((n, e), []):
            head = it.split(' - ')[0].split(':')[0].strip(' *')
            if is_name_like(head) and norm(head) != norm(e):
                terms[head].add(n)

index = sorted(terms.items(), key=lambda kv: sort_key(kv[0]))
letters = collections.OrderedDict()
for term, fs in index:
    L = (sort_key(term)[0][:1] or '#').upper()
    letters.setdefault(L, []).append((term, sorted(fs)))

E = lambda s: html.escape(s, quote=False)
TOTAL_ENTRIES = sum(len(v) for v in F.FILES.values())
TOTAL_TERMS = len(index)
TODAY = datetime.date.today().strftime('%B %Y')

# ---- markup ------------------------------------------------------------
files_html = []
for n, entries in F.FILES.items():
    blocks = []
    for e in entries:
        bits = ''
        subs = F.SUBLISTS.get(e, [])
        if subs:
            bits += '<p class="subs">' + E(' · '.join(subs)) + '</p>'
        items = detail.get((n, e), [])
        if items:
            bits += '<ul class="detail">' + ''.join(f'<li>{E(i)}</li>' for i in items) + '</ul>'
        blocks.append(f'<div class="entry"><h3>{E(e)}</h3>{bits}</div>')
    files_html.append(
        f'<article class="file"><header class="file-head"><span class="chip">{n}</span>'
        f'<h2>File {n}</h2><span class="count">{len(entries)} '
        f'{"entry" if len(entries) == 1 else "entries"}</span></header>'
        + ''.join(blocks) + '</article>')

index_html = ''.join(
    f'<div class="letter"><h3>{L}</h3><ul>' + ''.join(
        f'<li><span class="term">{E(t)}</span><span class="dots"></span>'
        f'<span class="ref">{", ".join(map(str, fs))}</span></li>' for t, fs in rows)
    + '</ul></div>' for L, rows in letters.items())

resolved_html = ''.join(
    f'<li><b>{E(a)}</b> — {E(b)}</li>' for a, b in F.RESOLVED)
outstanding_html = ''.join(
    f'<li><b>{E(a)}</b> ({E(b)}) — {E(c)}</li>' for a, b, c in F.OUTSTANDING)
typos_html = ', '.join(f'{E(a)} &rarr; {E(b)}' for a, b in F.TYPO_FIXES)

doc = f'''<title>KLBD Archive Catalogue</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
  :root{{
    --navy:#1c2b6b; --navy-deep:#141f4e; --ink:#10162f;
    --hair:#c9cee2; --rule:#dfe3ef; --mute:#5c6484;
    --paper:#ffffff; --ground:#eef0f6;
    --shadow:0 1px 3px rgba(20,31,78,.13), 0 12px 34px rgba(20,31,78,.10);
  }}
  @media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{ --ground:#12141c; }} }}
  :root[data-theme="dark"]{{ --ground:#12141c; }}

  @page{{ size:A4 portrait; margin:18mm 16mm 16mm; }}
  *{{ box-sizing:border-box; margin:0; padding:0; }}
  body{{
    background:var(--ground); color:var(--ink);
    font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
    -webkit-print-color-adjust:exact; print-color-adjust:exact;
  }}
  .page{{
    width:210mm; min-height:297mm; padding:18mm 16mm 16mm;
    margin:0 auto 10mm; background:var(--paper); box-shadow:var(--shadow);
  }}
  @media print{{
    body{{ background:var(--paper); }}
    .page{{ width:auto; min-height:0; padding:0; margin:0; box-shadow:none; }}
    .page + .page{{ break-before:page; }}   /* one break per section, never two */
  }}

  .cover{{ text-align:center; padding-top:48mm; }}
  .crest{{ display:inline-block; background:var(--navy); color:#fff; padding:9mm 14mm 10mm; margin-bottom:13mm; }}
  .crest .mark{{ font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:15pt; letter-spacing:.2em; line-height:1.25; }}
  .crest .div{{ width:22mm; height:.4mm; background:rgba(255,255,255,.5); margin:4mm auto 3.5mm; }}
  .crest .sub{{ font-family:Archivo,Arial,sans-serif; font-weight:500; font-size:7.5pt; letter-spacing:.26em; text-transform:uppercase; opacity:.85; }}
  .cover h1{{ font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:33pt; letter-spacing:-.02em; color:var(--navy-deep); text-wrap:balance; line-height:1.05; }}
  .cover .lede{{ font-size:12.5pt; line-height:1.6; color:var(--mute); max-width:112mm; margin:7mm auto 0; }}
  .cover .facts{{ display:flex; justify-content:center; gap:14mm; margin-top:15mm; font-family:Archivo,Arial,sans-serif; }}
  .cover .facts b{{ display:block; font-size:22pt; font-weight:700; color:var(--navy); font-variant-numeric:tabular-nums; line-height:1; }}
  .cover .facts span{{ font-size:7pt; letter-spacing:.2em; text-transform:uppercase; color:var(--mute); }}
  .cover .foot{{ margin-top:22mm; font-family:Archivo,Arial,sans-serif; font-size:8pt; letter-spacing:.16em; text-transform:uppercase; color:var(--mute); }}

  .section-open{{ border-top:1.2mm solid var(--navy); padding-top:4mm; margin-bottom:9mm; }}
  .section-open .eyebrow{{ font-family:Archivo,Arial,sans-serif; font-size:7.5pt; font-weight:600; letter-spacing:.24em; text-transform:uppercase; color:var(--mute); }}
  .section-open h2{{ font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:19pt; color:var(--navy-deep); margin-top:1.5mm; letter-spacing:-.01em; }}
  .section-open p{{ margin-top:2.5mm; color:var(--mute); font-size:10.5pt; max-width:150mm; }}

  .file{{ margin-bottom:7mm; }}
  .file-head{{ display:flex; align-items:center; gap:4mm; border-bottom:.4mm solid var(--navy); padding-bottom:1.8mm; margin-bottom:3mm; break-after:avoid; break-inside:avoid; }}
  .chip{{ flex:0 0 auto; min-width:11mm; padding:1.4mm 2mm; background:var(--navy); color:#fff; text-align:center; font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:13pt; font-variant-numeric:tabular-nums; line-height:1.1; }}
  .file-head h2{{ font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:12.5pt; letter-spacing:.1em; text-transform:uppercase; color:var(--navy-deep); }}
  .file-head .count{{ margin-left:auto; font-family:Archivo,Arial,sans-serif; font-size:7.5pt; letter-spacing:.14em; text-transform:uppercase; color:var(--mute); }}
  .entry{{ margin-bottom:3.2mm; break-inside:avoid; }}
  .entry h3{{ font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:10pt; color:var(--ink); line-height:1.3; }}
  .subs{{ margin:.8mm 0 0 4mm; font-size:9pt; line-height:1.45; color:var(--mute); }}
  .detail{{ margin:1mm 0 0 4mm; }}
  .detail li{{ list-style:none; position:relative; padding-left:3.6mm; font-size:9.5pt; line-height:1.42; color:#39405e; margin-bottom:.7mm; }}
  .detail li::before{{ content:""; position:absolute; left:0; top:.55em; width:1.1mm; height:1.1mm; border-radius:50%; background:var(--hair); }}

  .index{{ columns:3; column-gap:7mm; column-rule:.2mm solid var(--rule); }}
  .letter{{ break-inside:avoid-column; margin-bottom:3.5mm; }}
  .letter h3{{ font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:11pt; color:var(--navy); border-bottom:.3mm solid var(--hair); padding-bottom:.8mm; margin-bottom:1.5mm; }}
  .letter li{{ list-style:none; display:flex; align-items:baseline; gap:1mm; font-size:8.5pt; line-height:1.35; margin-bottom:.9mm; }}
  .letter .dots{{ flex:1 1 auto; min-width:2mm; align-self:flex-end; border-bottom:.2mm dotted var(--hair); transform:translateY(-.7mm); }}
  .letter .ref{{ font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:8pt; color:var(--navy); font-variant-numeric:tabular-nums; white-space:nowrap; }}

  .notes h4{{ font-family:Archivo,Arial,sans-serif; font-size:9.5pt; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:var(--navy-deep); margin:6mm 0 2mm; }}
  .notes li{{ list-style:none; font-size:10pt; line-height:1.5; margin-bottom:1.6mm; padding-left:4mm; position:relative; }}
  .notes li::before{{ content:""; position:absolute; left:0; top:.62em; width:1.4mm; height:1.4mm; background:var(--navy); }}
  .notes p{{ font-size:10pt; line-height:1.55; color:var(--mute); max-width:150mm; }}
</style>

<div class="page cover">
  <div class="crest">
    <div class="mark">KLBD<br>ARCHIVE</div>
    <div class="div"></div>
    <div class="sub">London Beth Din &middot; Kashrus Division</div>
  </div>
  <h1>Catalogue of the Archive</h1>
  <p class="lede">What is held in each of the thirty files, and an A&ndash;Z index of
  every subject with the file it is filed in.</p>
  <div class="facts">
    <div><b>30</b><span>Files</span></div>
    <div><b>{TOTAL_ENTRIES}</b><span>Entries</span></div>
    <div><b>{TOTAL_TERMS}</b><span>Index terms</span></div>
  </div>
  <div class="foot">{TODAY}</div>
</div>

<div class="page">
  <div class="section-open files-open">
    <div class="eyebrow">Section One</div>
    <h2>The Files</h2>
    <p>Files 1 to 30 in order. The number in navy is the number on the binder&rsquo;s
    spine label, so a file can be matched to the shelf at a glance.</p>
  </div>
  {''.join(files_html)}
</div>

<div class="page">
  <div class="section-open index-open">
    <div class="eyebrow">Section Two</div>
    <h2>Index A&ndash;Z</h2>
    <p>Every subject alphabetically with the file number to pull. A subject held in
    more than one file lists each of them.</p>
  </div>
  <div class="index">{index_html}</div>
</div>

<div class="page notes">
  <div class="section-open notes-open">
    <div class="eyebrow">Appendix</div>
    <h2>Sources &amp; Corrections</h2>
    <p>How this catalogue was reconciled. Nothing here changes what is in a file
    &mdash; only how it is recorded.</p>
  </div>
  <h4>Checked against the shelf</h4>
  <p>Every entry name and file number in Section One matches the spine label on the
  binder, photographed in place. Where Carol&rsquo;s two sheets disagreed, the shelf
  settles it:</p>
  <ul>{resolved_html}</ul>
  <h4>Still open</h4>
  <ul>{outstanding_html}</ul>
  <h4>Spellings regularised</h4>
  <p>{typos_html}.</p>
</div>
'''

open('catalogue.html', 'w').write(doc)
print(f'{TOTAL_ENTRIES} entries, {TOTAL_TERMS} index terms, '
      f'{sum(1 for k in detail if detail[k])} entries carrying detail')
