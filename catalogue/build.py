#!/usr/bin/env python3
"""Generate the KLBD Archive catalogue from Carol's spreadsheet export."""
import csv, re, html, collections, datetime

ROWS = list(csv.reader(open('source.tsv'), delimiter='\t'))[1:]

records = []
for r in ROWS:
    if not any(c.strip() for c in r):
        continue
    name, desc, num = (r + ['', '', ''])[:3]
    name, desc, num = name.strip(), desc.strip(), num.strip()
    if not num.isdigit():
        continue
    items = [re.sub(r'^\*\s*', '', l).strip() for l in desc.split('\n')]
    records.append({'name': name, 'file': int(num), 'items': [i for i in items if i]})

# ---- index terms -------------------------------------------------------
# Every entry name is indexed. A detail line is indexed too when it reads as a
# name rather than a sentence — that is what makes "Bonito" or "Marmite"
# findable without dumping whole paragraphs into the index.
STOPWORDS = {'report', 'reports', 'various letters', 'background', 'problems'}

def is_name_like(s):
    if len(s) > 34 or len(s.split()) > 4:
        return False
    if s.lower() in STOPWORDS:
        return False
    if s.count('(') != s.count(')'):      # a fragment left by splitting
        return False
    if re.search(r'\b(re|the|and|of|for|with|from|by|to)\b', s, re.I) and len(s.split()) > 2:
        return False
    return bool(re.match(r"^[A-Z0-9][\w&'’\-. ()]*$", s)) and not s.endswith(':')

def sort_key(s):
    s = re.sub(r'^(the|a|an)\s+', '', s.strip(), flags=re.I)
    return (re.sub(r'[^a-z0-9 ]', '', s.lower()), s.lower())

terms = collections.defaultdict(set)
for rec in records:
    terms[rec['name']].add(rec['file'])
    for it in rec['items']:
        head = it.split(' - ')[0].split(':')[0].strip(' *')
        if is_name_like(head) and head.lower() != rec['name'].lower():
            terms[head].add(rec['file'])

index = sorted(terms.items(), key=lambda kv: sort_key(kv[0]))
letters = collections.OrderedDict()
for term, files in index:
    L = sort_key(term)[0][:1].upper() or '#'
    letters.setdefault(L, []).append((term, sorted(files)))

by_file = collections.OrderedDict()
for n in range(1, 31):
    by_file[n] = [r for r in records if r['file'] == n]

E = lambda s: html.escape(s, quote=False)

# ---- markup ------------------------------------------------------------
files_html = []
for n, recs in by_file.items():
    entries = []
    for rec in recs:
        detail = ''
        if rec['items']:
            detail = '<ul class="detail">' + ''.join(
                f'<li>{E(i)}</li>' for i in rec['items']) + '</ul>'
        entries.append(f'<div class="entry"><h3>{E(rec["name"])}</h3>{detail}</div>')
    files_html.append(
        f'<article class="file" id="file-{n}">'
        f'<header class="file-head"><span class="chip">{n}</span>'
        f'<h2>File {n}</h2><span class="count">{len(recs)} '
        f'{"entry" if len(recs)==1 else "entries"}</span></header>'
        + ''.join(entries) + '</article>')

index_html = []
for L, rows in letters.items():
    items = ''.join(
        f'<li><span class="term">{E(t)}</span>'
        f'<span class="dots"></span>'
        f'<span class="ref">{", ".join(str(f) for f in fs)}</span></li>'
        for t, fs in rows)
    index_html.append(f'<div class="letter"><h3>{L}</h3><ul>{items}</ul></div>')

TOTAL_TERMS = len(index)
TOTAL_ENTRIES = len(records)
TODAY = datetime.date.today().strftime('%B %Y')

doc = f'''<title>KLBD Archive Catalogue</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
  :root{{
    --navy:#1c2b6b;
    --navy-deep:#141f4e;
    --ink:#10162f;
    --hair:#c9cee2;
    --rule:#dfe3ef;
    --mute:#5c6484;
    --paper:#ffffff;
    --ground:#eef0f6;
    --shadow:0 1px 3px rgba(20,31,78,.13), 0 12px 34px rgba(20,31,78,.10);
  }}
  @media (prefers-color-scheme: dark){{
    :root:not([data-theme="light"]){{ --ground:#12141c; }}
  }}
  :root[data-theme="dark"]{{ --ground:#12141c; }}

  @page{{ size:A4 portrait; margin:18mm 16mm 16mm; }}
  *{{ box-sizing:border-box; margin:0; padding:0; }}
  body{{
    background:var(--ground);
    color:var(--ink);
    font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
    -webkit-print-color-adjust:exact; print-color-adjust:exact;
  }}
  .page{{
    width:210mm; min-height:297mm;
    padding:18mm 16mm 16mm;
    margin:0 auto 10mm;
    background:var(--paper);
    box-shadow:var(--shadow);
  }}
  @media print{{
    body{{ background:var(--paper); }}
    .page{{ width:auto; min-height:0; padding:0; margin:0; box-shadow:none; }}
    .cover{{ page-break-after:always; }}
    .index-open{{ page-break-before:always; }}
  }}

  /* ---------- cover ---------- */
  .cover{{ text-align:center; padding-top:52mm; }}
  .crest{{
    display:inline-block; background:var(--navy); color:#fff;
    padding:9mm 14mm 10mm; margin-bottom:14mm;
  }}
  .crest .mark{{
    font-family:Archivo,Arial,sans-serif; font-weight:700;
    font-size:15pt; letter-spacing:.2em; line-height:1.25;
  }}
  .crest .div{{ width:22mm; height:.4mm; background:rgba(255,255,255,.5); margin:4mm auto 3.5mm; }}
  .crest .sub{{
    font-family:Archivo,Arial,sans-serif; font-weight:500;
    font-size:7.5pt; letter-spacing:.26em; text-transform:uppercase; opacity:.85;
  }}
  .cover h1{{
    font-family:Archivo,Arial,sans-serif; font-weight:700;
    font-size:34pt; letter-spacing:-.02em; color:var(--navy-deep);
    text-wrap:balance; line-height:1.05;
  }}
  .cover .lede{{
    font-size:13pt; line-height:1.6; color:var(--mute);
    max-width:110mm; margin:7mm auto 0;
  }}
  .cover .facts{{
    display:flex; justify-content:center; gap:14mm; margin-top:16mm;
    font-family:Archivo,Arial,sans-serif;
  }}
  .cover .facts div{{ text-align:center; }}
  .cover .facts b{{
    display:block; font-size:22pt; font-weight:700; color:var(--navy);
    font-variant-numeric:tabular-nums; line-height:1;
  }}
  .cover .facts span{{
    font-size:7pt; letter-spacing:.2em; text-transform:uppercase; color:var(--mute);
  }}
  .cover .foot{{
    margin-top:24mm; font-family:Archivo,Arial,sans-serif;
    font-size:8pt; letter-spacing:.16em; text-transform:uppercase; color:var(--mute);
  }}

  /* ---------- section openers ---------- */
  .section-open{{
    border-top:1.2mm solid var(--navy);
    padding-top:4mm; margin-bottom:9mm;
  }}
  .section-open .eyebrow{{
    font-family:Archivo,Arial,sans-serif; font-size:7.5pt; font-weight:600;
    letter-spacing:.24em; text-transform:uppercase; color:var(--mute);
  }}
  .section-open h2{{
    font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:19pt;
    color:var(--navy-deep); margin-top:1.5mm; letter-spacing:-.01em;
  }}
  .section-open p{{ margin-top:2.5mm; color:var(--mute); font-size:10.5pt; max-width:150mm; }}

  /* ---------- files ---------- */
  .file{{ margin-bottom:7mm; }}
  .file-head{{
    display:flex; align-items:center; gap:4mm;
    border-bottom:.4mm solid var(--navy); padding-bottom:1.8mm; margin-bottom:3mm;
    break-after:avoid; break-inside:avoid;
  }}
  .chip{{
    flex:0 0 auto; min-width:11mm; padding:1.4mm 2mm;
    background:var(--navy); color:#fff; text-align:center;
    font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:13pt;
    font-variant-numeric:tabular-nums; line-height:1.1;
  }}
  .file-head h2{{
    font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:12.5pt;
    letter-spacing:.1em; text-transform:uppercase; color:var(--navy-deep);
  }}
  .file-head .count{{
    margin-left:auto; font-family:Archivo,Arial,sans-serif;
    font-size:7.5pt; letter-spacing:.14em; text-transform:uppercase; color:var(--mute);
  }}
  .entry{{ margin-bottom:3.2mm; break-inside:avoid; }}
  .entry h3{{
    font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:10pt;
    color:var(--ink); line-height:1.3;
  }}
  .detail{{ margin:1mm 0 0 4mm; }}
  .detail li{{
    list-style:none; position:relative; padding-left:3.6mm;
    font-size:9.5pt; line-height:1.42; color:#39405e; margin-bottom:.7mm;
  }}
  .detail li::before{{
    content:""; position:absolute; left:0; top:.55em;
    width:1.1mm; height:1.1mm; border-radius:50%; background:var(--hair);
  }}

  /* ---------- index ---------- */
  .index{{ columns:3; column-gap:7mm; column-rule:.2mm solid var(--rule); }}
  .letter{{ break-inside:avoid-column; margin-bottom:3.5mm; }}
  .letter h3{{
    font-family:Archivo,Arial,sans-serif; font-weight:700; font-size:11pt;
    color:var(--navy); border-bottom:.3mm solid var(--hair);
    padding-bottom:.8mm; margin-bottom:1.5mm;
  }}
  .letter li{{
    list-style:none; display:flex; align-items:baseline; gap:1mm;
    font-size:8.5pt; line-height:1.35; margin-bottom:.9mm;
  }}
  .letter .term{{ color:var(--ink); }}
  .letter .dots{{
    flex:1 1 auto; min-width:2mm; align-self:flex-end;
    border-bottom:.2mm dotted var(--hair); transform:translateY(-.7mm);
  }}
  .letter .ref{{
    font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:8pt;
    color:var(--navy); font-variant-numeric:tabular-nums; white-space:nowrap;
  }}
</style>

<div class="page cover">
  <div class="crest">
    <div class="mark">KLBD<br>ARCHIVE</div>
    <div class="div"></div>
    <div class="sub">London Beth Din &middot; Kashrus Division</div>
  </div>
  <h1>Catalogue of the Archive</h1>
  <p class="lede">What is held in each of the thirty files, and an A&ndash;Z index
  of every subject with the file it is filed in.</p>
  <div class="facts">
    <div><b>30</b><span>Files</span></div>
    <div><b>{TOTAL_ENTRIES}</b><span>Entries</span></div>
    <div><b>{TOTAL_TERMS}</b><span>Index terms</span></div>
  </div>
  <div class="foot">{TODAY}</div>
</div>

<div class="page">
  <div class="section-open">
    <div class="eyebrow">Section One</div>
    <h2>The Files</h2>
    <p>Files 1 to 30 in order. The number in navy is the number on the binder&rsquo;s
    spine label, so a file can be matched to the shelf at a glance.</p>
  </div>
  {''.join(files_html)}
</div>

<div class="page index-open">
  <div class="section-open">
    <div class="eyebrow">Section Two</div>
    <h2>Index A&ndash;Z</h2>
    <p>Every subject in the archive, alphabetically, with the file number to pull.
    A subject held in more than one file lists each of them.</p>
  </div>
  <div class="index">{''.join(index_html)}</div>
</div>
'''

open('catalogue.html', 'w').write(doc)
print(f'{TOTAL_ENTRIES} entries, {TOTAL_TERMS} index terms across 30 files')
