# KLBD Archive spine labels

Print-ready spine labels for the 30 KLBD Archive lever-arch files, laid out for
**Avery L7171** sheets (A4, 200 × 60 mm, 4 labels per sheet) — 8 sheets in total.

Each label's artwork is portrait (60 mm wide × 200 mm tall) and rotated 90° into
the landscape die-cut, so it reads the right way up once applied down the spine
of a binder standing on a shelf. The sheet itself still prints portrait.

- `klbd-archive-labels.html` — the editable template. Open in a browser and print.
- `klbd-archive-labels.pdf` — the same thing rendered, if you just want to print.

## Printing (Chrome/Edge on Windows → Lexmark XC9255)

In the browser print dialog, under **More settings**:

- Tick **Background graphics** — without it the navy blocks print blank.
- **Scale: Custom → 100** (Chrome's "Default" shrinks to fit the printable area).
- **Layout: Landscape.** The label sheet is fed portrait as usual; printing
  landscape is what lays each 200 mm die-cut along the sheet with the artwork
  upright on the spine.
- **Margins: None**, **Paper size: A4**, **Headers and footers** off, two-sided off.
- Leave **Layout** on **Portrait** — the sheet is portrait even though each label sits sideways on it.

At the printer:

- Load label sheets in the **multipurpose / bypass tray**, not a cassette —
  cassettes bend the sheet tightly enough to peel labels off inside the machine.
- Set that tray's **paper type to Labels** and **size to A4** on the touchscreen,
  so the feed slows and the fuser adjusts.
- The XC9255 is A3-capable, so confirm it hasn't auto-selected an A3 tray.

Do a test run on plain paper and hold it over a label sheet before committing
label stock, and feed label sheets one at a time.

## Adjusting

- **Wording:** edit the `FILES` array near the bottom of the HTML file. Each entry
  is `{"n": <file number>, "items": [ ... ]}`. Type sizes shrink automatically so
  the contents always fit the 60 mm label.
- **Alignment:** if your printer is a millimetre off, change `--offset-x` /
  `--offset-y` in the CSS at the top of the file.
- **Colour:** `--navy` sets the number block and rules; it is matched to the
  existing blue binders.

## Layout note

Each label's artwork is authored upright (60 mm wide × 200 mm tall) on a
landscape 297 × 210 mm sheet, four across. Nothing is rotated in CSS: a rotated,
absolutely-positioned box is mis-placed by Chromium's print pagination, which
corrupts every label in the generated PDF while still looking correct on screen.
Verify changes against the rendered PDF, not the browser view.

Label geometry, measured on the sheet as printed: labels 28.5 mm in from each
short edge and 5 mm from each long edge, four 60 mm labels with no gaps between
them.
