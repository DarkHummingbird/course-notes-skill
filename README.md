# course-notes

A reusable skill for turning **lecture recordings/transcripts + courseware** into a **standalone Chinese study note**.

It encodes the workflow and the style constraints learned from the `需求与立项` note:

- group by concept and method, not by chronology;
- no lecturer voice (`老师 / 课堂 / 课件 / 上一讲 / 这一讲`);
- examples live under the knowledge point they prove;
- Chinese-numeral H1 headings, decimal H2 headings;
- courseware figures captured and cropped locally;
- interview questions kept as framework + reference answer + practice prompt;
- a short data note instead of per-paragraph "课堂口径".

## Files

```
SKILL.md                       # workflow, content model, output contract
references/style-contract.md   # banned phrases, rewrite table, structure rules
references/source-extraction.md# Feishu Minutes, HTML slides, PDF/PPTX recipes
assets/note-template.md        # starting skeleton
scripts/check_note.py          # deterministic style/link checks (stdlib only)
scripts/crop_slides.py         # crop 1920x1080 slide screenshots (needs Pillow)
```

## Install

Copy this directory into the user-level skills directory:

```bash
mkdir -p ~/.agents/skills
cp -R skills/course-notes ~/.agents/skills/
```

Then invoke it by name (`course-notes`) or ask the agent to use it when you provide recordings and courseware.

## Use

Typical prompt:

> 这是今天的录音转文字（链接/文件）和课件（链接/文件），今天讲到 X。帮我整理成一篇笔记。

The skill will:

1. lock the scope;
2. extract the full transcript and slide text;
3. capture key courseware figures;
4. build the content model;
5. weave examples under the relevant points;
6. write in the note voice;
7. run `check_note.py` and deliver.

## Validate a note

```bash
python3 scripts/check_note.py path/to/note.md
```

It checks forbidden lecturer phrases, heading format, image links, table columns, unmatched bold, and the presence of examples/data note.

## Customize

- Edit `references/style-contract.md` to change the voice, heading rules, or banned phrases.
- Edit `assets/note-template.md` to change the default skeleton.
- Add project-specific terms or course conventions to `SKILL.md`.

## Requirements

- Python 3.10+ for the scripts.
- Pillow only for `crop_slides.py`; use the bundled Python if system Python lacks it:
  `/Users/ddl/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3`
