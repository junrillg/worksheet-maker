# Using Worksheet Maker

Start by asking your agent to read [SKILL.md](../skills/worksheet-maker/SKILL.md). Its arguments are prompt text interpreted by the agent. This package does not provide an executable named `worksheet-maker`.

## Get help first

```text
Use Worksheet Maker: worksheet-maker help
```

`help`, `--help`, and `-h` are case-insensitive when used as the first argument. This path prints usage and stops without inspecting attachments, running tools, accessing the network, or writing files.

## Updates before worksheet work

On every non-help request, check for updates before inspecting source pages or generating content. A managed local Git installation runs `scripts/update.py` from the resolved skill directory; an app-managed plugin uses its supported update mechanism. Install an available update first, then read the updated `SKILL.md` before continuing. Check once per invocation; the next worksheet request checks again.

If the check or update fails, stop and explain the recovery step. Continue with the current version only if the user explicitly requests that fallback. Do not overwrite local changes or patch a managed plugin cache. See [installation and update recovery](installation.md).

## Choose the content mode

| Request | Mode and expected behavior |
|---|---|
| “Recreate these questions as a printable worksheet.” | Exact reproduction: preserve every supplied question and its format. |
| “Make a worksheet from these pages.” | Exact reproduction is still the default. |
| “Create similar practice from these pages with new examples.” | New practice: preserve the learning scope and age level while applying the requested changes. |
| “Adapt these science questions for Grade 2.” | Adaptation: change only what the requested adaptation requires. |
| “Create Kinder 2 phonics practice with a few challenge questions.” | Original practice: no source questions are needed when topic and level are clear. |

In exact mode, a suspected source error is preserved and flagged separately. The agent must not silently fix a number, replace an answer choice, insert hints, or randomize the order. Unreadable essential text requires clarification.

## Example requests

Attach source pages when the request refers to them.

```text
Use Worksheet Maker to recreate all the questions in these photos.
Preserve their wording, order, picture choices, and activity format.
```

```text
Use Worksheet Maker to create new Kinder 2 phonics practice from these pages.
Include a few age-appropriate challenge questions and recognizable line art.
```

```text
Use Worksheet Maker to adapt these science questions for Grade 2.
Also provide an editable source version.
```

## Outputs and checks

By default the agent produces:

- `Subject_Level_Worksheet.pdf`: A4 portrait, monochrome, with writing space and accurate pictures where the task requires them.
- `Subject_Level_Answer_Key.pdf`: a separate key verified against the final student PDF, including picture positions and acceptable open-ended answers.

Combined PDFs, randomized sets, and editable sources are opt-in. A4 portrait is the default; preserving source content does not imply pixel-perfect reconstruction of an unavailable layout.

The workflow requires an inventory and coverage checklist, individual picture review, rendering of all PDF pages, geometry checks with PyMuPDF, and final key verification. Exact reproduction also requires item-by-item comparison of extracted PDF text against the source. These steps must run in the agent's environment; they are not performed by the repository validator.

## Required capabilities and limits

Use an agent with attachment inspection, PDF generation and rendering, illustration tools, and a PDF workflow. PyMuPDF is required for the specified geometry and text checks. No model, PDF engine, image generator, or dependency installer is bundled with this repository. The bundled updater requires Git, Python 3.9+, network access, and a managed Git checkout; it does not install PDF or image dependencies.

If a required tool is unavailable, the agent must report the missing capability. If an essential subject, level, topic, or source passage cannot be inferred, it asks a targeted question. Do not treat a generated PDF or a passing repository check as proof that every picture and answer is correct.

Share only material you have permission to use. Remove student identifiers, scores, markings, and private details from examples shared publicly.
