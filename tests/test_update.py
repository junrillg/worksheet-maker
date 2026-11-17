"""Offline integration tests: only temporary local Git repositories are used."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/worksheet-maker/scripts/update.py'
spec = importlib.util.spec_from_file_location('worksheet_update', HELPER)
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def git(root, *args):
    env = os.environ.copy()
    env.update(GIT_AUTHOR_NAME='Test Author', GIT_AUTHOR_EMAIL='test@example.invalid',
               GIT_COMMITTER_NAME='Test Author', GIT_COMMITTER_EMAIL='test@example.invalid')
    result = subprocess.run(['git', '-c', f'core.hooksPath={os.devnull}', '-C', str(root), *args],
                            env=env, capture_output=True, text=True, check=True)
    return result.stdout.strip()


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.remote = self.base / 'remote.git'
        self.seed = self.base / 'seed'
        self.clone = self.base / 'installed'
        self.seed.mkdir()
        git(self.base, 'init', '--bare', '--initial-branch=main', str(self.remote))
        git(self.seed, 'init', '--initial-branch=main')
        (self.seed / 'skills/worksheet-maker/scripts').mkdir(parents=True)
        (self.seed / 'skills/worksheet-maker/SKILL.md').write_text('# Fixture\n')
        (self.seed / 'plugin.json').write_text('{}\n')
        shutil.copy2(HELPER, self.seed / 'skills/worksheet-maker/scripts/update.py')
        git(self.seed, 'add', '.')
        git(self.seed, 'commit', '-m', 'Initial fixture')
        git(self.seed, 'remote', 'add', 'origin', str(self.remote))
        git(self.seed, 'push', 'origin', 'main')
        git(self.base, 'clone', str(self.remote), str(self.clone))
        self.before = git(self.clone, 'rev-parse', 'HEAD')

    def run_update(self):
        return updater.update(self.clone, trusted_url=str(self.remote))

    def advance(self):
        (self.seed / 'new.txt').write_text('An upstream update\n')
        git(self.seed, 'add', 'new.txt')
        git(self.seed, 'commit', '-m', 'Advance upstream')
        git(self.seed, 'push', 'origin', 'main')
        return git(self.seed, 'rev-parse', 'HEAD')

    def local_commit(self):
        (self.clone / 'local.txt').write_text('Local work\n')
        git(self.clone, 'add', 'local.txt')
        git(self.clone, 'commit', '-m', 'Local commit')
        return git(self.clone, 'rev-parse', 'HEAD')

    def test_up_to_date(self):
        self.assertEqual(self.run_update(), f'UP-TO-DATE: {self.before}')

    def test_fast_forward(self):
        target = self.advance()
        result = self.run_update()
        self.assertIn(f'{self.before} -> {target}', result)
        self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), target)
        self.assertEqual((self.clone / 'new.txt').read_text(), 'An upstream update\n')

    def test_tracked_change_preserved(self):
        path = self.clone / 'plugin.json'
        path.write_text('local edits\n')
        with self.assertRaisesRegex(updater.UpdateError, 'local changes'):
            self.run_update()
        self.assertEqual(path.read_text(), 'local edits\n')
        self.assertFalse((self.clone / '.git/FETCH_HEAD').exists())

    def test_untracked_change_preserved(self):
        path = self.clone / 'notes.txt'
        path.write_text('Private local notes\n')
        with self.assertRaisesRegex(updater.UpdateError, 'untracked'):
            self.run_update()
        self.assertEqual(path.read_text(), 'Private local notes\n')

    def test_ignored_local_file_not_overwritten(self):
        # Keep the checkout clean while Git ignores a user's local file.
        (self.clone / '.git/info/exclude').write_text('new.txt\n')
        path = self.clone / 'new.txt'
        path.write_text('Private ignored local content\n')
        self.advance()
        with self.assertRaisesRegex(updater.UpdateError, 'merge failed'):
            self.run_update()
        self.assertEqual(path.read_text(), 'Private ignored local content\n')
        self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), self.before)

    def test_wrong_origin(self):
        git(self.clone, 'remote', 'set-url', 'origin', str(self.base / 'other.git'))
        with self.assertRaisesRegex(updater.UpdateError, 'Origin'):
            self.run_update()
        self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), self.before)

    def test_wrong_branch(self):
        git(self.clone, 'switch', '-c', 'feature')
        with self.assertRaisesRegex(updater.UpdateError, 'on main'):
            self.run_update()

    def test_detached_head(self):
        git(self.clone, 'checkout', '--detach', self.before)
        with self.assertRaisesRegex(updater.UpdateError, 'on main'):
            self.run_update()

    def test_local_ahead(self):
        local = self.local_commit()
        with self.assertRaisesRegex(updater.UpdateError, 'ahead of or diverged'):
            self.run_update()
        self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), local)

    def test_diverged(self):
        local = self.local_commit()
        self.advance()
        with self.assertRaisesRegex(updater.UpdateError, 'ahead of or diverged'):
            self.run_update()
        self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), local)
        self.assertFalse((self.clone / 'new.txt').exists())

    def test_fetch_failure(self):
        self.remote.rename(self.base / 'unavailable.git')
        with self.assertRaisesRegex(updater.UpdateError, 'fetch failed'):
            self.run_update()
        self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), self.before)

    def test_hooks_not_executed(self):
        self.advance()
        marker = self.base / 'hook-executed'
        hook = self.clone / '.git/hooks/post-merge'
        hook.write_text(f'#!/bin/sh\ntouch "{marker}"\n')
        hook.chmod(0o755)
        self.run_update()
        self.assertFalse(marker.exists())

    def test_help_without_git_or_checkout(self):
        isolated = self.base / 'copy.py'
        shutil.copy2(HELPER, isolated)
        env = os.environ.copy()
        env['PATH'] = ''
        result = subprocess.run([sys.executable, str(isolated), '--help'], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('usage:', result.stdout)
        self.assertFalse((self.clone / '.git/FETCH_HEAD').exists())

    def test_symlink_resolves_managed_checkout(self):
        linked = self.base / 'discovered-skill'
        linked.symlink_to(self.clone / 'skills/worksheet-maker', target_is_directory=True)
        linked_spec = importlib.util.spec_from_file_location('linked_updater', linked / 'scripts/update.py')
        module = importlib.util.module_from_spec(linked_spec)
        old = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = True
            linked_spec.loader.exec_module(module)
        finally:
            sys.dont_write_bytecode = old
        self.assertEqual(module.update(trusted_url=str(self.remote)), f'UP-TO-DATE: {self.before}')


if __name__ == '__main__':
    unittest.main()
