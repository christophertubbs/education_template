---
handoff_version: "1.0"
status: "draft"
---
# Knowledge and prerequisite design

This is a design checkpoint, not complete teaching coverage. Relationships point
from dependent to prerequisite. Topic numbers refer to the ordered 26 groups in
`topmodel.project.json`; the configured detailed obligations remain authoritative.
Importance is assigned before question generation. Categories below group
teaching domains; no category is an assertion of completion.

Configured entry knowledge: professional software development using Python, C,
or C++, and secondary-school algebra/arithmetic. File paths, ordinary loops,
variables, functions and tests can therefore be used in the first source-evidence
lesson. No hydrology, calculus, numerical methods, BMI, or Fortran is assumed.

## Record: tm-evidence

```yaml
{
  "identifier": "tm-evidence",
  "title": "Read a claim and identify its evidence",
  "importance": "foundational",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    1,
    22,
    24
  ]
}
```

### description

Distinguish static source facts, test assertions, executed observations and scientific claims; preserve commit-specific locators.

### prerequisite_closure

Closes against the configured professional-development baseline for the evidence lesson; specialized scientific vocabulary must be introduced later.

## Record: tm-units

```yaml
{
  "identifier": "tm-units",
  "title": "Quantities, units and water accounting",
  "importance": "foundational",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    2
  ]
}
```

### description

Convert amounts and rates, track signs for deficits, weight by area and close a water balance.

### prerequisite_closure

Requires `tm-evidence`. Detailed recursive closure remains under review.

## Record: tm-functions

```yaml
{
  "identifier": "tm-functions",
  "title": "Functions, logarithms and weighted distributions",
  "importance": "foundational",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    3
  ]
}
```

### description

Invert positive exponential relations, interpret slope and interpolate weighted index intervals.

### prerequisite_closure

Requires `tm-units`. Detailed recursive closure remains under review.

## Record: tm-calculus

```yaml
{
  "identifier": "tm-calculus",
  "title": "Rates, accumulation and change laws",
  "importance": "foundational",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    4
  ]
}
```

### description

Introduce local rates and finite sums before derivatives, integrals and storage-outflow derivations.

### prerequisite_closure

Requires `tm-functions`. Detailed recursive closure remains under review.

## Record: tm-numerics

```yaml
{
  "identifier": "tm-numerics",
  "title": "Finite steps and numerical failure",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    5
  ]
}
```

### description

Separate rounding from discretization, trace explicit updates, and test solver residuals and convergence.

### prerequisite_closure

Requires `tm-calculus`. Detailed recursive closure remains under review.

## Record: tm-soil

```yaml
{
  "identifier": "tm-soil",
  "title": "Water, vegetation and soil",
  "importance": "foundational",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    6
  ]
}
```

### description

Explain soil water stores, deficits, flow drivers, conductivity and transmissivity from ordinary physical examples.

### prerequisite_closure

Requires `tm-units`. Detailed recursive closure remains under review.

## Record: tm-catchments

```yaml
{
  "identifier": "tm-catchments",
  "title": "Catchments and runoff pathways",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    7
  ]
}
```

### description

Distinguish infiltration excess, saturation excess and return flow; link wetness, connectivity and outlet response.

### prerequisite_closure

Requires `tm-soil`. Detailed recursive closure remains under review.

## Record: tm-terrain-index

```yaml
{
  "identifier": "tm-terrain-index",
  "title": "Terrain classes and topographic index",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    8
  ]
}
```

### description

Derive area per contour width, index conventions, weighted reference and information lost by grouping.

### prerequisite_closure

Requires `tm-functions`, `tm-catchments`. Detailed recursive closure remains under review.

## Record: tm-deficit-flow

```yaml
{
  "identifier": "tm-deficit-flow",
  "title": "TOPMODEL deficit and baseflow relations",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    9
  ]
}
```

### description

Derive and invert local-deficit and exponential baseflow relations, with assumptions and positive-input checks.

### prerequisite_closure

Requires `tm-terrain-index`, `tm-calculus`. Detailed recursive closure remains under review.

## Record: tm-timestep

```yaml
{
  "identifier": "tm-timestep",
  "title": "Root-zone and unsaturated timestep",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    10
  ]
}
```

### description

Trace rain, storage transfer, excess, drainage, evaporation and mean-deficit changes in source order.

### prerequisite_closure

Requires `tm-deficit-flow`, `tm-numerics`. Detailed recursive closure remains under review.

## Record: tm-infiltration

```yaml
{
  "identifier": "tm-infiltration",
  "title": "Optional infiltration solver and storm memory",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    11
  ]
}
```

### description

Explain wetting-front quantities, ponding transitions, solver branches and persistent state; diagnose port defects.

### prerequisite_closure

Requires `tm-soil`, `tm-numerics`, `tm-timestep`. Detailed recursive closure remains under review.

## Record: tm-routing

```yaml
{
  "identifier": "tm-routing",
  "title": "Runoff generation versus delayed arrival",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    12
  ]
}
```

### description

Build and apply delayed weights, preserve pending water and distinguish fixed from flow-dependent routing.

### prerequisite_closure

Requires `tm-functions`, `tm-timestep`. Detailed recursive closure remains under review.

## Record: tm-preparation

```yaml
{
  "identifier": "tm-preparation",
  "title": "Terrain and parameter preparation",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    13
  ]
}
```

### description

Audit raster geometry, masks, area weights, thresholds and generated file conventions with bounded samples.

### prerequisite_closure

Requires `tm-terrain-index`, `tm-routing`. Detailed recursive closure remains under review.

## Record: tm-evaluation

```yaml
{
  "identifier": "tm-evaluation",
  "title": "Observations, calibration and scientific testing",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    14
  ]
}
```

### description

Align observed/model quantities, explain scores and distinguish fit, identifiability and independent evaluation.

### prerequisite_closure

Requires `tm-functions`, `tm-timestep`. Detailed recursive closure remains under review.

## Record: tm-validity

```yaml
{
  "identifier": "tm-validity",
  "title": "Model validity and alternatives",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    15
  ]
}
```

### description

Trace violated assumptions to expected error mechanisms and compare alternative formulations.

### prerequisite_closure

Requires `tm-soil`, `tm-catchments`, `tm-deficit-flow`, `tm-evaluation`. Detailed recursive closure remains under review.

## Record: tm-fortran

```yaml
{
  "identifier": "tm-fortran",
  "title": "Read fixed-form legacy Fortran",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    16
  ]
}
```

### description

Recover types, loops, shared storage, array bounds and call-side effects without assuming modern language behavior.

### prerequisite_closure

Requires `tm-evidence`. Detailed recursive closure remains under review.

## Record: tm-translation

```yaml
{
  "identifier": "tm-translation",
  "title": "Preserve Fortran behavior in C++",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    17
  ]
}
```

### description

Preserve state lifetime, precision, argument mutation, indexing and control flow; isolate deliberate corrections.

### prerequisite_closure

Requires `tm-fortran`, `tm-numerics`, `tm-infiltration`. Detailed recursive closure remains under review.

## Record: tm-ownership

```yaml
{
  "identifier": "tm-ownership",
  "title": "Architecture and execution ownership",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    18
  ]
}
```

### description

Trace registration, initialization, host control, configuration, allocation and cleanup; distinguish run modes.

### prerequisite_closure

Requires `tm-evidence`. Detailed recursive closure remains under review.

## Record: tm-bmi

```yaml
{
  "identifier": "tm-bmi",
  "title": "BMI values, units and clocks",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    19
  ]
}
```

### description

Audit exchange names, pointer lifetimes, scalar indices, metadata, parameter side effects and clock requests.

### prerequisite_closure

Requires `tm-ownership`, `tm-units`, `tm-timestep`. Detailed recursive closure remains under review.

## Record: tm-restart

```yaml
{
  "identifier": "tm-restart",
  "title": "Checkpoints and restart",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    20
  ]
}
```

### description

Audit archive field order, dimensional compatibility, ownership, hotstart/resume clocks and failure state.

### prerequisite_closure

Requires `tm-bmi`, `tm-routing`. Detailed recursive closure remains under review.

## Record: tm-build

```yaml
{
  "identifier": "tm-build",
  "title": "Build and operational behavior",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    21
  ]
}
```

### description

Trace mixed-language targets, Boost linkage, sanitizer scope, working-directory requirements and distribution.

### prerequisite_closure

Requires `tm-ownership`. Detailed recursive closure remains under review.

## Record: tm-paper

```yaml
{
  "identifier": "tm-paper",
  "title": "Original-paper reading and comparison",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    23
  ]
}
```

### description

Verify original notation, equations, experiment conditions, response surfaces and later-code differences.

### prerequisite_closure

Requires `tm-deficit-flow`, `tm-routing`, `tm-evaluation`. Detailed recursive closure remains under review.

## Record: tm-crosswalk

```yaml
{
  "identifier": "tm-crosswalk",
  "title": "Persistent symbol crosswalk",
  "importance": "major",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    25
  ]
}
```

### description

Map every configured historical symbol to current meaning, role, units, lifetime and source assignment.

### prerequisite_closure

Requires `tm-soil`, `tm-terrain-index`, `tm-timestep`, `tm-routing`. Detailed recursive closure remains under review.

## Record: tm-contribution

```yaml
{
  "identifier": "tm-contribution",
  "title": "Contribution and integrated verification",
  "importance": "high-risk",
  "category": "curriculum-domain",
  "configured_topic_groups": [
    22,
    24,
    26
  ]
}
```

### description

Design a bounded change and distinguish implementation, numerical, data and structural explanations with meaningful checks.

### prerequisite_closure

Requires `tm-translation`, `tm-restart`, `tm-build`, `tm-validity`, `tm-paper`, `tm-crosswalk`. Detailed recursive closure remains under review.

## Record: tm-prerequisite-relationships

```yaml
{
  "relationships": [
    {
      "source": "tm-units",
      "target": "tm-evidence",
      "type": "prerequisite"
    },
    {
      "source": "tm-functions",
      "target": "tm-units",
      "type": "prerequisite"
    },
    {
      "source": "tm-calculus",
      "target": "tm-functions",
      "type": "prerequisite"
    },
    {
      "source": "tm-numerics",
      "target": "tm-calculus",
      "type": "prerequisite"
    },
    {
      "source": "tm-soil",
      "target": "tm-units",
      "type": "prerequisite"
    },
    {
      "source": "tm-catchments",
      "target": "tm-soil",
      "type": "prerequisite"
    },
    {
      "source": "tm-terrain-index",
      "target": "tm-functions",
      "type": "prerequisite"
    },
    {
      "source": "tm-terrain-index",
      "target": "tm-catchments",
      "type": "prerequisite"
    },
    {
      "source": "tm-deficit-flow",
      "target": "tm-terrain-index",
      "type": "prerequisite"
    },
    {
      "source": "tm-deficit-flow",
      "target": "tm-calculus",
      "type": "prerequisite"
    },
    {
      "source": "tm-timestep",
      "target": "tm-deficit-flow",
      "type": "prerequisite"
    },
    {
      "source": "tm-timestep",
      "target": "tm-numerics",
      "type": "prerequisite"
    },
    {
      "source": "tm-infiltration",
      "target": "tm-soil",
      "type": "prerequisite"
    },
    {
      "source": "tm-infiltration",
      "target": "tm-numerics",
      "type": "prerequisite"
    },
    {
      "source": "tm-infiltration",
      "target": "tm-timestep",
      "type": "prerequisite"
    },
    {
      "source": "tm-routing",
      "target": "tm-functions",
      "type": "prerequisite"
    },
    {
      "source": "tm-routing",
      "target": "tm-timestep",
      "type": "prerequisite"
    },
    {
      "source": "tm-preparation",
      "target": "tm-terrain-index",
      "type": "prerequisite"
    },
    {
      "source": "tm-preparation",
      "target": "tm-routing",
      "type": "prerequisite"
    },
    {
      "source": "tm-evaluation",
      "target": "tm-functions",
      "type": "prerequisite"
    },
    {
      "source": "tm-evaluation",
      "target": "tm-timestep",
      "type": "prerequisite"
    },
    {
      "source": "tm-validity",
      "target": "tm-soil",
      "type": "prerequisite"
    },
    {
      "source": "tm-validity",
      "target": "tm-catchments",
      "type": "prerequisite"
    },
    {
      "source": "tm-validity",
      "target": "tm-deficit-flow",
      "type": "prerequisite"
    },
    {
      "source": "tm-validity",
      "target": "tm-evaluation",
      "type": "prerequisite"
    },
    {
      "source": "tm-fortran",
      "target": "tm-evidence",
      "type": "prerequisite"
    },
    {
      "source": "tm-translation",
      "target": "tm-fortran",
      "type": "prerequisite"
    },
    {
      "source": "tm-translation",
      "target": "tm-numerics",
      "type": "prerequisite"
    },
    {
      "source": "tm-translation",
      "target": "tm-infiltration",
      "type": "prerequisite"
    },
    {
      "source": "tm-ownership",
      "target": "tm-evidence",
      "type": "prerequisite"
    },
    {
      "source": "tm-bmi",
      "target": "tm-ownership",
      "type": "prerequisite"
    },
    {
      "source": "tm-bmi",
      "target": "tm-units",
      "type": "prerequisite"
    },
    {
      "source": "tm-bmi",
      "target": "tm-timestep",
      "type": "prerequisite"
    },
    {
      "source": "tm-restart",
      "target": "tm-bmi",
      "type": "prerequisite"
    },
    {
      "source": "tm-restart",
      "target": "tm-routing",
      "type": "prerequisite"
    },
    {
      "source": "tm-build",
      "target": "tm-ownership",
      "type": "prerequisite"
    },
    {
      "source": "tm-paper",
      "target": "tm-deficit-flow",
      "type": "prerequisite"
    },
    {
      "source": "tm-paper",
      "target": "tm-routing",
      "type": "prerequisite"
    },
    {
      "source": "tm-paper",
      "target": "tm-evaluation",
      "type": "prerequisite"
    },
    {
      "source": "tm-crosswalk",
      "target": "tm-soil",
      "type": "prerequisite"
    },
    {
      "source": "tm-crosswalk",
      "target": "tm-terrain-index",
      "type": "prerequisite"
    },
    {
      "source": "tm-crosswalk",
      "target": "tm-timestep",
      "type": "prerequisite"
    },
    {
      "source": "tm-crosswalk",
      "target": "tm-routing",
      "type": "prerequisite"
    },
    {
      "source": "tm-contribution",
      "target": "tm-translation",
      "type": "prerequisite"
    },
    {
      "source": "tm-contribution",
      "target": "tm-restart",
      "type": "prerequisite"
    },
    {
      "source": "tm-contribution",
      "target": "tm-build",
      "type": "prerequisite"
    },
    {
      "source": "tm-contribution",
      "target": "tm-validity",
      "type": "prerequisite"
    },
    {
      "source": "tm-contribution",
      "target": "tm-paper",
      "type": "prerequisite"
    },
    {
      "source": "tm-contribution",
      "target": "tm-crosswalk",
      "type": "prerequisite"
    }
  ]
}
```

### review

The graph is an initial acyclic domain ordering. Shared topic mappings are intentional:
verification and defect cases recur in several contexts. Terminology-level recursive
closure and full topic-to-block coverage are not yet certified. All 26 configured
groups are represented, including the paper requirement; none was dropped because
source retrieval failed.

