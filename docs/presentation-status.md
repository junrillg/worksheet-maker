# Presentation verification record

Updated 2026-11-17 for Worksheet Maker 1.3.0. Scope: publish the skill, agent installation guidance, and a required update-before-work gate with a bundled Git updater. No worksheet generation run or live agent installation is claimed.

| Requirement | Status | Evidence | Next action |
|---|---|---|---|
| Identity | Verified locally | README references `assets/logo.svg`; matching social assets prepared separately. | Logo inspected at 32/88 px on white and dark grounds; social PNG is 1280 × 640 and 79,403 bytes. |
| README and claims | Verified against source | Content modes, A4 defaults, separate PDFs, and limitations trace to `skills/worksheet-maker/SKILL.md`. | Repository validator passed; local links and common manifest metadata agree. |
| Product evidence | Verified as workflow illustration | `assets/workflow.svg` is explicitly labeled as an illustration of the instructions. No sample PDF or executed generation is presented. | Export inspected; source-backed workflow labels and output split are legible. |
| First use | Source-inspected | README shows clone, agent-read instruction, and help prompt. It distinguishes prompts from shell commands and cloning from installation. | Execute help in a capable agent if behavioral evidence is needed. |
| System explanation | Verified against source | README maps skill, manifests, usage, and external agent tooling. | Common manifest fields and interface metadata validated. |
| Participation | Implemented | `CONTRIBUTING.md` documents checks and safe synthetic examples without inventing a support commitment or private reporting channel. | `python3 scripts/validate.py` and `sh -n scripts/export-assets.sh` passed. |
| License | Owner-deferred | No license supplied; README states that public availability does not grant a reuse license. | Owner selects terms before a license is added. |
| GitHub metadata | Published; visibility verified | Proposed values below; social image is an asset, not an uploaded repository preview. | Published to `junrillg/worksheet-maker` on `main`; GitHub displays Public and the prepared description. Topics remain suggestions; social card remains a committed asset, not an uploaded preview. |
| Rendering | Live dark-theme checks passed; light-theme assets checked locally | GitHub README inspected at 1400 px viewport (838 px article) and 390 px viewport (309 px article). Logo and workflow load; no page overflow. Code blocks retain their normal horizontal scrolling on mobile. | Full README in GitHub light mode was not inspected; the existing account appearance was preserved. |

## Prepared GitHub metadata

| Field | Value |
|---|---|
| Repository | `junrillg/worksheet-maker` |
| Visibility | Public, as requested by the owner |
| Description | Agent skill for A4 printable worksheets and separate answer keys, with faithful question reproduction and checked monochrome illustrations. |
| Homepage | None; no hosted application is provided. |
| Topics | `agent-skills`, `worksheets`, `education`, `pdf`, `printable`, `codex` |
| Social image | `assets/social-preview.png` |
| Editable social source | `assets/social-preview.svg` |

Repository validation and presentation checks do not certify generated educational content. An actual worksheet run requires the PDF and picture review described in the skill.

## Initial publication review evidence

An independent source review found no material issues. At initial publication, the skill matched the selected installed 1.2.2 source byte for byte (SHA-256 `2b828cfe8b8b7fd346c1cf345dfd5f23fb5829b247354fa1521f9a480f328fde`). Metadata copy was aligned with exact reproduction defaults; the original publication did not change skill behavior. Version 1.3.0 subsequently adds the required update gate and helper. The validator checks repository structure and selected contracts, not a complete plugin-schema conformance test or PDF output.

## Initial publication evidence

The initial content commit is `042bf1b30bf6268dfda0512ebf697a312c1d1476`. GitHub Actions [Validate repository run 1](https://github.com/junrillg/worksheet-maker/actions/runs/44005512850) passed on that commit. Public visibility, `main`, the committed files, README image loading and live navigation were observed on GitHub. That record update changed documentation only. No license, release, plugin installation or hosted application was created. The installed plugin cache was left unchanged.

## Version 1.3.0 implementation and checks

| Requirement | Status | Evidence / next action |
|---|---|---|
| Agent installation | Implemented | README links to a copyable agent prompt and `docs/installation.md`, with host-specific local discovery paths and managed-install limitations. No actual host installation is claimed. |
| Update before worksheet work | Implemented | `SKILL.md` places the mandatory update gate immediately after help; help still stops without tools or network. |
| Git updater | Verified offline | 14 integration tests passed: up-to-date, fast-forward, dirty/untracked/ignored changes, wrong origin/branch, detached HEAD, ahead/diverged history, fetch failure, disabled hooks, help without Git, and symlink resolution. |
| Package consistency | Verified locally | Both manifests, skill and README use 1.3.0; repository validator passed and CI includes the offline updater tests. |
| Managed installations | Explicit limitation | Requires the host update mechanism and verification of active installed files. Existing 1.2.2 packages need an initial update to receive the new gate. The installed plugin cache is not edited by this repository change. |

A separate material review found no blocking issues in the update gate, helper or installation instructions. A fresh help invocation returned usage only. The production diagram was relabeled to make its position after the required update gate clear and its export was visually inspected. Installation paths and symlink support were checked against the current official Codex and Claude Code documentation linked in the installation guide. Live installation, actual GitHub network fetching by the helper, and managed-plugin upgrading were not exercised in this environment.
