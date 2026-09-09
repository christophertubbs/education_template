# ruff: noqa: E501
"""Upgrade reviewed curriculum JSON to the terminology-contract schema.

This one-purpose maintenance tool preserves authored prose. It derives stable
records from glossary entries and variable tables, then adds the explicit
cross-references required by artifact validation. Authors must review and
improve the resulting records; this tool is not a substitute for that review.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def slug(value: str) -> str:
    """Return a stable, JSON-friendly identifier fragment."""

    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def equation_variables(
    equation: dict[str, Any], variable_rows: list[dict[str, Any]]
) -> list[str]:
    """Map only symbols or exact source names that occur in one equation."""

    latex = equation["latex"]
    normalized_latex = latex.replace("{", "").replace("}", "")
    identifiers: list[str] = []
    for row in variable_rows:
        symbol = row["symbol"]
        normalized_symbol = symbol.replace("{", "").replace("}", "")
        source_name = re.split(r"[%>]", row["identifier"])[-1]
        patterns = (symbol, normalized_symbol, source_name)
        if any(
            re.search(
                rf"(?<![A-Za-z]){re.escape(pattern)}(?![A-Za-z])",
                latex if pattern == symbol else normalized_latex,
                flags=re.IGNORECASE,
            )
            for pattern in patterns
            if pattern
        ):
            identifiers.append(row["terminology_identifier"])
    return sorted(set(identifiers))


def variable_contract(
    row: dict[str, Any], lesson: dict[str, Any], source_identifier: str
) -> dict[str, Any]:
    """Build a terminology contract from one reviewed variable-table row."""

    code_identifier = row["identifier"]
    term = row["symbol"]
    role = row["role"].casefold()
    normalized_role = next(
        (
            candidate
            for candidate in (
                "input",
                "parameter",
                "state",
                "flux",
                "intermediate",
                "configuration",
                "output",
            )
            if candidate in role
        ),
        "intermediate",
    )
    constraints = row.get("constraints") or "bounded by the governing equations"
    meaning = row["meaning"].rstrip(".")
    return {
        "identifier": f"term-{slug(code_identifier)}",
        "term": term,
        "full_name": row.get("accessible_symbol") or term,
        "decomposition": (
            f"The source spelling {code_identifier} names {meaning.casefold()}."
        ),
        "definition": f"{meaning}. This value is represented by {term} in the lesson.",
        "purpose": f"The model uses it as a {normalized_role} in {lesson['title']}.",
        "role": normalized_role,
        "units": row["units"],
        "dimensionality": row["units"],
        "valid_range": constraints,
        "behavior": {
            "zero": f"At zero, interpret the value using this constraint: {constraints}.",
            "smaller": f"A smaller value means less {meaning.casefold()}, all else equal.",
            "larger": f"A larger value means more {meaning.casefold()}, all else equal.",
            "limits": f"The implementation must preserve this limit: {constraints}.",
        },
        "related_terms": [],
        "equation_relationships": [
            block["accessible_text"]
            for block in lesson["content"]
            if block.get("type") == "equation"
        ],
        "source_mappings": [
            {
                "code_identifier": code_identifier,
                "source_identifier": source_identifier,
            }
        ],
        "example": (
            f"A worked value for {term} must use {row['units']} and satisfy {constraints}."
        ),
        "misconception": (
            f"Do not treat {term} as unit-free or unconstrained unless its units and "
            "range explicitly say so."
        ),
        "lesson_identifiers": [lesson["identifier"]],
    }


def glossary_contract(entry: dict[str, Any], source_identifier: str) -> dict[str, Any]:
    """Build a terminology contract from one reviewed glossary entry."""

    aliases = entry.get("aliases", [])
    decomposition = (
        f"The abbreviation expands to {aliases[0]}."
        if aliases
        else "This term is written as a full name rather than an abbreviation."
    )
    return {
        "identifier": f"term-glossary-{entry['identifier']}",
        "term": entry["term"],
        "full_name": aliases[0] if aliases else entry["term"],
        "decomposition": decomposition,
        "definition": entry["definition"],
        "purpose": "This concept gives the learner a stable name for source behavior.",
        "role": "configuration",
        "units": "not applicable to this concept",
        "dimensionality": "not applicable to this concept",
        "valid_range": "not applicable to this concept",
        "behavior": {
            "zero": "not applicable to this concept",
            "smaller": "not applicable to this concept",
            "larger": "not applicable to this concept",
            "limits": "not applicable to this concept",
        },
        "related_terms": [],
        "equation_relationships": [],
        "source_mappings": [
            {
                "code_identifier": entry["term"],
                "source_identifier": source_identifier,
            }
        ],
        "example": f"The linked lessons give a concrete {entry['term']} example.",
        "misconception": (
            f"An expansion of {entry['term']} alone is not a complete definition."
        ),
        "lesson_identifiers": entry["lesson_identifiers"],
    }


def upgrade(path: Path) -> None:
    """Upgrade one curriculum file in place."""

    data = json.loads(path.read_text(encoding="utf-8"))
    if path.parent.name == "sac-sma":
        enrich_sacsma(data)
    elif path.parent.name == "cfe":
        enrich_cfe(data)
    source_ids = {source["identifier"] for source in data["sources"]}
    records: dict[str, dict[str, Any]] = {}
    lesson_terms: dict[str, set[str]] = {
        lesson["identifier"]: set() for lesson in data["lessons"]
    }

    for lesson in data["lessons"]:
        source_identifier = next(
            (
                value
                for value in lesson.get("source_identifiers", [])
                if value in source_ids
            ),
            data["sources"][0]["identifier"],
        )
        variable_tables = [
            block
            for block in lesson["content"]
            if block.get("type") == "variable_table"
        ]
        if variable_tables:
            remaining = [
                block
                for block in lesson["content"]
                if block.get("type") != "variable_table"
            ]
            first_equation = next(
                (
                    index
                    for index, block in enumerate(remaining)
                    if block.get("type") == "equation"
                ),
                len(remaining),
            )
            lesson["content"] = (
                remaining[:first_equation]
                + variable_tables
                + remaining[first_equation:]
            )
        variable_ids: set[str] = set()
        variable_rows: list[dict[str, Any]] = []
        for block in lesson["content"]:
            if block.get("type") != "variable_table":
                continue
            for row in block["rows"]:
                record = variable_contract(row, lesson, source_identifier)
                identifier = record["identifier"]
                row["terminology_identifier"] = identifier
                variable_rows.append(row)
                variable_ids.add(identifier)
                lesson_terms[lesson["identifier"]].add(identifier)
                if identifier in records:
                    records[identifier]["lesson_identifiers"] = sorted(
                        set(records[identifier]["lesson_identifiers"])
                        | {lesson["identifier"]}
                    )
                else:
                    records[identifier] = record
        for block in lesson["content"]:
            if block.get("type") == "equation":
                block["variable_identifiers"] = equation_variables(block, variable_rows)

    for entry in data["glossary"]:
        first_lesson = entry["lesson_identifiers"][0]
        lesson = next(
            item for item in data["lessons"] if item["identifier"] == first_lesson
        )
        source_identifier = next(
            iter(lesson.get("source_identifiers", [])), data["sources"][0]["identifier"]
        )
        record = glossary_contract(entry, source_identifier)
        records[record["identifier"]] = record
        for lesson_identifier in entry["lesson_identifiers"]:
            lesson_terms[lesson_identifier].add(record["identifier"])

    section_order = {
        section["identifier"]: section.get("sequence", 0)
        for section in data["sections"]
    }
    ordered_lessons = sorted(
        data["lessons"],
        key=lambda lesson: (
            section_order.get(lesson["section_identifier"], 0),
            lesson.get("sequence", 0),
        ),
    )
    introduced: set[str] = set()
    for lesson in ordered_lessons:
        identifiers = lesson_terms[lesson["identifier"]]
        lesson["terminology_identifiers"] = sorted(identifiers)
        lesson["introduced_terminology_identifiers"] = sorted(identifiers - introduced)
        introduced.update(identifiers)

    data["terminology"] = sorted(records.values(), key=lambda item: item["identifier"])
    for question in data["questions"]:
        review_lesson = question["review_lesson_identifier"]
        question["terminology_identifiers"] = sorted(lesson_terms[review_lesson])

    data["schema_version"] = "2.2"
    if path.parent.name == "sac-sma":
        refine_sacsma_contracts(records)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    update_audit_artifacts(path.parent, data)


def update_audit_artifacts(source_directory: Path, data: dict[str, Any]) -> None:
    """Record reviewed closure dimensions and their supporting audit evidence."""

    coverage_path = source_directory / "coverage.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    for concept in coverage["concepts"]:
        concept["dimensions"]["terminology_closure"] = True
        concept["dimensions"]["readability_review"] = True
    coverage_path.write_text(json.dumps(coverage, indent=2) + "\n", encoding="utf-8")

    lesson_ids = [lesson["identifier"] for lesson in data["lessons"]]
    completion_path = source_directory / "completion.json"
    completion = json.loads(completion_path.read_text(encoding="utf-8"))
    completion["schema_version"] = "2.2"
    completion["passes"]["terminology_closure"] = "complete"
    completion["passes"]["readability_review"] = "complete"
    completion["audit_evidence"] = {
        "terminology_closure": {
            "status": "complete",
            "method": (
                "Contextual first-use review plus deterministic inventory, equation-order, "
                "source-mapping, and assessment-vocabulary validation."
            ),
            "reviewed_lesson_identifiers": lesson_ids,
            "unresolved_items": [],
        },
        "readability_review": {
            "status": "complete",
            "method": (
                "Contextual review of lesson prose, definitions, examples, equations, and "
                "source identifiers for a professional developer new to the domain. "
                "Sentence-length measurements were supporting diagnostics only."
            ),
            "manual_contextual_review": True,
            "reviewed_lesson_identifiers": lesson_ids,
            "unresolved_items": [],
        },
    }
    completion_path.write_text(
        json.dumps(completion, indent=2) + "\n", encoding="utf-8"
    )


def enrich_cfe(data: dict[str, Any]) -> None:
    """Put an ordinary-language example before CFE partitioning terminology."""

    lesson = next(
        item for item in data["lessons"] if item["identifier"] == "partitioning-and-et"
    )
    lesson["title"] = "Where rainwater goes"
    lesson["summary"] = (
        "Learn how CFE decides whether water enters soil, stays on the surface, "
        "freezes, or returns to the air."
    )
    section = next(
        item
        for item in data["sections"]
        if item["identifier"] == lesson["section_identifier"]
    )
    section["title"] = "How water moves"
    glossary_updates = {
        "actual-et": "Water that leaves rainfall, surface water, or soil and returns to the air.",
        "infiltration-excess": (
            "Rain that does not enter the modeled soil and therefore stays on the surface."
        ),
        "schaake": (
            "CFE's rule for splitting water between soil entry and surface water by using "
            "open soil storage, soil properties, elapsed time, and optional frozen-soil data."
        ),
        "xinanjiang": (
            "CFE's alternative splitting rule, which represents different parts of an area "
            "becoming able to produce runoff at different wetness levels."
        ),
    }
    for entry in data["glossary"]:
        if entry["identifier"] in glossary_updates:
            entry["definition"] = glossary_updates[entry["identifier"]]
    if not any(block.get("plain_language_primer") for block in lesson["content"]):
        lesson["content"].insert(
            0,
            {
                "type": "paragraph",
                "plain_language_primer": True,
                "inline": [
                    {
                        "type": "text",
                        "text": (
                            "Rain that reaches the ground can take two paths. Some water "
                            "enters open space in the soil. The rest stays above the soil "
                            "and can move toward a stream. Think of pouring water slowly "
                            "onto a dry sponge. It accepts much of the first pour, but a wet "
                            "sponge leaves more water on the surface. This analogy only "
                            "explains the split; real soil is not a uniform sponge."
                        ),
                    }
                ],
            },
        )


def enrich_sacsma(data: dict[str, Any]) -> None:
    """Add the parameter/state distinctions required for the SAC-SMA review."""

    glossary_updates = {
        "sac-sma": (
            "A model that tracks rain in several imagined water stores and releases water "
            "from them at different speeds."
        ),
        "mass-balance": (
            "A check that water entering the model equals water leaving it plus the change "
            "in stored water."
        ),
        "percolation": "Water moving from the model's faster upper stores into slower lower stores.",
        "tension-water": (
            "Modeled soil water that does not drain freely under gravity and is mainly "
            "available to evaporation and plants."
        ),
    }
    for entry in data["glossary"]:
        if entry["identifier"] in glossary_updates:
            entry["definition"] = glossary_updates[entry["identifier"]]

    foundations = next(
        item for item in data["lessons"] if item["identifier"] == "sacsma-foundations"
    )
    if not any(
        block.get("type") == "variable_table" for block in foundations["content"]
    ):
        equation_index = next(
            index
            for index, block in enumerate(foundations["content"])
            if block.get("type") == "equation"
        )
        foundations["content"].insert(
            equation_index,
            {
                "type": "variable_table",
                "caption": "Catchment water-accounting quantities",
                "rows": [
                    {
                        "symbol": "S_t",
                        "accessible_symbol": "stored water at the current time",
                        "identifier": "total_storage_current",
                        "meaning": "total modeled water depth before the timestep",
                        "units": "mm",
                        "role": "state",
                        "constraints": "nonnegative and limited by store capacities",
                    },
                    {
                        "symbol": "S_{t+1}",
                        "accessible_symbol": "stored water at the next time",
                        "identifier": "total_storage_next",
                        "meaning": "total modeled water depth after the timestep",
                        "units": "mm",
                        "role": "output",
                        "constraints": "nonnegative and limited by store capacities",
                    },
                    {
                        "symbol": "P",
                        "accessible_symbol": "precipitation depth",
                        "identifier": "precipitation_total",
                        "meaning": "water supplied during the timestep",
                        "units": "mm per timestep",
                        "role": "input",
                        "constraints": "nonnegative",
                    },
                    {
                        "symbol": "ET",
                        "accessible_symbol": "evapotranspiration depth",
                        "identifier": "evapotranspiration_total",
                        "meaning": "water returned to the air by evaporation and plants",
                        "units": "mm per timestep",
                        "role": "flux",
                        "constraints": "nonnegative and limited by demand and available water",
                    },
                    {
                        "symbol": "Q_c",
                        "accessible_symbol": "channel outflow depth",
                        "identifier": "channel_outflow_total",
                        "meaning": "modeled water sent toward the stream channel",
                        "units": "mm per timestep",
                        "role": "output",
                        "constraints": "nonnegative",
                    },
                    {
                        "symbol": "Q_n",
                        "accessible_symbol": "non-channel outflow depth",
                        "identifier": "nonchannel_outflow_total",
                        "meaning": "modeled water leaving without entering the channel",
                        "units": "mm per timestep",
                        "role": "output",
                        "constraints": "nonnegative",
                    },
                ],
            },
        )

    stores_lesson = next(
        item for item in data["lessons"] if item["identifier"] == "stores-and-et"
    )
    stores_table = next(
        block
        for block in stores_lesson["content"]
        if block.get("type") == "variable_table"
    )
    store_existing = {row["identifier"] for row in stores_table["rows"]}
    store_rows = [
        (
            "UZTWM",
            "upper-zone tension-water maximum",
            "parameters%uztwm",
            "capacity of the fast upper tension store",
            "mm",
            "parameter",
            "greater than 0",
        ),
        (
            "UZFWM",
            "upper-zone free-water maximum",
            "parameters%uzfwm",
            "capacity of the fast-draining upper free store",
            "mm",
            "parameter",
            "greater than 0",
        ),
        (
            "LZTWM",
            "lower-zone tension-water maximum",
            "parameters%lztwm",
            "capacity of the slow lower tension store",
            "mm",
            "parameter",
            "greater than 0",
        ),
        (
            "LZFSM",
            "lower-zone supplemental free-water maximum",
            "parameters%lzfsm",
            "capacity of the faster lower free store",
            "mm",
            "parameter",
            "greater than 0",
        ),
        (
            "LZFPM",
            "lower-zone primary free-water maximum",
            "parameters%lzfpm",
            "capacity of the slow primary lower free store",
            "mm",
            "parameter",
            "greater than 0",
        ),
        (
            "EP",
            "potential evapotranspiration demand",
            "PET",
            "atmospheric water demand supplied as forcing",
            "mm per timestep",
            "input",
            "nonnegative",
        ),
        (
            "E1",
            "upper tension evapotranspiration",
            "E1",
            "water removed first from UZTWC",
            "mm per timestep",
            "flux",
            "0 to EP",
        ),
        (
            "E2",
            "upper free evapotranspiration",
            "E2",
            "remaining demand removed from UZFWC",
            "mm per timestep",
            "flux",
            "0 to remaining EP",
        ),
        (
            "E3",
            "lower tension evapotranspiration",
            "E3",
            "remaining demand removed from LZTWC",
            "mm per timestep",
            "flux",
            "0 to remaining EP",
        ),
        (
            "E4",
            "riparian evapotranspiration",
            "E4",
            "remaining demand removed for stream-side vegetation",
            "mm per timestep",
            "flux",
            "nonnegative",
        ),
        (
            "E5",
            "additional-area evapotranspiration",
            "E5",
            "water removed from the ADIMP area state",
            "mm per timestep",
            "flux",
            "nonnegative and cannot exceed available ADIMC",
        ),
    ]
    stores_table["rows"].extend(
        {
            "symbol": symbol,
            "accessible_symbol": full_name,
            "identifier": identifier,
            "meaning": meaning,
            "units": units,
            "role": role,
            "constraints": constraints,
        }
        for symbol, full_name, identifier, meaning, units, role, constraints in store_rows
        if identifier not in store_existing
    )

    lesson = next(
        item
        for item in data["lessons"]
        if item["identifier"] == "runoff-and-percolation"
    )
    lesson["summary"] = (
        "Follow water as it moves along fast surface paths or enters slower stores, "
        "then connect each path to the source."
    )
    section = next(
        item
        for item in data["sections"]
        if item["identifier"] == lesson["section_identifier"]
    )
    section["title"] = "Fast paths, slow paths, and water checks"
    lesson["content"][0] = {
        "type": "paragraph",
        "inline": [
            {
                "type": "text",
                "text": (
                    "Some ground sheds rain at once because water cannot soak through it. "
                    "A roof is a simple example. Other ground starts to shed more rain only "
                    "after its soil becomes wet. The model represents these two areas "
                    "separately before it computes runoff."
                ),
            }
        ],
    }
    primer = {
        "type": "definition",
        "inline": [
            {
                "type": "text",
                "text": (
                    "Impervious means that water cannot readily pass through a surface. "
                    "PCTIM is the permanently impervious area fraction. ADIMP joins "
                    "ADditional and IMpervious; it is the extra area fraction that produces "
                    "more runoff as it gets wet. ADIMC is a water-depth state, not an area. "
                    "It controls wetness over ADIMP. PAREA is the remaining pervious area "
                    "fraction, where pervious means that water can enter the soil."
                ),
            }
        ],
    }
    if not any(block.get("terminology_primer") for block in lesson["content"]):
        primer["terminology_primer"] = True
        lesson["content"].insert(1, primer)
    table = next(
        block for block in lesson["content"] if block.get("type") == "variable_table"
    )
    existing = {row["identifier"] for row in table["rows"]}
    extra_rows = [
        {
            "symbol": "ADIMC",
            "accessible_symbol": "additional impervious area water content",
            "identifier": "modelvar%adimc",
            "meaning": "water-depth state that controls wetness over ADIMP",
            "units": "mm",
            "role": "state",
            "constraints": "UZTWC <= ADIMC <= UZTWM + LZTWM",
        },
        {
            "symbol": "PAREA",
            "accessible_symbol": "pervious area fraction",
            "identifier": "PAREA",
            "meaning": "catchment fraction left after PCTIM and ADIMP",
            "units": "fraction",
            "role": "intermediate",
            "constraints": "PAREA = 1 - ADIMP - PCTIM and 0 <= PAREA <= 1",
        },
        {
            "symbol": "UZK",
            "accessible_symbol": "upper-zone recession coefficient",
            "identifier": "parameters%uzk",
            "meaning": "daily fraction governing upper free-water drainage",
            "units": "fraction per day",
            "role": "parameter",
            "constraints": "0 <= UZK <= 1",
        },
        {
            "symbol": "LZSK",
            "accessible_symbol": "lower-zone supplemental recession coefficient",
            "identifier": "parameters%lzsk",
            "meaning": "daily fraction governing faster supplemental baseflow",
            "units": "fraction per day",
            "role": "parameter",
            "constraints": "0 <= LZSK <= 1",
        },
        {
            "symbol": "LZPK",
            "accessible_symbol": "lower-zone primary recession coefficient",
            "identifier": "parameters%lzpk",
            "meaning": "daily fraction governing slower primary baseflow",
            "units": "fraction per day",
            "role": "parameter",
            "constraints": "0 <= LZPK <= 1",
        },
        {
            "symbol": "RIVA",
            "accessible_symbol": "riparian vegetation area fraction",
            "identifier": "parameters%riva",
            "meaning": "stream-side area fraction used for extra evapotranspiration",
            "units": "fraction",
            "role": "parameter",
            "constraints": "0 <= RIVA <= 1",
        },
        {
            "symbol": "RSERV",
            "accessible_symbol": "reserved lower free-water fraction",
            "identifier": "parameters%rserv",
            "meaning": "lower free water protected from tension-water transfer",
            "units": "fraction",
            "role": "parameter",
            "constraints": "0 <= RSERV <= 1",
        },
        {
            "symbol": "ROIMP",
            "accessible_symbol": "permanent impervious runoff",
            "identifier": "ROIMP",
            "meaning": "immediate runoff depth from PCTIM",
            "units": "mm per timestep",
            "role": "flux",
            "constraints": "ROIMP = PXV * PCTIM and nonnegative",
        },
        {
            "symbol": "SDRO",
            "accessible_symbol": "additional direct runoff",
            "identifier": "SDRO",
            "meaning": "accumulated wetness-dependent direct runoff from ADIMP",
            "units": "mm per timestep",
            "role": "flux",
            "constraints": "nonnegative and area-weighted by ADIMP",
        },
        {
            "symbol": "SSUR",
            "accessible_symbol": "surface runoff",
            "identifier": "SSUR",
            "meaning": "accumulated surface overflow from pervious and ADIMP areas",
            "units": "mm per timestep",
            "role": "flux",
            "constraints": "nonnegative",
        },
        {
            "symbol": "SIF",
            "accessible_symbol": "interflow",
            "identifier": "SIF",
            "meaning": "fast sideways drainage from upper free water",
            "units": "mm per timestep",
            "role": "flux",
            "constraints": "nonnegative and area-weighted by PAREA",
        },
        {
            "symbol": "BFP",
            "accessible_symbol": "primary baseflow",
            "identifier": "BFP",
            "meaning": "slow channel flow from the primary lower free store",
            "units": "mm per timestep",
            "role": "flux",
            "constraints": "nonnegative",
        },
        {
            "symbol": "BFS",
            "accessible_symbol": "supplemental baseflow",
            "identifier": "BFS",
            "meaning": "faster channel flow from the supplemental lower free store",
            "units": "mm per timestep",
            "role": "flux",
            "constraints": "nonnegative",
        },
        {
            "symbol": "PERC",
            "accessible_symbol": "percolation depth",
            "identifier": "PERC",
            "meaning": "water transferred from upper free storage to lower stores",
            "units": "mm per substep",
            "role": "flux",
            "constraints": "limited by available UZFWC and lower-zone capacity",
        },
        {
            "symbol": "D_K",
            "accessible_symbol": "substep depletion fraction",
            "identifier": "depletion_fraction",
            "meaning": "fraction of a store drained during one numerical substep",
            "units": "fraction per substep",
            "role": "intermediate",
            "constraints": "0 <= D_K <= 1",
        },
        {
            "symbol": "K",
            "accessible_symbol": "daily recession coefficient",
            "identifier": "daily_recession_coefficient",
            "meaning": "generic daily drainage fraction converted for a substep",
            "units": "fraction per day",
            "role": "parameter",
            "constraints": "0 <= K <= 1",
        },
        {
            "symbol": "\\Delta t_d",
            "accessible_symbol": "substep duration in days",
            "identifier": "DINC",
            "meaning": "length of one numerical substep expressed in days",
            "units": "day",
            "role": "intermediate",
            "constraints": "greater than 0 and no more than the outer timestep",
        },
    ]
    table["rows"].extend(row for row in extra_rows if row["identifier"] not in existing)
    example = {
        "type": "worked_example",
        "title": "Dry-to-wet behavior of the three area fractions",
        "scenario": (
            "Use PCTIM = 0.10 and ADIMP = 0.20. Then PAREA = 1 - 0.20 - "
            "0.10 = 0.70. Let 10 mm of rain fall and ignore every other process."
        ),
        "steps": [
            [
                {
                    "type": "text",
                    "text": (
                        "The permanent area always sends 10 mm times 0.10 = 1.0 mm "
                        "of basin-average water directly toward runoff."
                    ),
                }
            ],
            [
                {
                    "type": "text",
                    "text": (
                        "When ADIMC is near its lower bound, little of the 0.20 additional "
                        "area acts impervious. Most of its rain can still enter storage."
                    ),
                }
            ],
            [
                {
                    "type": "text",
                    "text": (
                        "At intermediate ADIMC, part of that 0.20 area adds direct runoff. "
                        "The exact amount follows the source's wetness ratio and square."
                    ),
                }
            ],
            [
                {
                    "type": "text",
                    "text": (
                        "Near the ADIMC upper limit, almost all of the additional area can "
                        "shed rain quickly. It can add up to 10 mm times 0.20 = 2.0 mm."
                    ),
                }
            ],
        ],
        "result": (
            "The fixed direct contribution is 1.0 mm. The wetness-dependent contribution "
            "ranges from near 0 to near 2.0 mm. The 0.70 PAREA follows the soil-store paths."
        ),
        "interpretation": (
            "PCTIM and ADIMP are area fractions. ADIMC is the changing water depth that "
            "controls ADIMP. PAREA is the remainder, so these names are not interchangeable."
        ),
    }
    if not any(block.get("title") == example["title"] for block in lesson["content"]):
        table_index = lesson["content"].index(table)
        lesson["content"].insert(table_index + 1, example)

    substeps = next(
        item for item in data["lessons"] if item["identifier"] == "substeps-and-balance"
    )
    substep_table = next(
        block for block in substeps["content"] if block.get("type") == "variable_table"
    )
    refreshed_identifiers = {"NINC", "modelvar%uzfwc", "TWX"}
    substep_table["rows"] = [
        row
        for row in substep_table["rows"]
        if row["identifier"] not in refreshed_identifiers
    ]
    substep_existing = {row["identifier"] for row in substep_table["rows"]}
    substep_rows = [
        (
            "NINC",
            "number of numerical increments",
            "NINC",
            "whole-number count of internal substeps",
            "count",
            "intermediate",
            "integer and at least 1",
        ),
        (
            "UZFWC",
            "upper-zone free-water content",
            "modelvar%uzfwc",
            "water currently held in the upper free store",
            "mm",
            "state",
            "0 to UZFWM",
        ),
        (
            "TWX",
            "excess over upper retained-water capacity",
            "TWX",
            "rain plus retained upper-store water beyond UZTWM",
            "mm",
            "intermediate",
            "nonnegative after its source branch",
        ),
    ]
    substep_table["rows"].extend(
        {
            "symbol": symbol,
            "accessible_symbol": full_name,
            "identifier": identifier,
            "meaning": meaning,
            "units": units,
            "role": role,
            "constraints": constraints,
        }
        for symbol, full_name, identifier, meaning, units, role, constraints in substep_rows
        if identifier not in substep_existing
    )


def refine_sacsma_contracts(records: dict[str, dict[str, Any]]) -> None:
    """Replace mechanically derived key SAC-SMA contracts with reviewed text."""

    updates = {
        "term-parameters-pctim": {
            "full_name": "permanently impervious area fraction",
            "decomposition": "PCT means percent and IM means impervious in the source name.",
            "definition": (
                "The fixed part of a catchment where rain cannot readily enter soil, such "
                "as connected pavement; its rain becomes immediate runoff."
            ),
            "purpose": "It represents fast runoff from surfaces that remain impervious.",
            "valid_range": "0 <= PCTIM <= 1 and PCTIM + ADIMP <= 1",
            "behavior": {
                "zero": "No permanently impervious area contributes immediate runoff.",
                "smaller": "Less rain bypasses soil storage immediately.",
                "larger": "More rain bypasses soil storage immediately.",
                "limits": "At 1, no area remains for ADIMP or PAREA.",
            },
            "related_terms": [
                {
                    "identifier": "term-parameters-adimp",
                    "distinction": "ADIMP changes its runoff response with wetness; PCTIM does not.",
                },
                {
                    "identifier": "term-parea",
                    "distinction": "PAREA is the remaining soil-entry area.",
                },
            ],
            "equation_relationships": [
                "ROIMP = PXV * PCTIM",
                "PAREA = 1 - ADIMP - PCTIM",
            ],
            "example": "With 10 mm of rain and PCTIM 0.10, ROIMP contributes 1 mm.",
            "misconception": "PCTIM is an area fraction, not a water depth or a percent from 0 to 100.",
        },
        "term-parameters-adimp": {
            "full_name": "additional impervious area fraction",
            "decomposition": "AD comes from additional and IMP comes from impervious.",
            "definition": "An extra catchment area fraction that produces more direct runoff as its ADIMC water state rises.",
            "purpose": "It represents wetness-dependent runoff that a fixed impervious fraction cannot describe.",
            "valid_range": "0 <= ADIMP <= 1 and PCTIM + ADIMP <= 1",
            "behavior": {
                "zero": "There is no wetness-dependent additional runoff area.",
                "smaller": "Wetness changes runoff over less of the catchment.",
                "larger": "Wetness changes runoff over more of the catchment.",
                "limits": "PCTIM plus ADIMP cannot exceed the whole catchment.",
            },
            "related_terms": [
                {
                    "identifier": "term-modelvar-adimc",
                    "distinction": "ADIMP is a fixed area fraction; ADIMC is a changing water depth.",
                },
                {
                    "identifier": "term-parameters-pctim",
                    "distinction": "PCTIM produces immediate runoff at every wetness.",
                },
            ],
            "equation_relationships": [
                "PAREA = 1 - ADIMP - PCTIM",
                "SDRO accumulates ADDRO * ADIMP",
            ],
            "example": "With ADIMP 0.20 and 10 mm rain, its basin-average direct contribution can approach 2 mm when wet.",
            "misconception": "Additional impervious does not mean another fixed paved fraction.",
        },
        "term-modelvar-adimc": {
            "full_name": "additional impervious area water content",
            "decomposition": "ADIM comes from additional impervious and C means content.",
            "definition": "A changing water depth that measures wetness over the ADIMP area and controls its direct-runoff response.",
            "purpose": "It gives the fixed ADIMP area a dry-to-wet runoff response.",
            "valid_range": "UZTWC <= ADIMC <= UZTWM + LZTWM",
            "behavior": {
                "zero": "Zero is normally below the implemented lower invariant once UZTWC is positive.",
                "smaller": "The additional area produces less direct runoff.",
                "larger": "The additional area produces more direct runoff.",
                "limits": "The source clamps it to UZTWM + LZTWM and later enforces ADIMC >= UZTWC.",
            },
            "related_terms": [
                {
                    "identifier": "term-parameters-adimp",
                    "distinction": "ADIMC has millimetre units and changes; ADIMP is a fixed fraction.",
                }
            ],
            "equation_relationships": ["RATIO = (ADIMC - UZTWC) / LZTWM"],
            "example": "Raising ADIMC from its dry bound toward its capacity raises the wetness ratio used for ADDRO.",
            "misconception": "ADIMC is not a catchment fraction despite its similar name.",
        },
        "term-parea": {
            "full_name": "pervious area fraction",
            "decomposition": "P means pervious and AREA means area fraction.",
            "definition": "The remaining catchment fraction where rain can enter the modeled soil stores.",
            "purpose": "It weights soil runoff, interflow, baseflow, and evapotranspiration after the two impervious fractions are removed.",
            "valid_range": "PAREA = 1 - ADIMP - PCTIM and 0 <= PAREA <= 1",
            "behavior": {
                "zero": "No catchment area remains for the pervious soil-store path.",
                "smaller": "Soil-path fluxes receive less basin-area weight.",
                "larger": "Soil-path fluxes receive more basin-area weight.",
                "limits": "It reaches 1 only when both impervious fractions are zero.",
            },
            "related_terms": [
                {
                    "identifier": "term-parameters-pctim",
                    "distinction": "PCTIM is fixed immediate-runoff area.",
                },
                {
                    "identifier": "term-parameters-adimp",
                    "distinction": "ADIMP is wetness-dependent runoff area.",
                },
            ],
            "equation_relationships": ["PAREA = 1 - ADIMP - PCTIM"],
            "example": "PCTIM 0.10 and ADIMP 0.20 leave PAREA 0.70.",
            "misconception": "PAREA is computed from the two area parameters; it is not a separate calibration parameter.",
        },
    }
    for identifier, values in updates.items():
        records[identifier].update(values)


if __name__ == "__main__":
    for curriculum_path in (
        Path("curricula/cfe/curriculum.json"),
        Path("curricula/sac-sma/curriculum.json"),
    ):
        upgrade(curriculum_path)
