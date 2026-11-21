# Ground-truth tooling

These files produced every program, README, CBOM and ledger in this corpus. Nothing here is needed to build or run
the five programs.

| File | Role |
|---|---|
| `spec.py` | Canonical registry shared by all languages: scenarios, algorithm assets (CycloneDX properties, OIDs, security levels, NIST / CNSA 2.0 status), related crypto material, the certificate, the TLS protocol asset, marker roles and the non-asset lexicon |
| `languages.py` | Per-language libraries (purl, licence), API-symbol prefixes, scope detection, notes and runtime facts |
| `markers.py` | Marker parser and coordinate computation |
| `build_sources.py` | Strips the markers from `templates/` and writes the delivered sources and build manifests |
| `docs.py` | Writes each language's `README.md`, `cbom.cdx.json` and `ground-truth.json`, plus the corpus `README.md` |
| `artifacts.py` | The `Artifacts/` case: `generate` creates the certificate, key, keystore, secret and configuration files once; the default command parses them, checks every object and writes the case's `README.md`, `cbom.cdx.json` and `ground-truth.json` plus the corpus `README.md` |
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

## The Artifacts case

`Artifacts/` has no template: its ground truth comes from the files themselves.

```sh
cd _tooling
python3 artifacts.py                   # parse ../Artifacts, check it, write its README, CBOM and ledger
python3 artifacts.py generate --force  # new keys, certificates and secrets first (fingerprints change)
```

`artifacts.py` needs the `cryptography` package with ML-DSA and ML-KEM support (tested with 50.0.1, which bundles
OpenSSL 4.0.2); the program cases still need only the standard library. The registry at the top of the script (`FILES`,
`KEYS`, `CERTS`, `CRL_SPEC`, `CSR_SPEC`) fixes names, serials, validity periods and algorithms; keys, signatures, salts
and secrets are random. The default command refuses to write anything if a file does not parse, a certificate does not
verify under its issuer, a key does not match its certificate, a password does not open its container, or a generated
document would contain PEM armour or a secret value (the case README is copied into every tool workspace).
Algorithms that only this case uses are registered in `spec.py` like the others.

To add an artifact, add it to `FILES` (and `CERTS` or `KEYS` if it holds a new certificate or key), write it in
`generate()`, teach the matching parser in `Analysis` about any new structure, and run `generate --force`.
