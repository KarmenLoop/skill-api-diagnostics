#!/usr/bin/env python3
"""Check bilingual entry points and the versioned, reproducible output illustration."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
meta = json.loads((root / 'skill.json').read_text(encoding='utf-8'))
version = meta['version']
for name in ('README.md', 'README.zh-CN.md', 'docs/tutorial.en.md', 'docs/tutorial.zh-CN.md'):
    path = root / name
    content = path.read_text(encoding='utf-8')
    assert version in content, name + ': missing current version'
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if '://' not in target and not target.startswith('#'):
            assert (path.parent / target.split('#', 1)[0]).exists(), name + ': ' + target
assert 'README.zh-CN.md' in (root / 'install.py').read_text(encoding='utf-8')
assert 'version: "' + version + '"' in (root / 'SKILL.md').read_text(encoding='utf-8')
proof = json.loads((root / 'docs/images/provenance.json').read_text(encoding='utf-8'))
assert proof['version'] == version
for name, digest in proof['files'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
result = subprocess.check_output([sys.executable, '-B', 'scripts/run.py', '--input', 'examples/input.json'], cwd=root)
assert json.loads(result) == json.loads((root / 'examples/expected.json').read_text(encoding='utf-8'))
assert hashlib.sha256(result.replace(b'\r\n', b'\n')).hexdigest() == proof['stdout_sha256']
print(json.dumps({'ok': True, 'version': version, 'example': 'matches expected JSON', 'languages': ['en', 'zh-CN']}))
