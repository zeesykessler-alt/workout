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

## Verified against the shelf

The binders are labelled and in place. Every entry name and file number in
Section One was checked against the spine labels photographed on the shelf:
**30 of 30 files match**. That also settled the six places Carol's two sheets
disagreed — all six in favour of her per-file listing (see `RESOLVED`).

One item is still open (`OUTSTANDING`): **Marriage**, File 5 — on Carol's sheet
but not named on the spine label. It is kept in the catalogue.

Also confirmed: **Shechita is File 29**. An earlier detail export had it at 26;
that was wrong.

Carol supplied three sheets in all — a per-file listing (structure), an A–Z index
(cross-check), and a detail export (the descriptive bullets, matched on name; see
`ALIASES` in `build.py` where the wording differs).
