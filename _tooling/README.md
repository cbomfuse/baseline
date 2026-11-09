# Ground-truth tooling

## Overview
| File | Role |
|---|---|
| `spec.py` | Canonical registry shared by all languages: scenarios, algorithm assets (CycloneDX properties, OIDs, security levels, NIST / CNSA 2.0 status), related crypto material, the certificate, the TLS protocol asset, marker roles and the non-asset lexicon |
| `languages.py` | Per-language libraries (purl, licence), API-symbol prefixes, scope detection, notes and runtime facts |
| `markers.py` | Marker parser and coordinate computation |
| `build_sources.py` | Strips the markers from `templates/` and writes the delivered sources and build manifests |
| `docs.py` | Writes each language's `README.md`, `cbom.cdx.json` and `ground-truth.json`, plus the corpus `README.md` |
| `verification.json` | Facts captured while building and running the programs (toolchains, Java provider resolution, Go TLS defaults) |
| `templates/<language>/` | The annotated program template (`*.tmpl`) and static build files |

## Marker grammar
Every cryptographic span in a template is wrapped like this (the markers never appear in the delivered sources):

```text
«ROLE ASSET[^PARENT][>PRODUCED,...][#SYMBOL][!NOTE]|CODE»
```

| Part | Meaning |
|---|---|
| `ROLE` | `kind[:qualifier]`, for example `op:encrypt`, `prm:iterations`, `alg`, `imp` (see `spec.ROLES`) |
| `ASSET` | Asset ID from `spec.py`, or a library ID from `languages.py` for imports |
| `^PARENT` | Composite asset this identifier parameterises, for example `sha-256^hkdf-sha256` |
| `>PRODUCED` | Material asset(s) whose value is produced at this location |
| `#SYMBOL` | Fully qualified API symbol; per-language prefixes such as `$jc.` are expanded |
| `!NOTE` | Note key resolved through `languages.COMMON_NOTES` or the language's own notes |
| `CODE` | The exact source text; markers may nest |

Coordinates are computed on the stripped text, so they are exact by construction. Go templates are written with
four-space indentation, which `build_sources.py` converts to tabs so the output is `gofmt`-clean.

## Regenerating
```sh
cd _tooling
python3 build_sources.py   # rewrites the five programs and their build manifests
python3 docs.py            # rewrites every README.md, cbom.cdx.json and ground-truth.json
```

Python 3.9 or later, standard library only. Unknown asset IDs, roles, library IDs or note keys stop the generator
with an error. `verification.json` is not refreshed automatically; update it if you re-run the programs elsewhere.

To add a scenario, register any new assets in `spec.py`, add the annotated code to all five templates, append the
expected output line to `../expected_output.txt`, and rerun both scripts.
