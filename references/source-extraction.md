# Source Extraction Recipes

The note is only as good as the raw material. Extract completely, then throw away the transcript.

## 1. Feishu Minutes (录音转文字)

Open the minutes page in a browser that already has the user's login. Do not bypass authentication.

If the transcript tab renders all paragraphs in the DOM, extract `document.body.innerText` after switching to `文字记录`.

If the list is virtualized, use the page's own transcript API:

```
GET /minutes/api/subtitles/paragraph-ids
  ?page_size=10000&page_num=0
  &object_token={object_token}&language=zh_cn

GET /minutes/api/subtitles_v2
  ?paragraph_id={first_pid}&size=200
  &translate_lang=default&is_fluent=false&filter_speaker=true
  &object_token={object_token}&language=zh_cn
```

The first response gives `data.list[].pid` and `start_time` / `stop_time` in milliseconds. The second gives `data.paragraphs[]`; join `sentences[].contents[].content` in order.

Normalize to a working file:

```
[00:02] text...
[00:20] text...
```

Verify:

- paragraph count matches `data.total` (or `size`);
- first and last timestamps match the recording duration;
- no `has_more: true` left unhandled;
- speaker labels, if present, are preserved.

Do not put timestamps or raw transcript into the final note.

## 2. HTML Slide Decks

Most generated decks expose slides as `section[data-slide="N"]` or similar. Inspect the DOM first.

Extract:

- slide count;
- each slide's text (strip nav, sidebar, footer);
- which slides contain a diagram, table, matrix, or before/after comparison.

Capture figures with a 1920×1080 viewport:

```js
await page.setViewportSize({ width: 1920, height: 1080 });
await page.evaluate((i) => window.show(i), slideIndex); // 0-based
await page.waitForTimeout(800);
await page.screenshot({ fullPage: false });
```

If the deck navigates by hash, `#p=N` may be 1-based; verify by reading the page counter (e.g. `10 / 89`).

Crop the sidebar and corner chrome. For a 1920×1080 deck with a 256 px sidebar and a bottom page counter, a useful starting box is:

```
(256, 8, 1890, 944)
```

Adjust per deck; always inspect one cropped image before batch cropping.

Only keep slides that carry a model, flow, matrix, table, or a meaningful before/after. Skip title, agenda, section divider, and decorative pages.

Name files:

```
assets/{slug}/01-seven-stations.png
assets/{slug}/02-problem-card.png
```

Two-digit order + short slug. Keep a mapping from slide number to file name.

## 3. PDF / PPTX

- PPTX: use the `office-pptx` skill or LibreOffice to render slides to images.
- PDF: render pages at 150–200 DPI with `pdftoppm` or PyMuPDF.
- Crop consistent margins; keep text legible at 100%.

## 4. Image-Only Decks

If the deck is screenshots or scanned pages:

- use vision/OCR to read the text;
- capture the figure at native resolution;
- do not upscale a blurry image; re-capture from the source if possible.

## 5. Working Files

Keep these out of the final deliverable:

```
.work/
  transcript-a.txt
  transcript-b.txt
  slides-text.txt
  slide-map.tsv
  notes-model.md
```

The final deliverable is only the note and its `assets/` folder.
