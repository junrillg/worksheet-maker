---
name: worksheet-maker
description: Create clean A4 printable worksheets and a separate answer key from pasted questions, worksheets, exams, photos, or screenshots. Preserve supplied questions and format exactly by default; create new or adapted practice only when explicitly requested. Supports every school subject with checked monochrome illustrations.
---

# Worksheet Maker

## Arguments

`worksheet-maker [help | --help | -h | <request>]`

`request` is optional free text describing the worksheet task; by default, use the user's current request and attached source pages. Attachments are optional files, not command-line arguments. When questions are supplied, reproduce those exact questions and their format by default; see Mode selection below. Subject, level, topic, and difficulty come from the source when evident; use A4 portrait, monochrome student PDF plus a separate answer key by default. Combined PDFs, randomized sets, and editable sources require an explicit request. There are no other command flags.

## Help — stop before doing anything else

If the first argument is `help`, `--help`, or `-h` (case-insensitive), print the usage block below and STOP. Do not inspect attachments, read other files, run preflight, call tools or subagents, access the network, generate content, or write files on this path.

```text
Worksheet Maker — create subject-independent printable practice PDFs from source material.
Usage: worksheet-maker [help | --help | -h | <request>]

Arguments:
  request     Free text; optional; default: current request and attached source pages.
              Describe the subject, level, topic, or desired changes when needed.
  help        Help selector; optional; no default; prints usage and stops.
  --help, -h  Aliases for help; optional; no default; case-insensitive as first argument.
  attachments Optional uploaded worksheets/photos/PDFs; default: current attachments.
              Attach in chat; these are not command-line flags.

Defaults: A4 portrait, crisp monochrome illustrations where source tasks use pictures,
the exact supplied questions, order, and format, complete source coverage,
and separate student and answer-key PDFs.
Opt-in: explicitly request new/adapted questions, combined PDFs, randomized sets, or editable sources.

Examples:
  worksheet-maker help
  worksheet-maker Create new Civics practice from these attached worksheets.
  worksheet-maker Adapt these Science pages for Grade 2; include an answer key.
  worksheet-maker Make English practice from these pages and an editable source.

Clarification: asks one short question only if an essential subject, topic,
difficulty, source reading, or other detail cannot be inferred. Report unavailable
required image/PDF tools; never claim files or checks were completed when they were not.

Internal pointers: Inventory the entire source set; Create a coverage matrix;
Design the printable pages; Illustrate accurately; Render, inspect, and deliver;
Version 1.2 quality safeguards (required).
```

## When to activate

Use when a user pastes questions or supplies photos, scans, screenshots, PDF pages, or documents and asks to **format, recreate, regenerate, adapt, review, expand, or produce printable worksheets**, exam practice, assessment sets, or answer keys. Alternate name: **Printable Worksheet PDF Generator**.

## Mode selection: supplied questions mean exact reproduction

When the user provides questions, treat them as the requested worksheet content, not merely examples to inspire a different assessment. This applies to pasted text as well as attachments. A bare skill invocation with supplied questions, or words such as "make a worksheet", "recreate", "regenerate", "clean up", or "printable", defaults to **exact reproduction**. Do not ask the user to confirm this default.

- **Exact reproduction (default with supplied questions):** Preserve every question, subpart, word, number, unit, mathematical symbol, punctuation mark, answer choice and its order, numbering, heading, instruction, scenario, table, required marker, rubric, and point value. Preserve the supplied activity format, option arrangement, and response format. Do not paraphrase, change examples or values, add practice or hints, reorder items, rebalance answer letters, or add diagrams absent from the source.
- **New or adapted practice (explicit opt-in):** Write or change questions only when the user clearly requests it, for example "new questions", "similar practice", "change the numbers", "adapt for Grade 2", or "randomize the choices". Apply only the requested transformation; preserve other content and format. When no questions are supplied and the user asks for practice on a topic, create suitable original questions.
- In exact mode, improve legibility, typesetting, and print pagination without changing content or the supplied structure. Preserve original page layout when it is available as a reference; when only pasted text is provided, preserve its section order, vertical/horizontal choice arrangement, subparts, and response format. Do not invent an unavailable original page layout or claim pixel-perfect matching.
- Remove only chat/Markdown transport escapes, not substantive characters. Do not silently correct a possible source error or ambiguity; preserve it and flag it separately in the answer key or delivery note. Ask one targeted question only if unreadable or missing source content prevents faithful reproduction.

## Version and non-negotiable illustration policy

Version: **1.2.2** (2026-11-14; exact supplied questions and format by default). When the source uses pictures, **the regenerated worksheet MUST also use accurate, legible pictures**, not text-only substitutes. Treat all picture answers as correctness-critical. Follow [Image quality gate](#version-12-quality-safeguards-required) and [Picture asset workflow](#4-illustrate-accurately) before final delivery.

## Default deliverables

1. `Subject_Level_Worksheet.pdf` — a clean A4 black-and-white, ink-efficient, ready-to-print student PDF preserving the supplied questions and format; use original or adapted questions only in the explicitly selected mode. Preserve picture content and labels when redrawing for legibility.
2. `Subject_Level_Answer_Key.pdf` — an independent teacher/parent key mapping unambiguously to every exercise, including acceptable answers for drawing and open-ended questions.
3. If requested, a combined all-in-one PDF, a second randomized set, or an editable source version.

Never provide only plain text when the user asked for a printable PDF.

## Workflow

### 1. Inventory the entire source set

- Inspect **all** supplied text, uploaded pages, and images, including second pages and reverse-side photos. In exact mode, transcribe and inventory every question and all accompanying instructions, options, task details, and scoring text.
- Record each lesson/topic, vocabulary item, skill, and type of activity actually assessed.
- Keep track of picture-based tasks separately; a picture-based source requires pictures in the new worksheet.
- Extract educational objectives, **not student scores, student names, grades, markings, logos, or private details**. Refrain from copying school branding unless explicitly authorized.
- In exact mode, do not infer unreadable wording from its apparent objective; ask for the missing text when it is essential. In explicitly requested new-practice mode, infer only when the educational objective is clear.

### 2. Create a coverage matrix

In exact mode, create a private fidelity checklist: `source item | exact text and format | output location | picture asset | answer check`. Include instructions, options, subparts, scenarios, tables, and rubrics, not only question stems. In new-practice mode, use `source topic | learning objective | source formats | replacement exercise | picture asset | answer check`.

In exact mode, require every supplied item to appear unchanged and in its original order. In new-practice mode, require every distinct objective and exercise family from the complete source to appear in the new pack. Example exercise types: multiple choice; True/False; Yes/No; needs/wants or other categorization; picture identification; picture-choice scenarios; labeling; word banks; matching; completion; drawing; short applied situations.

**Only in explicitly requested new-practice mode**, preserve learning scope and age level while writing new questions. Change examples, wording, distractors, or choice order only as authorized by the request. Safe transfer questions are appropriate in this mode, never an automatic addition to exact reproduction. Don't inject concepts above the source's age/grade unless requested.

### 3. Design the printable pages

- A4 portrait by default, no bleeds, safe side margins around 12–14 mm, footer inside page.
- Black line art, white backgrounds, adequate stroke widths, **no grayscale full-page texture** or decorative ink-heavy fills.
- Primary-school readable text, typically 10–12 pt minimum; larger where appropriate. Leave substantial writing/drawing space.
- In exact mode, preserve the supplied numbering, section headings, and instructions verbatim. In new-practice mode, use consistent numbering and clear instructions.
- Preserve supplied name/date fields and section headings. Do not insert new question headings or instructions in exact mode. Print page numbers may be added without changing item order. Do not pre-fill student personal information.
- Avoid orphaned questions, overlapping text, clipped images and blank lines crossing page boundaries.
- Keep illustrations close to the exact question and options that use them. Correct pictures must be unmistakable and distinct from distractors. Include visibly different art for each alternative.
- Pictures should be **crisp vector artwork or clean line art**, not low-quality pasted photos, broken fonts, or emoji. In exact mode, preserve the source picture content, labels, quantity, arrangement, and answer-relevant details; redraw only to improve print clarity. Illustrations must actually represent the named concept.

### 4. Illustrate accurately

- Use the environment's appropriate image/vector tools to generate simple high-contrast printable artwork.
- For an item asking to identify a dental clinic, a market, or a bedroom, the pictures must have unique, recognizable visual cues; reject generic storefronts/interiors that look alike. The picture for a nurse must actually depict a nurse, not a hospital building.
- Draw a house diagram with labels outside the diagram or numbered markers with a keyed word bank; avoid ambiguity.
- Use properly recognizable scene illustrations for pictures of people, workplaces and rooms, not abstract substitutes or stick figures when a detailed drawing is needed. Black-and-white line art may be simple, but it must contain the defining objects.
- Do not let long separator lines cross question text: inspect graphics AND text, because ordinary text-bound checks cannot detect line-through errors.
- Keep a picture-choice group together and align all option labels consistently.
- Inspect generated art visually rather than assuming it is correct.
- If an image generator renders art, verify spelling, anatomy, object count, and answer consistency. Redraw inaccurate artwork rather than embedding it. **Never** paste an AI-generated collage of whole worksheets as PDF pages; independently lay out typeset questions and checked individual artwork.
- Prefer vector illustrations for black-and-white pictorial exercises; raster images must be high enough resolution at placed size.
- Maintain a per-question image manifest (concept, visual cues, image path, distractor, answer, placement, rendered confirmation), and apply the six-stage [visual QA gate](#version-12-quality-safeguards-required). A rendered contact sheet alone is not a substitute for semantic review of *every* picture.

### 5. Build the answer key **from the actual final PDF**

- Walk through every final question in order and make sure each key entry matches its final option order.
- Multiple-choice keys must name both letter/position and answer.
- For image-choice answers provide picture number and label.
- For open-ended drawing, state possible accepted answers; never require a unique drawing.
- Check whether choices have exactly one appropriate answer unless explicitly multiple-select. If an exact source item has a flawed or ambiguous answer set, preserve the worksheet and flag the issue separately in the key; do not silently replace a choice.

### 6. Render, inspect, and deliver

- Use the installed PDF skill's render → inspect → refine workflow. Render ALL PDF pages, preferably at 150–200 dpi, and look for clipping, image correctness, overlap, missing glyphs, insufficient blank space and poor contrast.
- Programmatically check the final PDFs with PyMuPDF: verify each page is A4 portrait (approximately 595.28 × 841.89 pt, allowing 1 pt tolerance); check nonempty text span bounds against the page and safe print margins; warn on images or drawing bounds outside the page, unexpectedly empty pages, and missing expected picture assets. Inspect every warning and correct justified problems. These geometry checks cannot confirm picture meaning or detect every separator line crossing text, so retain the visual checks below. Also inspect complex illustrations individually at 120 dpi print-preview size.
- In exact mode, compare the final extracted PDF text item by item against the supplied source, normalizing only line wrapping and transport escapes. Check every value, symbol, choice, instruction, and scoring detail, then visually verify the supplied format and option arrangement. Do not claim exact reproduction until this comparison passes.
- Verify the answer key against the latest final PDF, including all picture options and drawing prompts.
- Keep the final student PDF separate from the key to prevent accidental distribution of answers.
- Link verified `/mnt/data/...` files in ChatGPT, or the actual supported output directory when running elsewhere. Include a short statement of what topics and question formats are covered.
- If the user requests an additional reusable skill, produce this `SKILL.md` and a ZIP containing support files.

## Version 1.2 quality safeguards (required)

1. **No missing image choices:** For every picture prompt, count the images in the rendered PDF and ensure it equals the number of printed choices. Do not silently replace a requested picture with an icon or blank box.
2. **Scene meaning is non-negotiable:** A kitchen must visibly contain kitchen furniture/appliances; a nurse must look like a medical worker; a dental clinic must have a dental cue. Look at every picture at normal printable scale, not only the contact sheet.
3. **Asset independence:** Separate source illustration assets from wording and answer markers. If working from a composite image, crop *individual* artwork only, remove captions/borders, and review each crop. Do not place a composite of whole completed worksheets in the PDF.
4. **Print-friendly quality:** Prefer vector artwork. For raster art, select sufficiently sharp originals at print size; do not treat upscaling as added true detail. If the original is inadequate, redraw rather than upsample only.
5. **Page layout:** Ensure options and pictures stay within their own cards. Check that horizontal rules, connectors, diagram numbers and captions do not cross text or artwork. Rerender after every fix.
6. **Answer-key synchronization:** Finalize question ordering first, then verify answer keys against the generated student PDF, including image choice positions and plausible alternative drawing answers.

Read the [Picture asset workflow](#4-illustrate-accurately) for an executable image-preparation checklist.

## Subject-specific caution

This skill is **subject-independent**. Do not put "Number Sense", dyscalculia, or any label that was not in the source or requested onto ordinary student worksheets. In Kindergarten arithmetic, neatly structured dot quantity patterns may be helpful only when the user asks or the source shows them; keep numerals and operators visible. For science, reading, language, writing, civic studies, and social studies, use visual aids suited to the actual subject rather than math-oriented imagery.

## If information is missing

Proceed with reasonable defaults if the subject, topic and difficulty are evident. Ask one short clarifying question only when a missing detail is essential and cannot be inferred. Do not claim 100% coverage until all supplied text and uploaded pages have been inspected and mapped. Do not treat a clear supplied question set as a request for different questions.

## Internal workflow and quality checks

- [Source inventory](#1-inventory-the-entire-source-set)
- [Exercise coverage matrix](#2-create-a-coverage-matrix)
- [Printable layout and quality checks](#3-design-the-printable-pages)
- [Picture-asset preparation and semantic review](#4-illustrate-accurately)
- [Final PDF geometry, print preview, and delivery checks](#6-render-inspect-and-deliver)
- [Mandatory six-stage image and answer safeguards](#version-12-quality-safeguards-required)

This self-contained package uses the workflow above; it does not depend on external reference files, a bundled PDF-check script, or a Civics-specific example. Use the environment's available PDF and image tools. If a required capability is unavailable, explain what is missing and do not claim successful generation or verification.
