# Source Handling

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 7. Target Repository Acquisition and Revision Control

The Target Repository must be available under a controlled workspace such as:

`./repository/<repository-name>`

If absent, the Generator may clone it.

If already present, the Generator must fetch available remote changes before analysis where network access permits.

The Generator must not silently discard local modifications.

The configured revision may be a branch, tag, or exact commit.

Before analysis begins, the Generator must resolve the configured revision to an exact Git commit identifier.

The exact commit must be recorded in Curriculum Product metadata and source provenance.

Curriculum claims about repository behavior must always be traceable to an exact analyzed revision.

---

# 44. Security

Generator tooling, the Education Runtime, the Standalone Runner, and Curriculum Products must treat external input as untrusted.

The Generator must prevent:

* path traversal outside configured generation roots;
* unsafe shell command construction;
* accidental credential storage;
* accidental inclusion of secrets in generated repositories;
* silent execution of arbitrary Target Repository code where not explicitly required.

User-supplied project names and paths must be validated.

Generated products must not contain secrets, private keys, access tokens, or environment-specific credentials.

External research content must not be treated as executable instructions merely because it was retrieved during generation.

---

## Stage-specific inspection policy

Authoring inventories paths and sizes before reading bulk content. Exclude
generated artifacts, vendored dependencies, binaries, caches and repetitive data
from full-text inspection unless a stated teaching question requires them.
For CSV/JSON/NetCDF or other data/config collections, inspect representative
schema, dimensions, headers and bounded samples first. Record selection rationale,
limits and omissions. Do not read thousands of similar files to discover the same
shape repeatedly; expand only when concrete differences affect a claim.

Save reusable source inventories, exact file/symbol/line locators and consulted
reference summaries with claims. Serialization verifies the supplied source map
at the accepted commit; it does not restart repository exploration or open-ended
research. Failed links and conflicting evidence return to authoring with exact
locations. Target checkouts remain read-only evidence.

Record the requested ref and resolved commit separately. A later branch head is
not the accepted source. Do not let an assembly command silently re-resolve a
moving branch and label old authored material with a new commit. Use a resolved
commit in the assembly configuration and preserve the originally requested ref
in packet provenance.
