---
handoff_version: "1.0"
status: "blocked"
requested_revision: "master"
resolved_revision: "89e4dc529dfdf7f23b7365530973e9f238fb740d"
generator_revision: "9efb8fa3190594acf157e826d55e6591777ee781"
---
# TOPMODEL authoring checkpoint

Target: `topmodel`; display name: `topmodel BMI`; product: `topmodel_curriculum`.
Source URL: `https://github.com/NOAA-OWP/topmodel.git`.
Output: `authored/topmodel/` (specification default).
The user selected master. The updated configuration already pinned its verified
head; that configuration was preserved. No later moving branch head is implied.

Configuration validation passes. Current configuration SHA-256:
`23a174a2a30f5dbd66f3560e0876752ed2f86c9e617fe79170a04de6115653fe`.
The 26 required topic groups remain scope obligations in `topmodel.project.json`.
They have not been treated as teaching text or verified source claims.

Learner baseline: professional Python, C or C++ development, secondary-school
algebra/arithmetic, no assumed hydrology, calculus or numerical modeling.
Calculus must be taught progressively because it is explicitly requested.
The reading-level default is grade 8–10 ordinary prose with full technical depth.

## Current outcome

The missing-revision issue is resolved. Source analysis, evidence locators and
bounded arithmetic checks are recorded. Now written in_review: one lesson, one
pop review and six questions; the initial knowledge map covers all 26 topic
groups in 24 domains. No full-course acceptance is claimed. The packet is **not authoring_ready** and must not be serialized
as an accepted curriculum. The current blocker is readable original-paper
evidence for configured topic 23; see `topmodel-paper-readable-evidence` in
`issues.md`. All unfinished teaching and review obligations are in `completion.md`.

## Profile and worktree provenance

Generator code is pinned to the revision above; local uncommitted specifications
are additional authority and are not falsely attributed to that Git commit.
Root SPEC SHA-256: `5de07bf3e8acaa3a0071f00cfd7ccad38863bdc07dbbc898695ed02809e53647`.
Profile file `spec/serialization/schema.md` SHA-256:
`b2babb5af74ca3e9a0eb39373736c6d07c5177c0027764929f590705f295f60d`.
The profile documents schema 2.2 versus generator constant 2.1; the incompatibility
is a recorded serialization release issue. This checkpoint does not certify a
complete compatible profile, product version, or release. Runtime compatibility
configuration remains `>=1.1,<2.0`. Automated product commits are disabled.

## Ordered checkpoint inventory

These SHA-256 values identify current partial files, not acceptance. The manifest
excludes itself. All substantive review gates remain open.

| Path | SHA-256 |
| --- | --- |
| assessments/tm-evidence-review.md | bb68b8003015e9ea8b963e2a55ec390547478fd23fc129578277ada7328e0566 |
| CHANGELOG.md | ba7eda058ec36abee3d79310640546ebc628d49ab009ac87485e9c18b87c2f03 |
| completion.md | 9e9f7ecb362476026feec44c8c7d9fa0a957297c4a0a9c2febe377f7ae50621b |
| curriculum.md | ebaffd50e6046ef1a8b3a2eb9a213e1c549f8b3ae57180d04e48d5061aee134b |
| decisions.md | 2a72a7fa8b19791967a2996d73384fdd8cefc100d9a3616727d5ebc6959d60b8 |
| issues.md | 36b20bdc069fd91780358b3d6235a2f04bdea3441d65470241071bdab2546902 |
| knowledge-map.md | 3f390a109f5d9526770b8bd00eb6850f1a6a82c442b543ba056f605d9e5ee8b4 |
| lessons/tm-evidence.md | 2c604ba5eb800b4c9cf25a7c50bfe2655d45a3b2f30dcc1d5c2612f3546f24c4 |
| mastery-contracts.md | e005c373e24790fa163a8c3b7cc51f8cb554605b4ae38a901dd00c26edb3fb63 |
| questions/tm-evidence-bank.md | e60a74db94840fe5c783ba443f1573f960f8a4fdf2a11375596567ad6020d41a |
| research.md | 6fb1790ad1dc2790a43625f1ecae7b04476c55f20cddef564d2280ceb9d27794 |
| review-checks.md | 18b333c7ec39de3ec87cf81b1249376fccdce15b9da18786b471e0b6226edc6a |
| source-analysis.md | daef0cf6bafb30b269473dc21ff076df7224d9ae220dd0626332007ad2a73b7e |
| source-inventory.md | bb9c9e43a50cc43a4812b15efb06dcb6327b01d66d7318f7e6d1ed09599b3921 |
| sources.md | 602f02f486f6ccb95303f49dd4d09e07ea0d2f2e764abf42398cb1cf13e3101f |

Initial curriculum design, knowledge map, mastery contract, lesson and pop-review
bank are now written. Remaining lessons, contracts, terminology, glossary, claims,
coverage and comprehensive assessments remain incomplete. Analysis sidecars do
not substitute for teaching. Review-checks.md records the additional validation.

## Review and resumption

Review record: `review-checks.md`, including checked content hashes, exact command,
results and limits. Review was model-assisted static analysis, not human review.
`research.md` records consulted URLs and failed retrievals. `source-inventory.md`
preserves all tree metadata without ingesting large/repetitive data.

The user has no paper copy. Legacy IAHS and NTUA URLs also returned HTTP 404.
Do not repeat the request for a user copy. Final acceptance still requires readable
original-paper evidence or an explicit user-approved scope change. Continue
independent teaching from the knowledge map with:

> Read and execute prompt.md, continuing authored/topmodel/MANIFEST.md. Reuse the
> saved source analysis, keeping topmodel-paper-readable-evidence unresolved. Preserve
> source commit 89e4dc529dfdf7f23b7365530973e9f238fb740d and reuse the saved analysis.

Only after authoring acceptance, the exact serialization prompt is:

> Read docs/agent/SERIALIZATION_PROMPT.md and execute it using the accepted
> authored/topmodel/MANIFEST.md. Verify authoring_ready and all acceptance hashes
> before transformation. Preserve the packet’s exact source commit.
