---
handoff_version: "1.0"
status: "in_review"
---
# Source analysis at the accepted master commit

This is authoring evidence, not a substitute for lessons or a completed coverage
matrix. Requested branch: `master`. Resolved and configured commit:
`89e4dc529dfdf7f23b7365530973e9f238fb740d`. No target code was executed or
modified. Review method: model-assisted reading of the cited source ranges and
independent arithmetic reasoning. Numerical consequences are unmeasured unless
explicitly described as a hand calculation.

## Selection and omissions

`git ls-tree -r -l HEAD` inventoried the complete tracked tree before content
inspection. The checkout has 94 tracked ordinary files and three submodule
gitlinks. Large hydrofabric GeoJSON/JSON files are approximately 59–76 MB each;
their values were not ingested. Plot datasets, binary executables, image files,
historical output series, and duplicated forcing series were excluded from full
text reading. The representative `data/inputs.dat` sample was limited to its
header and four rows. All of the small `data/topmod.run`, `data/params.dat`, and
`data/subcat.dat` were read for positional layouts and counts.

Selected science routines, header state definitions, BMI control and exchange
paths, serializer, restart tests, CMake and CI were inspected. Preprocessing
inspection selected the masking, histogram and writing branches plus orchestration
commands; it did not establish end-to-end terrain correctness. No target-local
AGENTS.md was found. No submodule was initialized or executed.

| Submodule | Pinned gitlink | Treatment |
| --- | --- | --- |
| refs/csdms/bmi-builder | fafe5b3704b3313f4b43ddc6cc8dff665705a079 | Inventory only; not used as evidence |
| refs/csdms/bmi-c | d28c46d5b293935e51b8a88a23d0d843ecd32769 | Inventory only; local include/bmi.h supplies current declarations |
| refs/csdms/bmi-example-c | 93e9ef960d2e4d5132fba638e445379a20ac0259 | Inventory only; not used as evidence |

## Execution ownership and state

The driver in `src/main.c` allocates a BMI handle, registers callbacks,
initializes from `./data/topmod.run`, loops over updates, finalizes, and frees
the handle. In standalone mode it additionally reallocates `Q` for the full
forcing history. In coupled mode it does not supply changing rainfall through
setters. Treat it as a demonstration, not a complete coupled forcing provider.
Locator: `src/main.c:17–81`, at the pinned commit.

`TopModel_Struct` owns file pointers, parameter scalars, topology arrays,
hydrological arrays, cumulative diagnostics and the integer step counter.
Registration allocates model data; initialization reads inputs and establishes
state. In framework mode `init_config` sets `nstep=1`, `dt=1`, and puts scalar
forcing in element 1. The outer host owns the series of calls. [State](citation:src-model)
and `src/bmi_topmodel.c:286–343,1363–1452`.

The one-step order is: select/shift the routing queue; read rain and demand;
optionally limit infiltration; traverse terrain classes; calculate local deficit;
fill root-zone deficit; move surplus to unsaturated storage; remove local excess;
drain available unsaturated water; calculate actual evaporation; integrate
surface excess; calculate baseflow from the old mean deficit; update that
deficit; combine generated components; route; accumulate diagnostics.
This order is executable behavior, not a commutative list of processes.
[Timestep](citation:src-science)

## Verified discrepancies and bounded implications

| ID | Observed source and locator | Defensible implication and verification case |
| --- | --- | --- |
| finding-intensity | `topmodel.c:210–211,1024`: double intensity passed to `int rint` | A positive 0.001 value becomes integer zero. Compare argument values, then solver behavior with defined inputs. Do not assign a reliable runoff magnitude to a branch containing undefined reads. |
| finding-dth | `topmodel.c:1040,1046`: local `dth` read with no assignment | The model struct's configured `dth` is not passed to this routine. Fortran `COMMON/PARAM` includes DTH at `TMOD9502.f:574`. Supplying the missing value requires a deliberate interface correction. |
| finding-fx | `topmodel.c:1040,1110–1116`: series uses `fx`, never assigned | Fortran uses `FC` after assigning `FC=F+CD` at `TMOD9502.f:637–645`. Trace the expression and isolate a ponding case. This is an additional defect beyond the configuration's supplied list. |
| finding-storm | `topmodel.c:157–159,211,1024`: storm variables reset per call and `irof` passed by value | In the historical routine initialization precedes `DO 10 IT=1,NSTEP` at `TMOD9502.f:202–222`. A wet sequence spanning updates is a necessary regression case. Do not assume legacy local temporaries have portable persistence across subroutine calls. |
| finding-clock | `bmi_topmodel.c:394–400,451,469–498`: integer step incremented by double dt; time multiplies the step by dt | For dt=2, one update from step zero sets step=2 and reports time=4. For dt=0.5 the integer can remain zero. These are arithmetic traces, not measured runs. |
| finding-until | `bmi_topmodel.c:469–498`: extra update occurs even at zero fraction; failure results ignored | Repeated-time and exact-step requests can still invoke science. At fractional dt, clock and precomputed hydrological scales are also inconsistent. Probe state as well as returned time/status. |
| finding-routing | `topmodel.c:331–338`: routing stops beyond current_time_step | Standalone `it` equals current_time_step, so positive-delay destinations are excluded. Coupled `it=1` gives a different evolving cutoff. Compare a pulse with positive initial delay and multiple weights; inspect future deposits and tail drainage. |
| finding-t0 | `topmodel.c:837–848`: exp(t0+log(dt)-tl) | `t0` is used as a logged input, unlike a literal physical transmissivity value. Do not silently substitute the units claimed in the parameter documentation. |
| finding-tl | `topmodel.c:504–518`: weighted mean of paired index values | The speculative time-lag comment in `topmodel.h:151` cannot establish meaning. Follow assignments. |
| finding-test-scope | `test/README.md:35–40` versus current CMake and tests | An old assertion of identical outputs is not a current test result. The present restart test explicitly identifies missing delayed-routing coverage. |
| finding-restore | `bmi_serialization.cpp:74–137`: state applied sequentially before all archive reads finish | Early version rejection is not general transaction rollback. Corrupt/truncated late payloads and hostile counts need separate investigation. Do not generalize the signature/version tests into complete validation. |
| finding-area | `topmodel.c:718–730`: area participates inside a subtraction and another multiplication | A unit-area check cannot establish correct scaling at area below 1. Compare the intended area-normalized histogram against literal operations and sum check before extending use. |

The table's evidence is the pinned [science](citation:src-science),
[infiltration](citation:src-infiltration), [Fortran](citation:src-fortran),
[clock](citation:src-clock), [routing](citation:src-routing),
[initialization](citation:src-initial), [terrain](citation:src-terrain),
[serializer](citation:src-state), [restart test](citation:src-restart-test),
and [historical test documentation](citation:src-test-doc). Each table locator
is narrower than those source records. These findings are curriculum evidence;
the target is not being repaired in this task.

## Equations recovered from current source

These are implementation expressions; full scientific justification remains an
authoring obligation. Let D denote mean saturation deficit (`sbar`), m the
deficit scale (`szm`), L the mean index (`tl`) and l_i the class index
(`lnaotb[i]`). The code computes local deficit as max(0, D+m(L-l_i)).
Larger l_i gives a smaller unclipped deficit when m>0. Baseflow for a step is
`szq*exp(-D/m)` and the mean deficit then increases by baseflow and decreases
by recharge. [Timestep](citation:src-science)

Using illustrative values D=0.04 m, m=0.02 m, L=5 and class indices 4,5,6
gives local deficits 0.06,0.04,0.02 m. If szq=0.001 m per step, baseflow is
0.0001353352832366127 m per step. With recharge 0.0002 m per step, next D is
0.039935335283236614 m. These numbers are invented examples, not catchment
measurements. Exponents are ratios of comparable quantities; the terrain and
logged-transmissivity conventions must remain compatible.

The root-zone variable is a deficit relative to field capacity; the unsaturated
variable is a positive store. Rain first subtracts from the former. A negative
remainder is moved into the latter. For a 0.003 m deficit and 0.005 m rain,
root-zone deficit becomes zero and unsaturated storage gains 0.002 m before
subsequent excess/drainage checks. Evaporation subsequently increases the deficit.
Do not call zero root-zone deficit full soil-profile saturation.
[Timestep comments and updates](citation:src-science)

Unsaturated drainage literally divides storage by `deficit_local*td*dt`, caps
the result by storage, then applies area weights. It is not the same expression
as multiplying a per-hour drainage rate by dt. The code removes stores below
1e-7 after drainage. A full lesson needs a unit audit, the legacy convention,
non-unit-step cases and an account of discarded residuals; hourly examples alone
cannot settle this. [Timestep](citation:src-science)

`tread` normalizes index-interval weights, evaluates a trapezoidal mean from
adjacent index boundaries, and appends a zero weight sentinel. `d_alloc`
itself adds one element (`topmodel.c:1295–1309`), so requesting N+1 for the
weight array creates indices through N+1. Do not translate the declared count
directly into a zero-based allocation without auditing the next-entry access.
[Terrain](citation:src-terrain)

## BMI exchanges and calibration consequences

The advertised interface has two inputs and fourteen outputs, all declared
scalar double values; eight parameter names have a separate table. The output
named `land_surface_water__runoff_mass_flux` is advertised in `m h-1`, not
mass/time units. Inspect the pointer mapping before converting it. This is a
name/metadata inconsistency; it is not a reason to invent a density conversion.
[Metadata](citation:src-bmi)

`Get_value` copies bytes; `Get_value_ptr` exposes borrowed storage. Model
finalization, state creation/freeing and parameter-triggered reallocation can
invalidate relevant pointers. Ordinary indexed access calculates offsets without
bounds checks; reserved serialization variables explicitly reject indexed
access. Scalar exchange index zero is not the same thing as an internal
Fortran-compatible array index. [Exchange implementation](citation:src-access)

`Set_value` for szm, t0, chv, rv or sr0 reconstructs routing and reinitializes
the discharge array. For szm, t0 or sr0 it also reinitializes water stores and
mean deficit. A mid-run parameter update is therefore not simply a future-only
parameter change. Compare baseline state before and after calibration calls.
Writing through a borrowed pointer bypasses this setter behavior.
[Parameter setter](citation:src-access)

## Restart and build evidence

Serialization writes one versioned, ordered Boost binary representation.
Topographic array lengths come from destination configuration, while routing
counts come from the payload and may trigger reallocation. The stored clock
applies only in resume mode; hotstart is the default and retains the destination
clock while applying the other archived values. The serializer rejects
standalone mode. Source-defined version checking does not promise portability
across arbitrary architectures or Boost versions. [Archive](citation:src-state)
and [state mode](citation:src-model).

The reserved protocol captures with `ngen::serialization_create`, reads
`ngen::serialization_size` and `ngen::serialization_state`, then releases
the held capture with `ngen::serialization_free`. Loading declares the size
before setting the state bytes. Read paths return a copy when using Get_value;
freeing a copied client buffer is separate from freeing the model's capture.
Check every return status. [Accessors](citation:src-access)

Current CMake requires Boost serialization >=1.86.0, sets C++17 for the archive,
and builds `topmodelbmi`, `topmodeldriver`, `simple_unit_tests`,
`serialization_unit_tests`, and `serialization_integration_tests`.
The source sets global C standard properties with an intention of C99; verify
actual compiler command flags before claiming enforcement on every toolchain.
CI puts AddressSanitizer flags on both C and C++ compilation and runs binaries
directly. CTest registration is absent from the inspected CMake file.
[Build](citation:src-build) [CI](citation:src-ci)

The restart integration source compares all advertised outputs at every forcing
step for straight, one-restart, and three-restart runs. Its introductory comment
explicitly limits routing coverage: num_delay=0 and one histogram ordinate.
Hotstart and internally selected resume have different tests; no claim is made
that a public BMI control selects resume. Test code was read, not run.
[Restart test](citation:src-restart-test) [Protocol test](citation:src-protocol-test)

## Terrain preparation and scientific scores

The preprocessing workflow invokes GDAL, TauDEM through mpiexec, and Python.
That does not make the hydrological timestep an MPI solver. The Python
histogram branch masks data, imposes a valid-data percentage threshold,
filters positive values, caps an upper tail, chooses up to 30 classes, and
sorts boundaries descending. These are substantive data transformations,
not neutral file conversion. The width-function mask and its raster alignment
need further review. Preserve projection, resolution, thresholds, versions,
and excluded-area accounting with any produced input.
[Workflow](citation:src-workflow) [Histogram](citation:src-preprocess)

In current `results`, f1 is the sum of squared paired errors and f2 is the sum
of absolute paired errors. The code computes population observation variance
and NSE as one minus mean squared error divided by that variance. Constant
observations give a zero denominator. These formulas do not establish what
the 1979 paper called F2, or that the current code performs optimization.
[Results](citation:src-results)

## References

The complete citations for every `src-*` record above are in `sources.md`.
All are NOAA-OWP TOPMODEL files at commit
`89e4dc529dfdf7f23b7365530973e9f238fb740d`, consulted 2026-09-11.
Additional exact locators used here: `src/main.c:17–81`,
`src/bmi_topmodel.c:286–343,1363–1452`, `src/topmodel.c:1295–1309`.
