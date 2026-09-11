---
handoff_version: "1.0"
status: "in_review"
---
# Checkpoint validation and review

Date: 2026-09-11. Review method: model-assisted static source reading plus
deterministic locator/arithmetic checks. Checkpoint checks passed; authoring
acceptance has not passed. No human review is claimed.

## Reviewed checkpoint hashes

These identify checked analysis bytes, not an accepted curriculum.

```text
daef0cf6bafb30b269473dc21ff076df7224d9ae220dd0626332007ad2a73b7e  authored/topmodel/source-analysis.md
602f02f486f6ccb95303f49dd4d09e07ea0d2f2e764abf42398cb1cf13e3101f  authored/topmodel/sources.md
bb9c9e43a50cc43a4812b15efb06dcb6327b01d66d7318f7e6d1ed09599b3921  authored/topmodel/source-inventory.md
0133c5b083544e19f98366dc5dc51cc61a63797860ead07663082cddb60a55bd  authored/topmodel/research.md
```

## Reproducible local validation

```bash
PYTHONPATH=src .venv/bin/python - <<'PY'
import json
import math
import re
import subprocess
from pathlib import Path
from education_generator.configuration import load_project_configuration

packet = Path("authored/topmodel")
target = Path("repository/topmodel")
config = load_project_configuration(Path("topmodel.project.json"))
commit = subprocess.check_output(
    ["git", "-C", str(target), "rev-parse", "HEAD"], text=True
).strip()
assert commit == config.revision == "89e4dc529dfdf7f23b7365530973e9f238fb740d"
assert not subprocess.check_output(
    ["git", "-C", str(target), "status", "--porcelain"], text=True
).strip()
records = [
    json.loads(block)
    for block in re.findall(
        r"```yaml\n(.*?)\n```", (packet / "sources.md").read_text(), re.S
    )
]
identifiers = {record["identifier"] for record in records}
assert len(identifiers) == len(records) == 19
for record in records:
    source = (target / record["file_path"]).resolve()
    assert source.is_relative_to(target.resolve())
    assert 1 <= record["start_line"] <= record["end_line"]
    assert record["end_line"] <= len(source.read_text().splitlines())
assert set(re.findall(
    r"citation:([a-z-]+)", (packet / "source-analysis.md").read_text()
)) <= identifiers
for path in packet.glob("*.md"):
    raw = path.read_bytes()
    assert b"\r" not in raw, path
    assert raw.endswith(b"\n"), path
    text = raw.decode("utf-8")
    assert text.startswith("---\n"), path
    assert len(text.split("\n---\n", 1)) == 2, path
    assert all(line == line.rstrip() for line in text.splitlines()), path
qb = .001 * math.exp(-.04 / .02)
assert math.isclose(qb, .0001353352832366127, abs_tol=1e-18)
assert math.isclose(.04 - .0002 + qb, .039935335283236614, abs_tol=1e-17)
for index, expected in zip([4, 5, 6], [.06, .04, .02]):
    assert math.isclose(.04 + .02 * (5 - index), expected, abs_tol=1e-15)
print("PASS: configuration, exact clean target, 19 unique source records,")
print("source bounds, analysis citation closure, Markdown framing, and arithmetic.")
print("NOT RUN: full handoff grammar or substantive acceptance review.")
PY
```

Result: exit 0. Configuration, exact clean target, 19 unique source records,
source bounds, analysis citation closure, Markdown framing and arithmetic passed.
Source-record metadata is JSON within YAML fences, parsed with the data-only
standard-library JSON parser. This is not a full YAML or packet-schema validator.

## Acquisition and failures

`git clone --branch master --single-branch https://github.com/NOAA-OWP/topmodel.git repository/topmodel` completed.
`git ls-remote https://github.com/NOAA-OWP/topmodel.git refs/heads/master` first failed
DNS resolution in the sandbox (exit 128); the approved retry returned the pinned
commit. `git -C repository/topmodel rev-parse HEAD` matched that commit and
`git -C repository/topmodel status --short` was empty.
`git -C repository/topmodel ls-tree -r -l HEAD` produced 94 blobs and 3 gitlinks.

The optional `.venv/bin/python -c 'import yaml; print(yaml.__version__)'` probe
failed: PyYAML is not installed. No dependency was added for this checkpoint.
Full safe-YAML grammar validation remains required at authoring acceptance.
Publisher PDF retrieval returned HTTP 403 (curl exit 22); see `research.md`.

Scoped `git diff --check -- docs/agent/STATUS.md docs/agent/TASKS.md` passed.
The root check previously found the existing user edit `AGENTS.md:83: new blank
line at EOF`; that file was preserved. No target builds, simulations, Django
tests, migrations, package checks or final JSON generation ran.

## Actual review corrections

Verified supplied bug cases against source; located uninitialized `fx` and
compared Fortran `FC`; recorded the routing limitation in the restart test.
Corrected the inventory from 97 ordinary files to 94 files plus 3 gitlinks and
two narrow line locators before hashing. Full scientific, pedagogical, terminology,
assessment and readability reviews remain outstanding in `completion.md`.

## Continuation after the user had no paper copy

User response: no copy or accessible URL. New IAHS and NTUA links returned
HTTP 404. The previous research.md hash is historical and superseded by the
hash below. The scientific acceptance blocker remains; independent writing
now includes the evidence lesson and six-item introductory review.

```text
3f390a109f5d9526770b8bd00eb6850f1a6a82c442b543ba056f605d9e5ee8b4  authored/topmodel/knowledge-map.md
2c604ba5eb800b4c9cf25a7c50bfe2655d45a3b2f30dcc1d5c2612f3546f24c4  authored/topmodel/lessons/tm-evidence.md
e60a74db94840fe5c783ba443f1573f960f8a4fdf2a11375596567ad6020d41a  authored/topmodel/questions/tm-evidence-bank.md
bb68b8003015e9ea8b963e2a55ec390547478fd23fc129578277ada7328e0566  authored/topmodel/assessments/tm-evidence-review.md
6fb1790ad1dc2790a43625f1ecae7b04476c55f20cddef564d2280ceb9d27794  authored/topmodel/research.md
```

```bash
PYTHONPATH=src .venv/bin/python - <<'PY'
import itertools
import json
import re
from pathlib import Path
from education_generator.configuration import load_project_configuration

packet = Path("authored/topmodel")
configuration = load_project_configuration(Path("topmodel.project.json"))
assert configuration.revision == "89e4dc529dfdf7f23b7365530973e9f238fb740d"
def records(path):
    return [json.loads(block) for block in re.findall(
        r"```yaml\n(.*?)\n```", path.read_text(), re.S)]
knowledge = records(packet / "knowledge-map.md")
concepts = knowledge[:-1]
relationships = knowledge[-1]["relationships"]
ids = {concept["identifier"] for concept in concepts}
assert len(ids) == len(concepts) == 24
assert set().union(*(set(c["configured_topic_groups"]) for c in concepts)) == set(range(1, 27))
graph = {identifier: [] for identifier in ids}
for relation in relationships:
    assert relation["source"] in ids and relation["target"] in ids
    assert relation["type"] == "prerequisite"
    graph[relation["source"]].append(relation["target"])
def visit(node, active):
    assert node not in active, "prerequisite cycle"
    for prerequisite in graph[node]:
        visit(prerequisite, active | {node})
for identifier in ids:
    visit(identifier, set())
questions = records(packet / "questions/tm-evidence-bank.md")
assert len(questions) == len({q["identifier"] for q in questions}) == 6
for question in questions:
    assert question["type"] == "single_choice"
    assert len(question["options"]) == 4
    assert sum(option["correct"] for option in question["options"]) == 1
    assert question["concept_identifiers"] == ["tm-evidence"]
    assert question["review_lesson_identifier"] == "tm-evidence-lesson"
    assert question["assessment_identifiers"] == ["tm-evidence-review"]
    assert question["mastery_contract_identifiers"] == ["tm-evidence-contract"]
assert len(list(itertools.combinations(questions, 3))) == 20
source_ids = {r["identifier"] for r in records(packet / "sources.md")}
for path in [packet / "lessons/tm-evidence.md", packet / "questions/tm-evidence-bank.md"]:
    text = path.read_text()
    assert set(re.findall(r"citation:([a-z-]+)", text)) <= source_ids
    assert not re.search(r"\bTODO\b|\bTBD\b", text)
for path in packet.rglob("*.md"):
    raw = path.read_bytes()
    assert raw.startswith(b"---\n") and b"\r" not in raw
    assert all(line == line.rstrip() for line in raw.decode().splitlines()), path
print("PASS: config pin; 24 concepts; all 26 groups; acyclic graph;")
print("6 complete single-choice keys; 20 feasible pop subsets; source closure; framing.")
print("Full grammar, vocabulary closure and course acceptance remain unverified.")
PY
```

Result: exit 0. All 26 configured topic groups represented by 24 domain records;
graph acyclic; six single-choice keys complete; twenty three-item subsets
feasible for the initial pop review; source IDs resolve; framing checks pass.

Model-assisted content review: each item has one defensible correct option
given its supplied premise. Lesson distinguishes code inspection, execution
and scientific adequacy and explicitly teaches the fixture limit. No paper
claims are introduced. The lesson and bank remain in_review: complete course
ordering, terminology/glossary contracts, cross-record grammar and cumulative
assessment coverage are not yet accepted. Do not call this review a full
twelve-pass audit. The remaining course is recorded as incomplete.

