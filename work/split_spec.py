"""Split retained requirements into task-scoped specification files.

TODO: AI-written by Codex; review and replace before adopting as project tooling.
This is a reproducibility utility for the documentation delivery, not application code.
"""

from pathlib import Path
import re
import json

SOURCE: Path = Path('work/source/SPEC.original.md')
DESTINATION: Path = Path('deliverable')
text: str = SOURCE.read_text(encoding='utf-8')
pattern: re.Pattern[str] = re.compile(r'(?m)^#{1,2} (\d+(?:\.\d+)?)\.?(?: )([^\n]+)')
# Only original top-level sections and the separately headed 40.1 are split.
matches: list[re.Match[str]] = [m for m in pattern.finditer(text) if '.' not in m[1] or m[1] == '40.1']
sections: dict[str, str] = {}
titles: dict[str, str] = {}
for index, match in enumerate(matches):
    end: int = matches[index + 1].start() if index + 1 < len(matches) else len(text)
    sections[match[1]] = text[match.start():end].strip() + '\n'
    titles[match[1]] = match[2]

assignments: dict[str, list[str]] = {
    'spec/common/pedagogy.md': ['5', '41'],
    'spec/common/terminology.md': ['4', '22'],
    'spec/common/citations.md': ['15', '16', '36'],
    'spec/common/source_handling.md': ['7', '44'],
    'spec/common/lifecycle.md': ['1', '3', '6', '8', '31', '32', '33', '34', '35', '45'],
    'spec/authoring/curriculum_structure.md': ['9', '10', '11', '14', '17'],
    'spec/authoring/lesson_content.md': ['12', '13', '40.1'],
    'spec/authoring/assessments.md': ['20', '21'],
    'spec/authoring/review.md': ['18', '19'],
    'spec/serialization/project_structure.md': ['23', '24', '37', '38'],
    'spec/serialization/validation.md': ['39', '46'],
    'spec/runtime/SPEC.md': ['25', '26', '27', '28', '29', '30', '40', '42', '43'],
}
for relative_path, numbers in assignments.items():
    path: Path = DESTINATION / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    heading: str = relative_path.rsplit('/', 1)[-1].replace('.md', '').replace('_', ' ').title()
    intro: str = ('# ' + heading + '\n\n'
        'Normative retained requirements. Original section numbers are stable migration anchors, '
        'not a required reading order. The stage ownership and explicit amendments in the '
        'root SPEC.md and common/handoff.md govern the two-stage workflow.\n\n')
    content: str = '\n'.join(sections[number] for number in numbers)
    content = content.replace('These passes do not require ten separate model invocations',
                              'These twelve passes do not require twelve separate model invocations')
    path.write_text(intro + content, encoding='utf-8')

rows: list[str] = ['# Original requirement migration map', '',
    'All original numbered sections are accounted for. Section 2 navigation is replaced by the root routing table. '
    'Other sections retain their text except the twelve-pass wording correction; amendments are explicit in the new root contract.', '',
    '| Original section | Topic | New owner |', '| --- | --- | --- |']
for number in sections:
    owner: str = next((path for path, numbers in assignments.items() if number in numbers), 'SPEC.md')
    rows.append(f'| {number} | {titles[number].replace("|", "/")} | [{owner}](../../{owner}) |')
(DESTINATION / 'docs/agent/REQUIREMENT_MAP.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
(Path('work') / 'section-map.json').write_text(json.dumps(assignments, indent=2) + '\n', encoding='utf-8')
