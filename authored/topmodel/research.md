---
handoff_version: "1.0"
status: "blocked"
---
# Required primary-paper evidence

Required source: K. J. Beven and M. J. Kirkby (1979), “A physically based,
variable contributing area model of basin hydrology,” Hydrological Sciences
Bulletin 24(1), 43–69. DOI: `10.1080/02626667909491834`.

The pinned repository README links this DOI. The supplied configuration's
paper-specific tasks require more than bibliographic verification. The current
C and historical Fortran can establish their own behavior but cannot establish
the exact original publication's figures and equations.

## Retrieval log, 2026-09-11

| Source | Result | Use and limitation |
| --- | --- | --- |
| https://www.tandfonline.com/doi/abs/10.1080/02626667909491834 | Search returned bibliographic metadata and abstract | Identity confirmed; not a full-paper review |
| https://www.tandfonline.com/doi/pdf/10.1080/02626667909491834 | Browser retrieval HTTP 403 | PDF not obtained |
| https://www.tandfonline.com/doi/epdf/10.1080/02626667909491834 | Retrieval error | No readable page images |
| https://www.tandfonline.com/doi/full/10.1080/02626667909491834 | Browser retrieval failure | No full-text verification |
| https://www.tandfonline.com/doi/pdf/10.1080/02626667909491834?download=true | Browser error; direct curl HTTP 403, exit 22 | No PDF obtained |
| https://eprints.whiterose.ac.uk/id/eprint/111293/ | Abstract and metadata; explicitly no full-text download | No page images |
| https://research.lancaster-university.uk/en/publications/a-physically-based-variable-contributing-area-model-of-basin-hydr/ | Abstract, metadata, DOI link | No independent full-text attachment found |
| https://www.scribd.com/document/368361723/A-Physically-Based-Variable-Contributing-Area-Model-of-Basin-Hydrology-Un-Mod-Le-Base-Physique-de-Zone-d-Appel-Variable-de-l-Hydrologie-Du-Bassin | Partial consultation of a 28-page reproduction's extracted text | Some prose readable; equations damaged, plots absent from text |

The OCR around printed page 49, equation 10, separates the summation and its
fraction into disconnected fragments. Printed page 50, equation 12, has damaged
symbols and integration limits. The extracted text at pages 61–62 contains
rotated-axis gibberish. Page 64 supplies the Figure 14 caption without readable
contours. These observations prevent reliable figure and notation verification.
Readable prose is a discovery aid, not authority for reconstructing missing
mathematical content. This checkpoint makes no full-paper review claim.

Local filename search under the workspace and `/tmp` found an LGAR PDF, but
no TOPMODEL/Beven/Kirkby PDF. No subscription, external message or purchase
was attempted. A request for a readable local path or URL was sent to the user
while independent source analysis continued. The user subsequently answered no.

## Additional public-copy checks after the user's reply

A bibliography at https://volaya.github.io/libro-sig/bib.htm identified the
legacy IAHS path `http://iahs.info/hsj/240/hysj_24_01_0043.pdf`. A published
reference list at https://www.ipabhi.org/serhidro/anais/anais2009/doc/pdfs/p92.pdf
identified `www.itia.ntua.gr/hsj/24/hysj_24_01_0043.pdf`. These bibliographies
were used only to discover possible locations, not as scientific evidence.

Both direct checks returned HTTP 404 (curl exit 22):

```bash
curl -L --fail --max-time 20 -o /tmp/topmodel-iahs-1979.pdf https://iahs.info/hsj/240/hysj_24_01_0043.pdf
curl -L --fail --max-time 30 -o /tmp/topmodel-beven-kirkby-1979.pdf https://www.itia.ntua.gr/hsj/24/hysj_24_01_0043.pdf
```

The source remains unavailable in readable form through the checked locations.
The user's no-copy answer is not authorization to omit the required paper review.
Independent source-evidence teaching was written while this acceptance blocker
remains open; see `lessons/tm-evidence.md` and `questions/tm-evidence-bank.md`.

## Exact direct-download check

```bash
curl -L --fail --max-time 30 -o /tmp/topmodel-beven-kirkby-1979.pdf 'https://www.tandfonline.com/doi/pdf/10.1080/02626667909491834?download=true'
```

Result: exit 22, HTTP 403. No usable PDF was obtained at that output path.

## Resume requirement

Read the supplied complete paper using page images to verify equations and
figures. Preserve the source bytes and checksum where permitted; retain exact
page/equation/figure locators with claim records. Then continue `prompt.md`
without reacquiring or reselecting a moving source branch. The accepted code
revision remains `89e4dc529dfdf7f23b7365530973e9f238fb740d`.
