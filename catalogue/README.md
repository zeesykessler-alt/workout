# KLBD Archive catalogue

An A4 catalogue of the archive, built from Carol's spreadsheet export.

- `klbd-archive-catalogue.pdf` — the deliverable, 18 pages, A4 portrait.
- `catalogue.html` — the rendered document.
- `files.py` — **the authoritative structure**: Carol's per-file listing, files 1–30,
  plus the sub-lists she enumerated inside entries, the conflicts between her two
  sheets, and the spellings regularised.
- `source.tsv` — Carol's earlier detail export (File Name / Description / File No.),
  used only for the descriptive bullets.
- `build.py` — regenerates `catalogue.html` from `files.py` + `source.tsv`.

## Two sections

1. **The Files** — files 1 to 30 in order, each with its entries and the detail
   recorded against them. The navy number matches the binder's spine label.
2. **Index A–Z** — every subject alphabetically with the file number to pull.
   Entry names are always indexed; a detail line is indexed too when it reads as
   a name rather than a sentence, so "Bonito" and "Marmite" are findable without
   dumping paragraphs into the index.

## Rebuilding

    python3 build.py        # source.tsv -> catalogue.html
    # then render catalogue.html to PDF at A4 portrait

To correct or add content, edit `source.tsv` and re-run — never edit the HTML by
hand, it is generated.

## Two sources, one structure

Carol supplied two sheets: a per-file listing and an A–Z index. Where they
disagree the catalogue follows the **per-file listing**, and the disagreement is
printed in the Points to Check appendix rather than silently resolved. The
detail export is a third sheet, matched onto the structure by name (see
`ALIASES` in `build.py` for the cases where the wording differs).

Note: **Shechita is File 29**, confirmed by both of Carol's sheets. An earlier
detail export had it at 26; that was wrong.
