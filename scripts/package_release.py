#!/usr/bin/env python3
"""Build a release from a clean commit; retain both languages and all notices."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', required=True, type=Path, help='New directory outside the source tree')
args = parser.parse_args()
target = args.output.expanduser().resolve()
if target.exists() or target == root or root in target.parents:
    parser.error('choose a new output directory outside the source tree')
if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root).strip():
    parser.error('commit source changes before packaging')
subprocess.run([sys.executable, '-B', 'scripts/check_docs.py'], cwd=root, check=True)
meta = json.loads((root / 'skill.json').read_text(encoding='utf-8'))
target.mkdir(parents=True)
stem = meta['name'] + '-v' + meta['version']
archive = target / (stem + '.zip')
files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as out:
    for name in sorted(filter(None, files)):
        out.write(root / name, stem + '/' + name)
with zipfile.ZipFile(archive) as out:
    assert out.testzip() is None
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
(target / (archive.name + '.sha256')).write_text(digest + '  ' + archive.name + '\n')
receipt = {'version': meta['version'], 'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip(),
           'asset': archive.name, 'sha256': digest, 'bytes': archive.stat().st_size}
(target / 'release-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
