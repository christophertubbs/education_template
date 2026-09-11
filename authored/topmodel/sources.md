---
handoff_version: "1.0"
status: "in_review"
---
# Consulted source records

All repository paths below are relative to `repository/topmodel/` at commit
`89e4dc529dfdf7f23b7365530973e9f238fb740d`, resolved from `master` on 2026-09-11. Line ranges count physical lines, including Fortran CRLF lines. Source review was model-assisted and static. Test source is evidence of assertions present, not passing execution. Locators are verified by `review-checks.md`; semantic teaching review is incomplete.

## Record: src-science

```yaml
{
  "identifier": "src-science",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/topmodel.c",
  "symbol": "topmod",
  "start_line": 110,
  "end_line": 368,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/topmodel.c#L110"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 110–368. Consulted 2026-09-11.

### inspection_scope

Current timestep order, class weights, deficit/storage changes, routing cutoff.

## Record: src-terrain

```yaml
{
  "identifier": "src-terrain",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/topmodel.c",
  "symbol": "tread",
  "start_line": 444,
  "end_line": 555,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/topmodel.c#L444"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 444–555. Consulted 2026-09-11.

### inspection_scope

Terrain normalization, descending bins, endpoint sentinel and weighted mean.

## Record: src-routing

```yaml
{
  "identifier": "src-routing",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/topmodel.c",
  "symbol": "convert_dist_to_histords; calc_time_delay_histogram",
  "start_line": 600,
  "end_line": 734,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/topmodel.c#L600"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 600–734. Consulted 2026-09-11.

### inspection_scope

Travel times, histogram construction, area scaling and failure checks.

## Record: src-initial

```yaml
{
  "identifier": "src-initial",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/topmodel.c",
  "symbol": "init_water_balance",
  "start_line": 817,
  "end_line": 853,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/topmodel.c#L817"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 817–853. Consulted 2026-09-11.

### inspection_scope

Logged input transformation, initial mean deficit and balance.

## Record: src-infiltration

```yaml
{
  "identifier": "src-infiltration",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/topmodel.c",
  "symbol": "expinf",
  "start_line": 1024,
  "end_line": 1161,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/topmodel.c#L1024"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1024–1161. Consulted 2026-09-11.

### inspection_scope

Integer rain intensity and uninitialized variables; iterative branch.

## Record: src-results

```yaml
{
  "identifier": "src-results",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/topmodel.c",
  "symbol": "results",
  "start_line": 1163,
  "end_line": 1217,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/topmodel.c#L1163"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1163–1217. Consulted 2026-09-11.

### inspection_scope

Squared error, absolute error and NSE calculation.

## Record: src-clock

```yaml
{
  "identifier": "src-clock",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/bmi_topmodel.c",
  "symbol": "Get_current_time; Update; Update_until",
  "start_line": 349,
  "end_line": 498,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/bmi_topmodel.c#L349"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/bmi_topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 349–498. Consulted 2026-09-11.

### inspection_scope

Clock representation and fractional advance.

## Record: src-bmi

```yaml
{
  "identifier": "src-bmi",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/bmi_topmodel.c",
  "symbol": "input_var_names; output_var_names; param_var_names",
  "start_line": 1,
  "end_line": 169,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/bmi_topmodel.c#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/bmi_topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–169. Consulted 2026-09-11.

### inspection_scope

Declared exchange counts, types and units.

## Record: src-access

```yaml
{
  "identifier": "src-access",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/bmi_topmodel.c",
  "symbol": "Get_value_ptr; Get_value; Set_value; Set_value_at_indices",
  "start_line": 743,
  "end_line": 1210,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/bmi_topmodel.c#L743"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/bmi_topmodel.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 743–1210. Consulted 2026-09-11.

### inspection_scope

Pointer mappings, copied values, unchecked ordinary indices and parameter resets.

## Record: src-state

```yaml
{
  "identifier": "src-state",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "src/bmi_serialization.cpp",
  "symbol": "TopmodelSerializer::serialize; serialize_topmodel; deserialize_topmodel",
  "start_line": 1,
  "end_line": 201,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/src/bmi_serialization.cpp#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `src/bmi_serialization.cpp`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–201. Consulted 2026-09-11.

### inspection_scope

Archive order, clock mode, reallocation and exception boundary.

## Record: src-model

```yaml
{
  "identifier": "src-model",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "include/topmodel.h",
  "symbol": "TopModel_Struct; topmodel_restore_mode",
  "start_line": 1,
  "end_line": 221,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/include/topmodel.h#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `include/topmodel.h`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–221. Consulted 2026-09-11.

### inspection_scope

State ownership, parameter declarations and clock type.

## Record: src-fortran

```yaml
{
  "identifier": "src-fortran",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "refs/original_code_fortran/TMOD9502.f",
  "symbol": "TOPMOD; EXPINF",
  "start_line": 164,
  "end_line": 686,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/refs/original_code_fortran/TMOD9502.f#L164"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `refs/original_code_fortran/TMOD9502.f`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 164–686. Consulted 2026-09-11.

### inspection_scope

Original loop placement, COMMON data and infiltration expression.

## Record: src-build

```yaml
{
  "identifier": "src-build",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "CMakeLists.txt",
  "symbol": "project; add_library; add_executable",
  "start_line": 1,
  "end_line": 121,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/CMakeLists.txt#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `CMakeLists.txt`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–121. Consulted 2026-09-11.

### inspection_scope

Dependencies and actual build/test targets.

## Record: src-ci

```yaml
{
  "identifier": "src-ci",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": ".github/workflows/build_and_run_unit_test.yml",
  "symbol": "test_unit",
  "start_line": 1,
  "end_line": 63,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/.github/workflows/build_and_run_unit_test.yml#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `.github/workflows/build_and_run_unit_test.yml`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–63. Consulted 2026-09-11.

### inspection_scope

Current CI command sequences.

## Record: src-test-doc

```yaml
{
  "identifier": "src-test-doc",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "test/README.md",
  "symbol": "Comparison",
  "start_line": 1,
  "end_line": 59,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/test/README.md#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `test/README.md`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–59. Consulted 2026-09-11.

### inspection_scope

Historical comparison assertions; not current test execution evidence.

## Record: src-restart-test

```yaml
{
  "identifier": "src-restart-test",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "test/main_integration_test_serialization.c",
  "symbol": "run; compare; main",
  "start_line": 1,
  "end_line": 237,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/test/main_integration_test_serialization.c#L1"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `test/main_integration_test_serialization.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 1–237. Consulted 2026-09-11.

### inspection_scope

Long-run test design and explicit routing coverage limits.

## Record: src-protocol-test

```yaml
{
  "identifier": "src-protocol-test",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "test/main_unit_test_serialization.c",
  "symbol": "test_round_trip; test_rejects_bad_payloads; test_resume_mode_applies_the_clock",
  "start_line": 209,
  "end_line": 393,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/test/main_unit_test_serialization.c#L209"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `test/main_unit_test_serialization.c`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 209–393. Consulted 2026-09-11.

### inspection_scope

Hotstart, rejection and internally selected resume checks.

## Record: src-preprocess

```yaml
{
  "identifier": "src-preprocess",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "params/src/generate_twi_per_basin.py",
  "symbol": "generate_twi_per_basin",
  "start_line": 214,
  "end_line": 361,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/params/src/generate_twi_per_basin.py#L214"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `params/src/generate_twi_per_basin.py`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 214–361. Consulted 2026-09-11.

### inspection_scope

Masking, filtering, histogram choices and file writing.

## Record: src-workflow

```yaml
{
  "identifier": "src-workflow",
  "evidence_kind": "source",
  "certainty": "verified",
  "file_path": "params/src/workflow_hand_twi_giuh.sh",
  "symbol": "terrain workflow",
  "start_line": 80,
  "end_line": 277,
  "url": "https://github.com/NOAA-OWP/topmodel/blob/89e4dc529dfdf7f23b7365530973e9f238fb740d/params/src/workflow_hand_twi_giuh.sh#L80"
}
```

### citation

NOAA-OWP, TOPMODEL BMI, `params/src/workflow_hand_twi_giuh.sh`, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`, lines 80–277. Consulted 2026-09-11.

### inspection_scope

GDAL, TauDEM and Python orchestration; read-only inspection.

