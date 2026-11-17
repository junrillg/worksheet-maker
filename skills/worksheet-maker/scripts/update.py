#!/usr/bin/env python3
"""Update a clean managed Worksheet Maker checkout from its canonical main branch.

Run with no arguments to check and apply a fast-forward update. --help/-h only
prints usage. A failure must stop the caller before worksheet production.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys

CANONICAL_URL = 'https://github.com/junrillg/worksheet-maker.git'


class UpdateError(Exception):
    """The caller must resolve the reported condition before proceeding."""


def git(root, *args, check=True):
    env = os.environ.copy()
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE',
                'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_NAMESPACE'):
        env.pop(key, None)
    env['GIT_TERMINAL_PROMPT'] = '0'
    try:
        result = subprocess.run(
            ['git', '--no-replace-objects', '-c', f'core.hooksPath={os.devnull}',
             '-c', 'core.fsmonitor=false', '-c', 'submodule.recurse=false',
             '-C', str(root), *args],
            env=env, capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired as error:
        raise UpdateError('Git timed out after 30 seconds; check network/access and retry explicitly.') from error
    except OSError as error:
        raise UpdateError('Git is unavailable; install Git or correct its executable path.') from error
    if check and result.returncode:
        # Do not echo arbitrary Git diagnostics: remotes/config can contain credentials.
        raise UpdateError(f'Git {args[0]} failed; check checkout permissions and network access. No success is claimed.')
    return result


def check_checkout(root, trusted_url):
    if not (root / 'skills/worksheet-maker/SKILL.md').is_file() or not (root / 'plugin.json').is_file():
        raise UpdateError('Not a managed full-repository install; follow the installation guide.')
    top = Path(git(root, 'rev-parse', '--show-toplevel').stdout.strip()).resolve()
    if top != root:
        raise UpdateError('The skill is inside a different repository; use a dedicated clone.')
    allowed = {trusted_url, trusted_url.removesuffix('.git')}
    raw = git(root, 'config', '--get-all', 'remote.origin.url').stdout.splitlines()
    effective = git(root, 'remote', 'get-url', '--all', 'origin').stdout.splitlines()
    if len(raw) != 1 or len(effective) != 1 or raw[0] not in allowed or effective[0] not in allowed:
        raise UpdateError('Origin is not the trusted Worksheet Maker repository; do not update this checkout.')
    branch = git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD', check=False)
    if branch.returncode or branch.stdout.strip() != 'main':
        raise UpdateError('The checkout must be on main; preserve branch work before switching.')
    if git(root, 'status', '--porcelain', '--untracked-files=all').stdout:
        raise UpdateError('The checkout has local changes or untracked files; preserve them before updating.')
    return git(root, 'rev-parse', '--verify', 'HEAD^{commit}').stdout.strip()


def update(root=None, trusted_url=CANONICAL_URL):
    """Return status text; trusted_url is injectable only for offline test fixtures."""
    root = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[3]
    before = check_checkout(root, trusted_url)
    git(root, 'fetch', '--no-tags', '--no-recurse-submodules', 'origin', 'refs/heads/main')
    target = git(root, 'rev-parse', '--verify', 'FETCH_HEAD^{commit}').stdout.strip()
    if check_checkout(root, trusted_url) != before:
        raise UpdateError('The checkout changed during the check; stop and retry explicitly.')
    if before == target:
        return f'UP-TO-DATE: {before}'
    ancestor = git(root, 'merge-base', '--is-ancestor', before, target, check=False)
    if ancestor.returncode:
        raise UpdateError('Local main is ahead of or diverged from upstream; preserve local commits and resolve manually.')
    git(root, 'merge', '--ff-only', '--no-edit', '--no-overwrite-ignore', target)
    after = check_checkout(root, trusted_url)
    if after != target:
        raise UpdateError('The resulting revision differs from the fetched revision; do not proceed.')
    return f'UPDATED: {before} -> {after}\nRe-read the updated SKILL.md before proceeding.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        print(update())
    except UpdateError as error:
        print(f'UPDATE BLOCKED: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
