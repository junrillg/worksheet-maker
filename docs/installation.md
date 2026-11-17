# Install and update Worksheet Maker

Use a supported agent installation method so the complete skill directory, including its update helper, stays together. The instructions below cover owner-controlled local Codex and Claude Code installations on macOS/Linux. App-managed plugins and synced skills follow their host's installation rules instead.

## Ask your agent to install it

Copy this prompt into your coding agent:

```text
Install Worksheet Maker from https://github.com/junrillg/worksheet-maker.
Read this repository's docs/installation.md and entire skills/worksheet-maker/SKILL.md.
Identify this agent's supported skill installation mechanism and use user scope;
use project scope only if I explicitly request it.
If local skill links are supported, clone the complete canonical repository on main
to ~/.local/share/worksheet-maker and link its skills/worksheet-maker directory
into the appropriate skill-discovery directory. Preserve existing files, local edits,
and duplicate installations; report a conflict instead of overwriting one.
If this host requires a managed installer, use that supported lifecycle instead.
Verify the active skill path and update helper, then report the version and commit.
Every non-help worksheet request must check and install available updates before work.
Read the updated SKILL.md after updating. Verify help prints usage without tools
or network calls. Do not claim installation succeeded until discovery is verified.
```

Check for an existing `worksheet-maker` in local skills, plugin registries, and synced skills before installing. A same-named plugin may take precedence over a local copy. Identify which one the agent actually loads rather than silently creating a duplicate.

## Local Git installation

Prerequisites: Git, Python 3.9+, network access, and permission to write the selected locations. Follow any host-specific installer requirement before these generic filesystem steps. These commands do not register a plugin in ChatGPT or modify a plugin cache.

Clone the full repository to a dedicated directory, outside the skill-discovery directories:

```sh
mkdir -p "$HOME/.local/share"
git clone --branch main --single-branch \
  https://github.com/junrillg/worksheet-maker.git \
  "$HOME/.local/share/worksheet-maker"
```

If the destination already exists, stop and inspect it. Reuse it only after confirming its origin, branch, and local changes; do not delete it or bypass a failed clone. The updater requires the canonical HTTPS origin and a clean `main` checkout.

Choose the discovery directory for the intended agent and scope:

| Agent | User scope, across projects | Project scope, only when requested |
|---|---|---|
| Local Codex | `~/.agents/skills/worksheet-maker` | `.agents/skills/worksheet-maker` |
| Claude Code | `~/.claude/skills/worksheet-maker` | `.claude/skills/worksheet-maker` |

For **Codex user scope**, run this only after the clone succeeds:

```sh
set -eu
worksheet_skill_parent="$HOME/.agents/skills"
worksheet_skill_target="$worksheet_skill_parent/worksheet-maker"
mkdir -p "$worksheet_skill_parent"
if [ -e "$worksheet_skill_target" ] || [ -L "$worksheet_skill_target" ]; then
  printf '%s\n' 'Worksheet Maker already exists; inspect it before changing anything.'
else
  ln -s "$HOME/.local/share/worksheet-maker/skills/worksheet-maker" \
    "$worksheet_skill_target"
fi
```

For **Claude Code user scope**, use the same block with `worksheet_skill_parent="$HOME/.claude/skills"`. For an explicitly requested project installation, use the corresponding project directory from the table. Keep the link target absolute. Do not link the entire `.agents/skills` or `.claude/skills` directory and do not force replacement of an existing skill.

Verify that the link resolves to the dedicated clone, `SKILL.md` and `scripts/update.py` exist there, and the agent discovers that same path. Ask the agent to run `worksheet-maker help`: the expected result is the usage block only. If discovery is stale, refresh the skill list or open a fresh agent session as supported by that client. Report the version in `SKILL.md` and the checkout's `git rev-parse HEAD`; a successful clone alone is not an installation check.

## Check and install updates

Every non-help invocation must check for updates **before** inspecting worksheet inputs. For the local installation above, the agent runs:

```sh
python3 "$HOME/.local/share/worksheet-maker/skills/worksheet-maker/scripts/update.py"
```

The helper verifies the dedicated repository, canonical origin, `main` branch, and clean working tree. It fetches `main` and fast-forwards when an update is available. It reports either up-to-date or updated, with commit identifiers. It does not reset, stash, clean, force-push, run downloaded installers, or install PDF dependencies. Each Git command has a bounded timeout.

After a successful check, the agent reads the current `SKILL.md` again and follows it for the original request. Do not repeat the preflight after reloading during the same invocation; check again on the next worksheet request. `worksheet-maker help`, `--help`, and `-h` skip the update preflight entirely.

To inspect helper usage without an update:

```sh
python3 "$HOME/.local/share/worksheet-maker/skills/worksheet-maker/scripts/update.py" --help
```

If the checkout is dirty, ahead, diverged, on another branch, or has the wrong origin, the helper refuses to update. Network and authentication failures also stop the preflight. Explain the specific problem and preserve local work. Resume after recovery, or use the installed version only when the user explicitly requests that fallback. Never report a failed check as “up to date.”

## App-managed plugins and copied skills

For ChatGPT plugins, synced skills, read-only installations, or other host-managed skills, check and install updates through that host's supported mechanism. Do not edit generated plugin-cache files, assume local discovery paths apply, or run `git pull` inside a cache. If the host cannot check or install an available update, report that limitation and pause; continuing with the current version needs the user's explicit choice.

A loose copy of `SKILL.md` cannot use the Git helper. Reinstall the complete skill through the supported mechanism or use the linked Git installation above when allowed. This repository update does not itself upgrade an already installed plugin or prove that a local installation has been discovered.

## Client documentation

- [Codex skill discovery and symlink support](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skill discovery and installation](https://code.claude.com/docs/en/skills)

Client behavior can change. An agent must follow its host's current supported installer and permission model before using these local commands.
