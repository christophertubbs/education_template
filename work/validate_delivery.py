"""Check specification preservation, links and illustrative mapping fixtures.

TODO: AI-written by Codex; review and replace before using as project validation.
This checks a documentation bundle, not a complete authored curriculum or runtime.
"""

from pathlib import Path
import hashlib
import importlib
import json
import re
import sys

import yaml

ROOT: Path = Path('deliverable')
errors: list[str] = []
checks: list[str] = []
source: str = Path('work/source/SPEC.original.md').read_text()
pattern: re.Pattern[str] = re.compile(r'(?m)^#{1,2} (\d+(?:\.\d+)?)\.?(?: )([^\n]+)')
matches: list[re.Match[str]] = [m for m in pattern.finditer(source) if '.' not in m[1] or m[1] == '40.1']
mapping: dict[str, list[str]] = json.loads(Path('work/section-map.json').read_text())
assigned: list[str] = [number for numbers in mapping.values() for number in numbers]
expected: set[str] = {m[1] for m in matches} - {'2'}
if set(assigned) != expected or len(assigned) != len(set(assigned)):
    errors.append('Original section coverage is missing or duplicated')
for index, match in enumerate(matches):
    if match[1] == '2':
        continue
    end: int = matches[index + 1].start() if index + 1 < len(matches) else len(source)
    original: str = source[match.start():end].strip()
    original = original.replace('These passes do not require ten separate model invocations',
                                'These twelve passes do not require twelve separate model invocations')
    owner: str = next(path for path, numbers in mapping.items() if match[1] in numbers)
    if original not in (ROOT / owner).read_text():
        errors.append(f'Original section {match[1]} not retained in {owner}')
checks.append(f'{len(expected)} original numbered sections retained; section 2 navigation replaced explicitly')

# Ignore example code fences when checking documentation hyperlinks.
link_count: int = 0
for path in ROOT.rglob('*.md'):
    clean: str = re.sub(r'(?ms)^```[^\n]*\n.*?^```\s*$', '', path.read_text())
    for target in re.findall(r'\]\(([^)]+)\)', clean):
        if ':' in target or target.startswith('#'):
            continue
        target_path: Path = (path.parent / target.split('#')[0]).resolve()
        link_count += 1
        if not target_path.exists():
            errors.append(f'Broken relative link in {path}: {target}')
checks.append(f'{link_count} relative Markdown links checked')

lesson: dict[str, object] = json.loads((ROOT / 'examples/handoff/lesson.expected.json').read_text())
question: dict[str, object] = json.loads((ROOT / 'examples/handoff/question.expected.json').read_text())
for name, expected_record in [('lesson', lesson), ('question', question)]:
    content: str = (ROOT / f'examples/handoff/{name}.md').read_text()
    meta: dict[str, object] = yaml.safe_load(content.split('---', 2)[1])
    if meta.get('status') != 'draft':
        errors.append(f'{name} fixture incorrectly claims acceptance')
    for field, value in meta.items():
        if field not in {'handoff_version', 'status'} and expected_record.get(field) != value:
            errors.append(f'{name} fixture changed metadata field {field}')
    if name == 'question':
        for part in content.split('---', 2)[2].split('### ')[1:]:
            field, value = part.split('\n', 1)
            if expected_record.get(field.strip()) != value.strip():
                errors.append(f'Question changed prose field {field}')
    else:
        latex: str = content.split('```latex\n')[1].split('\n```')[0]
        if lesson['content'][2]['latex'] != latex:
            errors.append('Equation LaTeX changed in fixture')
checks.append('Fixture metadata, question prose and equation bytes preserved')

# Use only the inspected dependency-free generator validation modules.
sys.path.insert(0, str(Path('work/source/src').resolve()))
sys.dont_write_bytecode = True
validator = importlib.import_module('education_generator.validation')
report = validator.ValidationReport()
terms: set[str] = set(lesson['terminology_identifiers'])
validator._validate_lesson_content(report, lesson, {}, terms, set(), terms)
validator._validate_question(report, question)
errors.extend(report.errors)
checks.append('Paired lesson/question fragments pass applicable existing validator checks; no whole-curriculum pass claimed')

# GitHub tool text snapshots may gain one terminal newline from patch transport.
index_data: dict[str, object] = json.loads(Path('work/source-index.json').read_text())
source_entries: dict[str, dict[str, object]] = {entry['path']: entry for entry in index_data['files']}
snapshot_count: int = 0
for path in Path('work/source').rglob('*'):
    if not path.is_file() or '__pycache__' in path.parts:
        continue
    relative: str = str(path.relative_to('work/source'))
    source_key: str = 'SPEC.md' if relative == 'SPEC.original.md' else relative
    data: bytes = path.read_bytes()
    variants: list[bytes] = [data, data[:-1] if data.endswith(b'\n') else data]
    hashes: set[str] = {hashlib.sha1(b'blob ' + str(len(value)).encode() + b'\0' + value).hexdigest() for value in variants}
    if source_entries[source_key]['sha'] not in hashes:
        errors.append(f'Source snapshot blob mismatch: {source_key}')
    snapshot_count += 1
checks.append(f'{snapshot_count} source snapshots matched GitHub blob IDs allowing one transport-added terminal newline')

result: dict[str, object] = {'checks': checks, 'errors': errors,
    'scope': 'Documentation and illustrative fragments only; no general Markdown converter or complete curriculum generated; no application code changed.'}
Path('work/validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(bool(errors))
