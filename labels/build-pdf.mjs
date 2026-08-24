// Build the print-ready PDF.
//
// The sheet is authored LANDSCAPE with upright labels: rotating a label's
// artwork in CSS looks right on screen but is mis-placed by Chromium's print
// pagination, which silently corrupts every label in the output. So we render
// landscape, then rotate the finished PDF pages to portrait, giving an A4
// portrait file that prints with default settings.
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';

const HTML = new URL('./klbd-archive-labels.html', import.meta.url).pathname;
const OUT  = new URL('./klbd-archive-labels.pdf', import.meta.url).pathname;
const TMP  = OUT.replace(/\.pdf$/, '.landscape.pdf');

const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
});
const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
await page.goto('file://' + HTML);
await page.waitForTimeout(2500);

const overflow = await page.evaluate(() =>
  [...document.querySelectorAll('.items')].filter(u => u.scrollHeight - u.clientHeight > 1).length);
if (overflow) throw new Error(`${overflow} label(s) overflow their 200mm height`);

await page.pdf({ path: TMP, format: 'A4', landscape: true, printBackground: true });
await browser.close();

execFileSync('python3', ['-c', `
import pymupdf, os, sys
d = pymupdf.open("${TMP}")
for p in d: p.set_rotation(90)
d.save("${OUT}")
os.remove("${TMP}")
r = pymupdf.open("${OUT}")[0].rect
mm = lambda v: round(v / 72 * 25.4, 1)
assert (mm(r.width), mm(r.height)) == (210.2, 297.3), (mm(r.width), mm(r.height))
print("built", d.page_count, "portrait A4 pages")
`], { stdio: 'inherit' });
