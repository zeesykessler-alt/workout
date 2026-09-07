# KLBD Archive catalogue

An A4 catalogue of the archive, built from Carol's spreadsheet export.

- `klbd-archive-catalogue.pdf` — the deliverable, 18 pages, A4 portrait.
- `catalogue.html` — the rendered document.
- `source.tsv` — Carol's spreadsheet, tab-separated (File Name / Description / File No.).
- `build.py` — regenerates `catalogue.html` from `source.tsv`.

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

## Note on file numbers

The spreadsheet's "Page No." column is the file (binder) number, 1–30. One
conflict with the original archive index used for the spine labels: **Shechita**
is filed at 26 here and at 29 there. The catalogue follows the spreadsheet.
