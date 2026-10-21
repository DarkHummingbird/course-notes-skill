---
name: course-notes
description: Build standalone Chinese course notes from lecture recordings/transcripts and slide decks. Use when the user provides recordings, transcripts, or courseware (录音转文字、课件、课堂录音) and asks for organized notes (整理笔记). Extracts concepts, methods, examples, and interview Q&A; captures slide figures; enforces a no-lecture-narration style so the note reads like a handbook, not a transcript.
argument-hint: "[course or topic]"
license: MIT
metadata:
  author: ddl
  version: "1.0.0"
---

# Course Notes

Turn raw lecture material into a note that reads like a handbook, not a transcript.

## When to Use

- User provides one or more lecture recordings/transcripts (Feishu Minutes, audio transcript, plain text) and courseware (HTML slides, PDF, PPTX, screenshots).
- User asks to 整理笔记 / 做成笔记 / 形成一篇笔记.
- User has a preferred note sample; follow its structure and voice.
- User asks to turn the workflow itself into a reusable skill (as opposed to producing one note).

Do not use for: meeting minutes, verbatim transcription, or a summary of every sentence.

## What Good Looks Like

The note is a **standalone system**, not a lesson log:

- It can be read without the recording or the slides.
- It groups by concept and method, not by chronology.
- It states rules directly; it never says "老师开场说", "课堂上", "课件里", "上一讲".
- Examples sit under the knowledge point they prove; they are not a separate "案例" section.
- It keeps the concrete details that make a case credible: numbers, quotes, roles, sequence, trade-offs.
- It ends with what the reader can do: outputs, checks, pitfalls, interview answers, exercises.

Before:

> 上一讲做的事，是把一款完整产品拆成五层。老师开场先给了一个判断……

After:

> 做一款 AI 产品，第一步不是想功能，而是判断做什么、为谁做、值不值得做。
>
> **核心判断**：当 PRD、代码、产品文档都能由 AI 生成，产品经理的价值集中在判断、取舍和为结果负责。

## Inputs and Source Inventory

Build this table before extracting anything:

| Source | What to extract | Verify |
|---|---|---|
| Recording A / transcript | full text, timestamps, speakers if available | paragraph count, start/end time, no truncation |
| Recording B / transcript | same; mark overlap or continuation | coverage of the scope the user named |
| Courseware | slide count, section titles, diagrams, tables, code blocks | every slide number mapped to a section |
| Existing note / style sample | heading conventions, tone, example format, banned phrases | diff against the style contract |
| User constraints | scope, output format, image handling, depth | restate in one line before drafting |

If the user names a scope ("今天讲到上篇收尾"), do not silently include later parts. Put later parts in a short "next stage" section only if useful.

## Workflow

### 1. Lock the scope

Write one sentence: **"This note covers X; Y is out of scope."** If the recordings and courseware disagree, follow the user's scope, then flag the gap.

### 2. Extract the transcript

- Prefer the user's text file or a full transcript export.
- If the source is a Feishu Minutes page, open it in the browser, use the 文字记录 tab, and extract the complete transcript; if the DOM is virtualized, use the page's transcript API with the existing login. Never bypass authentication.
- Save raw text with timestamps in a working file. Do not paste raw transcript into the final note.
- Read for: definitions, rules, steps, examples, numbers, trade-offs, interview questions, homework.
- Mark off-topic material: greetings, device checks, breaks, attendance, repetition, filler.

### 3. Extract the courseware

- For HTML slide decks, read the slide structure from the DOM; extract all slide text to a working file.
- Identify slides that carry a model, flow, matrix, table, or before/after comparison. These become figures.
- Capture figures at 1920×1080 or the deck's native size. Crop sidebars, page numbers, and corner chrome.
- Save as `assets/{slug}/NN-slug.png`; keep a mapping from slide number to image path.
- For PDF/PPTX, render pages at high DPI and crop margins. For image-only decks, use vision/OCR.
- Do not include decorative title slides, agenda pages, or screenshots that add no information.

### 4. Build the content model

Extract into these buckets before writing:

| Bucket | What goes in |
|---|---|
| Definitions | term → one-sentence definition |
| Judgement rules | if/then, three conditions, red flags, thresholds |
| Methods | numbered steps, inputs, outputs |
| Decision points | trade-offs, what to cut, what to defer |
| Examples | positive and negative cases with concrete details |
| Outputs | cards, tables, reports, PRDs, checklists |
| Interview Q&A | question, framework, reference answer, variant |
| Pitfalls | common mistakes and their fixes |
| Data / caveats | numbers that need a source or a confidence note |

Then build the spine:

- One H1 per stage or big question.
- One H2 per method or decision.
- Each H2 should answer: what is it → how to do it → example → output/check.
- If a bucket has no source material, leave it out. Do not invent.

### 5. Weave examples under points

This is the most important structural rule.

- Put each example immediately after the point it proves, as a blockquote: `> **例｜...**` or `> **反例｜...**`.
- Do not create an H1/H2 called "案例" or "课堂案例".
- If one case illustrates several methods (e.g., a single project used for problem definition, user research, and demand pool), split it into fragments and place each fragment under the relevant method.
- Keep the case's concrete details: who, when, what they said, the numbers, what was tried, why it failed.
- End each example with one sentence: what it proves, or what the reader should do differently.
- Examples should support the method, not replace it. If the note reads as a chain of stories, the spine is missing.

### 6. Write in the note voice

Follow `references/style-contract.md` exactly. The short version:

- H1: `# 一、...`, `# 二、...` — each major section is a top-level heading. An optional document title may sit above them as a single `#` line.
- One-line definition, one-line mainline.
- H2: `## 1.1 ...`, `## 1.2 ...`.
- H3: `### ...` for sub-substeps inside a method.
- Direct assertions, imperative guidance, no lecturer voice.
- Tables for steps, fields, comparisons, and decision matrices.
- Figures from the courseware at the point they explain.
- Interview questions: `## Q1 ...` with `**框架**`, `**参考话术**`, `**补充**`, `**换成你的**`.
- One short data note at the end; no per-paragraph "课堂口径".

### 7. QA and deliver

Run `python3 scripts/check_note.py <note.md>` and fix every error. Then:

- Verify every image path exists and every figure is referenced.
- Read the opening and three random sections aloud; if any sentence sounds like a lecture, rewrite it.
- Deliver the note plus the assets folder. State the scope and any data caveats in one short paragraph.

## Output Contract

- Note: `{主题}-{阶段}-笔记.md` (or the user's requested name).
- Assets: `assets/{slug}/NN-slug.png`.
- Figures: 1600–2000 px wide, cropped, legible at 100%.
- No raw transcript, no timestamps, no attendance/break/device content.
- No "老师/课堂/课件/上一讲/这一讲/同学们/课堂口径" in the body.
- If the courseware includes interview questions with answers, preserve the framework and reference answer, then add course examples and a "换成你的" prompt.

## References

- `references/style-contract.md` — banned phrases, rewrite table, heading rules, example format.
- `assets/note-template.md` — starting skeleton.
- `scripts/check_note.py` — deterministic style and link checks.
