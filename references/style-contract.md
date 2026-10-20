# Style Contract

The note is a standalone handbook. It is **not** a lesson log, a transcript, or a summary of what the lecturer did.

## Hard Bans

Never write these in the note body:

- `老师`, `讲师`, `课堂`, `课件`, `上一讲`, `这一讲`, `本讲`, `今天讲`, `下节`
- `同学们`, `大家看`, `我们来看`, `这一页`, `这张图`, `课堂上模拟`, `老师提醒`, `老师反复强调`
- `课堂口径`, `待核实`, `课堂作业`, `老师给大家看`
- `案例` as an H2 heading (examples belong under knowledge points)
- Chronological narration: "首先老师讲了……然后老师讲了……最后……"
- Course logistics: greetings, attendance, breaks, device checks, "课件没发到群里"
- Self-referential meta: "本文分为五部分", "下面我们进入第二章", "读法建议"

Allowed in a quote or an example dialogue: "今天怎么样", "大家最熟悉", "我们公司" — these are content, not lecturer voice.

## Rewrite Table

| 讲课式 / 流水账 | 笔记式 |
|---|---|
| 上一讲我们拆了一款完整产品；这一讲换方向，从 0 到 1 做产品。 | 做一款 AI 产品，第一步不是想功能，而是判断做什么、为谁做、值不值得做。 |
| 老师开场先给了一个判断：…… | **核心判断**：…… |
| 课件里的高德项目原始文档有三四十个，老师给大家看的是重新结构化过的版本。 | 真实项目的原始文档可能有三四十个，结构各不相同；文档的目的不是格式正确，而是把事情说清楚。 |
| 课堂上模拟了一个真实场景： | 典型场景： |
| 老师举了一个经典伪需求： | 经典伪需求： |
| 老师提醒：不要一板一眼地问五个为什么。 | 不要一板一眼地问五个为什么。 |
| 这一段/下面我们来看/接下来老师会讲 | 直接进入下一节，或省略 |
| 同学们/大家 | 你 / 读者 / 省略 |
| 这页课件/这张图 | 图注，或直接引用图中结论 |
| 课堂口径：3.05 → 1.67 | 3.05 → 1.67；统一放到文末「数据说明」 |

## Structure

- **H1**: `{主题}：{阶段}` or `{主题}`. No "课堂笔记" in the title unless the user asks for it.
- **Opening**: one-line definition + one-line mainline. No course review, no lecturer introduction.
- **H2**: Chinese numerals, `## 一、...`, `## 二、...`.
- **H3**: decimal numbering, `### 1.1 ...`, `### 1.2 ...`.
- **H4**: only for sub-steps inside a method; use `####` sparingly.
- **No H2 named "案例"**. Examples live under the H3 they support.
- **No "总结" H2** unless it adds a new synthesis (e.g., a three-station evidence chain). A summary that repeats the sections is filler.

## Paragraphs and Tables

- Prefer short paragraphs (2–4 sentences) and bullet lists for steps.
- Use a table when the content is inherently tabular: steps, fields, comparison, decision matrix, before/after.
- Do not put a long narrative into a table; do not put a table's worth of fields into prose.
- Every table needs a header and a separator row.

## Examples

Format:

```
> **例｜小红书：要不要开放长文章？**
>
> ...
>
> 这个例子说明：**同一个需求，写作、编辑、发布、阅读是四个场景。**
```

Rules:

- Use `例｜` for positive cases, `反例｜` for negative cases.
- The label should name the case, not the lesson: `例｜记账：为什么坚持不下来？`, not `例｜需求的真实性`.
- Put the example immediately after the point it proves.
- Keep concrete details: roles, numbers, quotes, what was tried, why it failed.
- End with one sentence that states the lesson or the design implication.
- If a case is used in several sections, split it; do not repeat the whole story.

## Interview Q&A

When the courseware includes questions with answers:

```
### Q1 这个功能不加 AI 解决不了吗？

**框架**：还原场景 → 现在怎么凑合 → 卡在哪 → AI 带来什么 → 不加也行就承认。

**参考话术**

> ...

**补充**

- ...

**换成你的**：...
```

Rules:

- Keep the courseware's framework and reference answer, but rewrite the wording so it reads as a note.
- Add course examples under `**补充**`.
- Add a `**换成你的**` prompt so the reader can practice.
- Do not include questions from a later part unless the user asks for them.

## Data and Caveats

- Put uncertain numbers in one short `### 数据说明` at the end.
- Say what the number is and what it is not: "案例数据，未回原始报告核对" or "业务方测算，不是上线结果".
- Do not write "课堂口径" or "待核实" next to every number.
- If a number is essential to the argument and unverified, keep it but mark it once in the data note.

## Final Checklist

- [ ] No banned phrases in the body.
- [ ] H2 uses Chinese numerals; H3 uses decimal numbering.
- [ ] Every example is under a knowledge point, not under a "案例" H2.
- [ ] Every image path exists and the figure is legible.
- [ ] Tables have consistent columns.
- [ ] Interview questions have framework + reference answer + supplement + practice prompt.
- [ ] Data note is present and short.
- [ ] Reading the first page does not sound like a lecture.
