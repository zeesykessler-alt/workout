# KLBD Archive spine labels

Print-ready spine labels for the 30 KLBD Archive lever-arch files, laid out for
**Avery L7171** sheets (A4, 200 × 60 mm, 4 labels per sheet) — 8 sheets in total.

- `klbd-archive-labels.html` — the editable template. Open in a browser and print.
- `klbd-archive-labels.pdf` — the same thing rendered, if you just want to print.

## Printing

Print at **100% / Actual size** — no "fit to page", no headers and footers,
A4 portrait, single-sided. Do a test run on plain paper and hold it over a label
sheet before committing a sheet of labels.

## Adjusting

- **Wording:** edit the `FILES` array near the bottom of the HTML file. Each entry
  is `{"n": <file number>, "items": [ ... ]}`. Type sizes shrink automatically so
  the contents always fit the 60 mm label.
- **Alignment:** if your printer is a millimetre off, change `--offset-x` /
  `--offset-y` in the CSS at the top of the file.
- **Colour:** `--navy` sets the number block and rules; it is matched to the
  existing blue binders.

Label geometry assumed: 5 mm side margins, 28.5 mm top/bottom margins, no gaps
between labels.
