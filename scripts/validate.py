#!/usr/bin/env python3
"""Check this repository's packaging, documentation, and presentation assets.

This does not run an agent or validate generated worksheet PDFs.
"""
import argparse
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


def validate(root):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    portable = json.loads((root / 'plugin.json').read_text())
    codex = json.loads((root / '.codex-plugin/plugin.json').read_text())
    skill = (root / 'skills/worksheet-maker/SKILL.md').read_text()
    require(skill.startswith('---\nname: worksheet-maker\n'), 'Skill frontmatter/name missing')
    require('description: ' in skill.split('---', 2)[1], 'Skill description missing')
    for key in ('name', 'version', 'description', 'author'):
        require(portable[key] == codex[key], f'Manifests disagree: {key}')
    for key, value in portable['extensions']['com.openai']['interface'].items():
        require(codex['interface'].get(key) == value, f'Plugin interface metadata differs: {key}')
    require(codex['skills'] == './skills', 'Skill discovery path changed')
    require((root / codex['skills'] / 'worksheet-maker/SKILL.md').is_file(),
            'Skill discovery path does not resolve')
    require(f'Version: **{portable["version"]}**' in skill, 'Skill/manifest version differs')
    help_at = skill.find('## Help')
    require(0 < help_at < skill.find('## When to activate'), 'Help must precede workflow')
    for contract in ('--help', '-h', 'STOP', 'Exact reproduction', 'explicit opt-in',
                     'separate', 'PyMuPDF', 'six-stage'):
        require(contract in skill, f'Missing skill contract: {contract}')

    def anchors(path):
        result = set()
        counts = {}
        for line in path.read_text().splitlines():
            match = re.match(r'^#{1,6}\s+(.+)', line)
            if not match:
                continue
            slug = re.sub(r'[^\w\- ]', '', match[1].lower()).replace(' ', '-')
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            result.add(slug if count == 0 else f'{slug}-{count}')
        return result

    for path in root.rglob('*.md'):
        if '.git' in path.relative_to(root).parts:
            continue
        text = path.read_text()
        urls = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', text)
        urls += re.findall(r'(?:href|src)="([^"]+)"', text)
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            target = path.parent / unquote(parsed.path) if parsed.path else path
            require(target.exists(), f'{path.relative_to(root)}: missing link {url}')
            if target.is_file() and target.suffix == '.md' and parsed.fragment:
                require(unquote(parsed.fragment) in anchors(target),
                        f'{path.relative_to(root)}: missing anchor {url}')
        require('/Users/' not in text, f'{path.relative_to(root)}: private local path')

    ns = '{http://www.w3.org/2000/svg}'
    for path in (root / 'assets').glob('*.svg'):
        document = ET.parse(path).getroot()
        require(document.tag == ns + 'svg', f'{path.name}: invalid SVG root')
        require(document.find(ns + 'title') is not None, f'{path.name}: missing title')
        require(document.find(ns + 'desc') is not None, f'{path.name}: missing description')
        for element in document.iter():
            require(element.tag not in (ns + 'script', ns + 'foreignObject', ns + 'image'),
                    f'{path.name}: not a self-contained vector')
            for key, value in element.attrib.items():
                require(not key.lower().startswith('on'), f'{path.name}: event handler')
                if key.endswith('href'):
                    require(value.startswith('#'), f'{path.name}: external reference')

    png = root / 'assets/social-preview.png'
    data = png.read_bytes()
    require(data[:8] == b'\x89PNG\r\n\x1a\n', 'Social image must be PNG')
    require(struct.unpack('>II', data[16:24]) == (1280, 640), 'Social image must be 1280x640')
    require(len(data) < 1_000_000, 'Social image must be under 1 MB')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        errors = validate(Path(__file__).resolve().parents[1])
    except (OSError, ValueError, KeyError, ET.ParseError, struct.error) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    for error in errors:
        print(f'FAIL: {error}', file=sys.stderr)
    if errors:
        return 1
    print('PASS: packaging, help/default contracts, local links, SVG safety, social-image dimensions/size')
    print('Not checked: agent execution, picture meaning, generated PDFs, or live GitHub rendering.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
