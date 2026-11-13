"""Generate README.md, cbom.cdx.json and ground-truth.json for every implementation,
plus the corpus-level README.md. Run after build_sources.py."""
import datetime
import json
import re
import uuid
from collections import Counter, OrderedDict
from pathlib import Path

import markers
import spec
from build_sources import OUT, TOOLING, load_template
from languages import COMMON_NOTES, LANGS

GEN_TIME = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ID_PREFIX = {"python": "PY", "java": "JV", "go": "GO", "typescript": "TS", "csharp": "CS"}
EXPECTED = (OUT / "expected_output.txt").read_text().splitlines()
VERIFY = json.loads((TOOLING / "verification.json").read_text())
TRANSITIVE = {"lib.bcutil": ["lib.bcpkix"], "lib.xsys": ["lib.xcrypto", "lib.circl"]}
KIND_ORDER = {"algorithm": 0, "certificate": 1, "protocol": 2, "related-crypto-material": 3}
ALG_ORDER = {aid: i for i, aid in enumerate(spec.ALGORITHMS)}
MAT_ORDER = {mid: i for i, mid in enumerate(spec.MATERIALS)}


def asset_kind(aid):
    if aid in spec.ALGORITHMS:
        return "algorithm"
    if aid in spec.MATERIALS:
        return "related-crypto-material"
    if aid in spec.CERTIFICATES:
        return "certificate"
    if aid in spec.PROTOCOLS:
        return "protocol"
    raise KeyError(f"unknown asset id {aid!r}")


def asset_name(aid):
    for table in (spec.ALGORITHMS, spec.MATERIALS, spec.CERTIFICATES, spec.PROTOCOLS):
        if aid in table:
            return table[aid]["name"]
    return aid


def bom_ref(aid):
    kind = asset_kind(aid)
    if kind == "algorithm":
        return f"crypto/algorithm/{aid}"
    if kind == "related-crypto-material":
        return f"crypto/related-crypto-material/{aid[2:]}"
    if kind == "certificate":
        return f"crypto/certificate/{aid.split('.', 1)[1]}"
    return f"crypto/protocol/{aid}"


def sort_key(aid):
    kind = asset_kind(aid)
    return (KIND_ORDER[kind], ALG_ORDER.get(aid, MAT_ORDER.get(aid, 0)), aid)


# ---------------------------------------------------------------- analysis
def regions(text, lang):
    """Comment and string regions (start, end, kind); everything else is code."""
    out, i, n = [], 0, len(text)
    quotes = sorted(lang.strings, key=len, reverse=True)
    while i < n:
        hit = None
        for tok in lang.line_comment:
            if text.startswith(tok, i):
                j = text.find("\n", i)
                hit = (i, n if j < 0 else j, "comment")
                break
        if not hit:
            for opn, cls in lang.block_comment:
                if text.startswith(opn, i):
                    j = text.find(cls, i + len(opn))
                    hit = (i, n if j < 0 else j + len(cls), "comment")
                    break
        if not hit:
            for q in quotes:
                if text.startswith(q, i):
                    raw = lang.key == "go" and q == "`"
                    j = i + len(q)
                    while j < n:
                        if text[j] == "\\" and not raw:
                            j += 2
                            continue
                        if text.startswith(q, j):
                            j += len(q)
                            break
                        if len(q) == 1 and q != "`" and text[j] == "\n":
                            break
                        j += 1
                    hit = (i, j, "string")
                    break
        if hit:
            out.append(hit)
            i = hit[1]
        else:
            i += 1
    return out


def analyse(lang):
    text, spans = markers.parse(load_template(lang), lang.template)
    pos = markers.positions(text)
    lines = text.split("\n")
    func_re = re.compile(lang.func_re)
    headers = [(i, m.group(1)) for i, line in enumerate(lines, 1) if (m := func_re.match(line))]
    notes_all = dict(COMMON_NOTES, **lang.notes)
    libs = {lib["id"]: lib for lib in lang.libs}
    prefixes = sorted(lang.prefixes.items(), key=lambda kv: len(kv[0]), reverse=True)

    def scope_of(line_no):
        name = lang.module_scope
        for ln, nm in headers:
            if ln > line_no:
                break
            name = nm
        return name

    def expand(sym):
        for pre, full in prefixes:
            if sym.startswith(pre):
                return full + sym[len(pre):]
        return sym

    def lib_of(sym):
        if not sym:
            return None
        for pre, lid in lang.lib_rules:
            if sym.startswith(pre):
                return lid
        return None

    raw = []
    for sp in spans:
        meta = sp["meta"]
        kind, _, qual = meta["role"].partition(":")
        if kind not in spec.ROLES:
            raise ValueError(f"{lang.key}: unknown role {meta['role']}")
        asset = meta["asset"].strip()
        parent = meta["parent"].strip() if meta["parent"] else None
        produces = [p.strip() for p in meta["prod"].split(",")] if meta["prod"] else []
        sym = expand(meta["sym"].strip()) if meta["sym"] else None
        note = meta["note"].strip() if meta["note"] else None
        if kind == "imp":
            if asset not in libs:
                raise ValueError(f"{lang.key}: unknown library {asset}")
        else:
            asset_kind(asset)
        for x in [parent, *produces]:
            if x:
                asset_kind(x)
        if note and note not in notes_all:
            raise ValueError(f"{lang.key}: unknown note key {note}")
        raw.append(dict(sp=sp, kind=kind, qual=qual or None, role=meta["role"], asset=asset,
                        parent=parent, produces=produces, symbol=sym, note=note))
    for r in raw:
        lib = r["asset"] if r["kind"] == "imp" else lib_of(r["symbol"])
        if lib is None:
            best = None
            for o in raw:
                if o is r or not o["symbol"]:
                    continue
                if (o["sp"]["start"] <= r["sp"]["start"] and o["sp"]["end"] >= r["sp"]["end"]
                        and o["sp"]["depth"] < r["sp"]["depth"]):
                    if best is None or o["sp"]["depth"] > best["sp"]["depth"]:
                        best = o
            lib = lib_of(best["symbol"]) if best else lang.libs[0]["id"]
        r["library"] = lib

    occs = []
    for n, r in enumerate(raw, 1):
        s, e = r["sp"]["start"], r["sp"]["end"]
        l1, c1, b1 = pos(s)
        l2, c2, b2 = pos(e)
        scope = scope_of(l1)
        m = re.match(r"^[sS](\d{2})", scope)
        if m:
            scen = "S" + m.group(1)
        elif scope in lang.helpers:
            scen = lang.helpers[scope]
        elif r["kind"] == "imp":
            scen = "-"
        elif r["asset"] in spec.MATERIALS:
            scen = spec.MATERIALS[r["asset"]]["scenario"]
        else:
            scen = "shared"
        occs.append(OrderedDict(
            id=f"{ID_PREFIX[lang.key]}-{n:03d}", file=lang.target, scenario=scen, scope=scope,
            role=r["role"], kind=r["kind"], qualifier=r["qual"], asset=r["asset"], parent=r["parent"],
            produces=r["produces"], symbol=r["symbol"], library=r["library"], note=r["note"],
            start=OrderedDict(line=l1, column=c1, charOffset=s, byteOffset=b1),
            end=OrderedDict(line=l2, column=c2, charOffset=e, byteOffset=b2),
            length=OrderedDict(chars=e - s, bytes=b2 - b1), nesting=r["sp"]["depth"],
            evidence=text[s:e]))

    # assets referenced directly, as parents, as produced material, or implicitly
    assets = OrderedDict()

    def touch(aid, oid=None, relation=None):
        a = assets.setdefault(aid, dict(id=aid, kind=asset_kind(aid), occ=[], implicit=True))
        if oid:
            a["occ"].append((oid, relation))
            a["implicit"] = False

    for o in occs:
        if o["kind"] == "imp":
            continue
        touch(o["asset"], o["id"], "direct")
        if o["parent"]:
            touch(o["parent"], o["id"], f"parameter:{o['asset']}")
        for p in o["produces"]:
            touch(p, o["id"], "produced")
    changed = True
    while changed:
        changed = False
        for aid in list(assets):
            deps = []
            if aid in spec.ALGORITHMS:
                deps = spec.ALGORITHMS[aid]["dependsOn"]
            elif aid in spec.PROTOCOLS:
                deps = [a for cs in spec.PROTOCOLS[aid]["cipherSuites"] for a in cs["algorithms"]]
            elif aid in spec.MATERIALS:
                deps = [spec.MATERIALS[aid]["algorithmRef"]]
            elif aid in spec.CERTIFICATES:
                deps = [spec.CERTIFICATES[aid]["signatureAlgorithmRef"], spec.CERTIFICATES[aid]["subjectPublicKeyRef"]]
            for d in deps:
                if d not in assets:
                    touch(d)
                    changed = True
    assets = OrderedDict(sorted(assets.items(), key=lambda kv: sort_key(kv[0])))
    by_id = {o["id"]: o for o in occs}
    for a in assets.values():
        funcs = set()
        for oid, rel in a["occ"]:
            o = by_id[oid]
            if rel == "direct" and o["kind"] in ("op", "init", "ctor") and o["qualifier"] in spec.CDX_FUNCTION:
                funcs.add(spec.CDX_FUNCTION[o["qualifier"]])
        a["functions"] = sorted(funcs)

    # non-asset mentions
    covered = bytearray(len(text))
    for o in occs:
        covered[o["start"]["charOffset"]:o["end"]["charOffset"]] = b"\x01" * o["length"]["chars"]
    regs = regions(text, lang)
    decoys = []
    for m in re.finditer(spec.DECOY_PATTERN, text):
        if any(covered[m.start():m.end()]):
            continue
        ctx = next((k for (a, b, k) in regs if a <= m.start() < b), "code")
        l1, c1, b1 = pos(m.start())
        line = lines[l1 - 1]
        if ctx == "code":
            tok = re.search(r"[A-Za-z0-9_$]*\Z", text[:m.start()]).group(0) + re.match(r"[A-Za-z0-9_$]*", text[m.start():]).group(0)
            why = lang.decoy_overrides.get(tok, "Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset")
            ctx = "identifier"
        elif ctx == "comment":
            tok = line.strip()
            why = "Comment text; documentation only"
        else:
            tok = next(text[a:b] for (a, b, k) in regs if a <= m.start() < b)
            why = ("Output label passed to emit(); printed text only" if re.search(r"\b[eE]mit\(", line)
                   else "String literal not consumed by a crypto API")
        decoys.append(OrderedDict(id=f"{ID_PREFIX[lang.key]}-N{len(decoys) + 1:03d}", line=l1, column=c1,
                                  charOffset=m.start(), byteOffset=b1, length=len(m.group(0)), text=m.group(0),
                                  context=ctx, token=tok, reason=why))
    notes_used = OrderedDict()
    for o in occs:
        if o["note"]:
            notes_used.setdefault(o["note"], []).append(o["id"])
    return dict(lang=lang, text=text, occs=occs, by_id=by_id, assets=assets, decoys=decoys,
                notes_used=notes_used, notes_all=notes_all, libs=libs, lines=len(lines) - (1 if text.endswith("\n") else 0))


# ---------------------------------------------------------------- CycloneDX 1.6
def cbom(A):
    lang = A["lang"]
    app_ref = f"application/cbom-corpus-{lang.key}"
    components = []
    lib_provides = {lib["id"]: set() for lib in lang.libs}
    for o in A["occs"]:
        if o["kind"] != "imp":
            lib_provides[o["library"]].add(bom_ref(o["asset"]))
    for lib in lang.libs:
        components.append(OrderedDict([
            ("type", "library"), ("bom-ref", lib["purl"]), ("name", lib["name"]), ("version", lib["version"]),
            ("scope", "required"), ("licenses", [{"expression": lib["license"]}]), ("purl", lib["purl"]),
            ("description", lib["desc"]),
            ("properties", [{"name": "cbom-corpus:library-id", "value": lib["id"]},
                            {"name": "cbom-corpus:dependency-scope", "value": lib["scope"]}])]))
    for aid, a in A["assets"].items():
        kind = a["kind"]
        comp = OrderedDict([("type", "cryptographic-asset"), ("bom-ref", bom_ref(aid)), ("name", asset_name(aid))])
        props = [{"name": "cbom-corpus:asset-id", "value": aid},
                 {"name": "cbom-corpus:implicit", "value": "true" if a["implicit"] else "false"},
                 {"name": "cbom-corpus:occurrence-count", "value": str(len(a["occ"]))}]
        if kind == "algorithm":
            d = spec.ALGORITHMS[aid]
            ap = OrderedDict([("primitive", d["primitive"])])
            if d["parameterSetIdentifier"]:
                ap["parameterSetIdentifier"] = d["parameterSetIdentifier"]
            if d["curve"]:
                ap["curve"] = d["curve"]
            ap["executionEnvironment"] = "software-plain-ram"
            ap["implementationPlatform"] = "generic"
            ap["certificationLevel"] = ["none"]
            if d["mode"]:
                ap["mode"] = d["mode"]
            if d["padding"]:
                ap["padding"] = d["padding"]
            if a["functions"]:
                ap["cryptoFunctions"] = a["functions"]
            if d["classicalSecurityLevel"] is not None:
                ap["classicalSecurityLevel"] = d["classicalSecurityLevel"]
            if d["nistQuantumSecurityLevel"] is not None:
                ap["nistQuantumSecurityLevel"] = d["nistQuantumSecurityLevel"]
            cp = OrderedDict([("assetType", "algorithm"), ("algorithmProperties", ap)])
            if d["oid"]:
                cp["oid"] = d["oid"]
            props += [{"name": "cbom-corpus:family", "value": d["family"]},
                      {"name": "cbom-corpus:standards", "value": "; ".join(d["standards"])},
                      {"name": "cbom-corpus:nist-status", "value": d["nistStatus"]},
                      {"name": "cbom-corpus:cnsa-2.0", "value": d["cnsa2"]},
                      {"name": "cbom-corpus:quantum", "value": d["quantum"]}]
            if d["note"]:
                props.append({"name": "cbom-corpus:note", "value": d["note"]})
        elif kind == "related-crypto-material":
            d = spec.MATERIALS[aid]
            rp = OrderedDict([("type", d["type"]), ("id", aid), ("state", "active"),
                              ("algorithmRef", bom_ref(d["algorithmRef"]))])
            if d["size"]:
                rp["size"] = d["size"]
            cp = OrderedDict([("assetType", "related-crypto-material"), ("relatedCryptoMaterialProperties", rp)])
            props.append({"name": "cbom-corpus:provenance", "value": d["provenance"]})
            if d["value"]:
                props.append({"name": "cbom-corpus:test-vector-value", "value": d["value"]})
            if d["note"]:
                props.append({"name": "cbom-corpus:note", "value": d["note"]})
        elif kind == "certificate":
            d = spec.CERTIFICATES[aid]
            cp = OrderedDict([("assetType", "certificate"), ("certificateProperties", OrderedDict([
                ("subjectName", d["subjectName"]), ("issuerName", d["issuerName"]),
                ("signatureAlgorithmRef", bom_ref(d["signatureAlgorithmRef"])),
                ("subjectPublicKeyRef", bom_ref(d["subjectPublicKeyRef"])),
                ("certificateFormat", d["certificateFormat"])]))])
            props += [{"name": "cbom-corpus:not-valid-before", "value": d["notValidBefore"]},
                      {"name": "cbom-corpus:not-valid-after", "value": d["notValidAfter"]},
                      {"name": "cbom-corpus:serial", "value": d["serial"]}]
        else:
            d = spec.PROTOCOLS[aid]
            cp = OrderedDict([("assetType", "protocol"), ("protocolProperties", OrderedDict([
                ("type", d["type"]), ("version", d["version"]),
                ("cipherSuites", [OrderedDict([("name", cs["name"]),
                                               ("algorithms", [bom_ref(x) for x in cs["algorithms"]]),
                                               ("identifiers", cs["identifiers"])]) for cs in d["cipherSuites"]])]))])
            props.append({"name": "cbom-corpus:note", "value": d["note"]})
        for key, text in lang.implicit:
            if key == aid:
                props.append({"name": f"cbom-corpus:{lang.key}-runtime-note", "value": text})
        comp["cryptoProperties"] = cp
        if a["occ"]:
            occ_list = []
            for oid, rel in a["occ"]:
                o = A["by_id"][oid]
                item = OrderedDict([("location", o["file"]), ("line", o["start"]["line"]),
                                    ("offset", o["start"]["column"] - 1)])
                if o["symbol"]:
                    item["symbol"] = o["symbol"]
                item["additionalContext"] = (
                    f"id={oid}; relation={rel}; role={o['role']}; scenario={o['scenario']}; scope={o['scope']}; "
                    f"end={o['end']['line']}:{o['end']['column']}; charRange={o['start']['charOffset']}-{o['end']['charOffset']}; "
                    f"byteRange={o['start']['byteOffset']}-{o['end']['byteOffset']}; library={o['library']}")
                occ_list.append(item)
            comp["evidence"] = {"occurrences": occ_list}
        comp["properties"] = props
        components.append(comp)
    deps = OrderedDict()

    def dep(ref):
        return deps.setdefault(ref, OrderedDict([("ref", ref)]))

    direct_libs = [lib for lib in lang.libs if lib["scope"] != "transitive"]
    dep(app_ref)["dependsOn"] = [lib["purl"] for lib in direct_libs]
    purl = {lib["id"]: lib["purl"] for lib in lang.libs}
    for child, parents in TRANSITIVE.items():
        for p in parents:
            if child in purl and p in purl:
                dep(purl[p]).setdefault("dependsOn", []).append(purl[child])
    for lib in lang.libs:
        if lib_provides[lib["id"]]:
            dep(lib["purl"])["provides"] = sorted(lib_provides[lib["id"]])
    for aid in A["assets"]:
        if aid in spec.ALGORITHMS and spec.ALGORITHMS[aid]["dependsOn"]:
            dep(bom_ref(aid))["dependsOn"] = [bom_ref(x) for x in spec.ALGORITHMS[aid]["dependsOn"] if x in A["assets"]]
    return OrderedDict([
        ("$schema", "http://cyclonedx.org/schema/bom-1.6.schema.json"), ("bomFormat", "CycloneDX"),
        ("specVersion", "1.6"), ("serialNumber", "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, f"cbom-corpus/{lang.key}"))),
        ("version", 1),
        ("metadata", OrderedDict([
            ("timestamp", GEN_TIME),
            ("tools", {"components": [{"type": "application", "name": "cbom-corpus ground-truth generator (_tooling/docs.py)", "version": "1.0.0"}]}),
            ("component", OrderedDict([("type", "application"), ("bom-ref", app_ref), ("name", f"cbom-corpus-{lang.key}"),
                                       ("version", "1.0.0"),
                                       ("description", f"Ground-truth CBOM for {lang.target} ({lang.title}); every occurrence is hand-annotated, not scanner output.")]))])),
        ("components", components), ("dependencies", list(deps.values()))])


# ---------------------------------------------------------------- markdown helpers
def code(s):
    s = s.replace("|", "\\|")
    return f"`` {s} ``" if "`" in s else f"`{s}`"


def ev(s, limit=None):
    first, *rest = s.split("\n")
    out = first if not rest else first + f" … (+{len(rest)} lines)"
    if limit and len(out) > limit:
        out = out[:limit - 1] + "…"
    return code(out)


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def loc(o, which="start"):
    return f"{o[which]['line']}:{o[which]['column']}"


def ids(lst):
    return ", ".join(lst) if lst else "-"


def readme(A):
    lang, occs, assets = A["lang"], A["occs"], A["assets"]
    v = VERIFY[lang.key]
    n_alg = sum(1 for a in assets.values() if a["kind"] == "algorithm")
    n_mat = sum(1 for a in assets.values() if a["kind"] == "related-crypto-material")
    roles = Counter(o["kind"] for o in occs)
    L = []
    w = L.append
    w(f"# CBOM ground-truth corpus - {lang.title}\n")
    w(f"`{lang.target}` is the {lang.title} implementation of a 24-scenario cryptography program that is logically "
      f"identical in Python, Java, Go, TypeScript and C#. This file records every location where a cryptographic "
      f"asset appears in it: **{len(occs)} occurrences** of **{len(assets)} assets** ({n_alg} algorithms, {n_mat} "
      f"items of related crypto material, 1 certificate, 1 protocol) drawn from **{len(lang.libs)} library components**, "
      f"plus **{len(A['decoys'])} non-asset mentions** of algorithm names that a scanner should *not* report. "
      f"The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.\n")
    w("> All keys, IVs, salts, seeds and passwords in this program are published test vectors or are generated at run time. "
      "Weak and legacy algorithms (MD5, SHA-1, AES-ECB, 3DES, a 24-bit HMAC key) are deliberate so that policy checks have something to find.\n")
    w("## Files\n")
    files = [(f"`{lang.target}`", f"The program ({A['lines']} lines, ASCII, LF line endings)")]
    for item in sorted((OUT / lang.dir).rglob("*")):
        rel = item.relative_to(OUT / lang.dir).as_posix()
        if item.is_file() and rel not in (lang.target, "README.md", "cbom.cdx.json", "ground-truth.json"):
            files.append((f"`{rel}`", "Build manifest"))
    files += [("`README.md`", "This document"), ("`cbom.cdx.json`", "Ground-truth CycloneDX 1.6 CBOM (validated against the official 1.6 JSON schema)"),
              ("`ground-truth.json`", "Complete occurrence ledger, asset inventory and non-asset mentions")]
    w(table(["File", "Purpose"], files) + "\n")
    w("## Build and run\n")
    w("```sh\n" + "\n".join(lang.run) + "\n```\n")
    w(f"Verified in the build environment with {v['toolchain']}: {v['build']}. Standard output was byte-identical to the "
      f"other four implementations (see the corpus README).\n")
    w("## Expected output\n")
    w("Deterministic lines are known-answer tests (published vectors where one exists); randomized scenarios print only "
      "booleans and sizes, so the output is identical on every run and in every language.\n")
    w("```text\n" + "\n".join(EXPECTED) + "\n```\n")
    w("## How occurrences are recorded\n")
    w("An **occurrence** is a contiguous span of source text that names, configures or exercises a cryptographic asset. "
      "Coordinates use these conventions:\n")
    w(table(["Field", "Convention"], [
        ("Line", "1-based"),
        ("Column", "1-based, counted in Unicode code points (the source is pure ASCII, so it equals the byte column)"),
        ("End", "Exclusive: the position just after the last character of the span"),
        ("Char / byte offset", "0-based offset from the start of the file; ranges are half-open `[start, end)`"),
        ("Nesting", "Spans may nest (for example a transformation string inside a `getInstance` call); each span is its own occurrence"),
        ("CycloneDX `offset`", "Written as column - 1 (0-based column); absolute ranges are in `additionalContext`"),
    ]) + "\n")
    w("Roles:\n")
    w(table(["Role", "Meaning"], [(f"`{k}`", v_) for k, v_ in spec.ROLES.items()]) + "\n")
    w("Recording rules: data-feeding calls (`update`, `updateAAD`, `setAAD`, `Write`, `BlockUpdate`, `doPhase`) are not "
      "recorded separately; imports are recorded only for crypto-specific modules; material produced by an operation is "
      "attributed to that operation's span (`produces`); a hash or MGF identifier used inside a composite scheme is recorded "
      "against the hash asset with the composite as its parent (`^`), and it is also listed under the parent asset; a call site "
      "that serves two assets depending on the caller is recorded once per asset.\n")
    w("## Summary\n")
    w(table(["Measure", "Count"], [("Occurrences", len(occs))] +
            [(f"Occurrences with role `{k}`", roles[k]) for k in spec.ROLES if roles[k]] +
            [("Algorithm assets (incl. implicit)", n_alg),
             ("Implicit assets (no source occurrence)", sum(1 for a in assets.values() if a["implicit"])),
             ("Related crypto material", n_mat), ("Certificates", 1), ("Protocols", 1),
             ("Library components", len(lang.libs)), ("Non-asset mentions", len(A["decoys"]))]) + "\n")
    w("## Libraries\n")
    rows = []
    for lib in lang.libs:
        imps = [o["id"] for o in occs if o["kind"] == "imp" and o["asset"] == lib["id"]]
        uses = [o for o in occs if o["kind"] != "imp" and o["library"] == lib["id"]]
        provided = sorted({o["asset"] for o in uses}, key=sort_key)
        rows.append((f"`{lib['id']}`", lib["name"], lib["version"], code(lib["purl"]), lib["license"], lib["scope"],
                     ids(imps), len(uses), ", ".join(provided) or "-", lib["desc"]))
    w(table(["ID", "Component", "Version", "purl", "License", "Scope", "Import occurrences", "Other occurrences",
             "Assets provided", "Notes"], rows) + "\n")
    w("## Algorithm assets\n")
    w("Identity and parameters (`functions` lists the CycloneDX crypto functions actually exercised here):\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "algorithm":
            continue
        d = spec.ALGORITHMS[aid]
        rows.append((f"`{aid}`", d["name"], d["primitive"], d["family"], d["parameterSetIdentifier"] or "-",
                     d["mode"] or "-", d["padding"] or "-", d["curve"] or "-", ", ".join(a["functions"]) or "-",
                     d["oid"] or "-", "implicit" if a["implicit"] else len(a["occ"]),
                     ", ".join(d["dependsOn"]) or "-"))
    w(table(["Asset", "Name", "Primitive", "Family", "Parameter set", "Mode", "Padding", "Curve", "Functions", "OID",
             "Occurrences", "Depends on"], rows) + "\n")
    w("Security and compliance:\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "algorithm":
            continue
        d = spec.ALGORITHMS[aid]
        rows.append((f"`{aid}`", d["classicalSecurityLevel"] if d["classicalSecurityLevel"] is not None else "-",
                     d["nistQuantumSecurityLevel"] if d["nistQuantumSecurityLevel"] is not None else "-",
                     "; ".join(d["standards"]), d["nistStatus"], d["cnsa2"], d["quantum"], d["note"] or "-"))
    w(table(["Asset", "Classical bits", "NIST PQ category", "Standards", "NIST status", "CNSA 2.0", "Quantum", "Note"], rows) + "\n")
    w("Occurrences per algorithm (`direct` = the span names this asset; `parameter:x` = span names x inside this composite; "
      "`produced` = span produces this material):\n")
    rows = []
    for aid, a in assets.items():
        if a["occ"] and a["kind"] in ("algorithm", "certificate", "protocol"):
            rows.append((f"`{aid}`", ", ".join(f"{oid}" + ("" if rel == "direct" else f" ({rel})") for oid, rel in a["occ"])))
    w(table(["Asset", "Occurrence IDs"], rows) + "\n")
    w("## Certificate and protocol assets\n")
    c = spec.CERTIFICATES["cert.self-signed"]
    w(table(["Property", "Value"], [("Asset", "`cert.self-signed`"), ("Format", c["certificateFormat"] + " v3"),
                                     ("Subject / issuer", f"{c['subjectName']} / {c['issuerName']}"),
                                     ("Signature algorithm", "`ecdsa-p256-sha256`"), ("Subject public key", "`m.cert-public-key`"),
                                     ("Validity", f"{c['notValidBefore']} to {c['notValidAfter']}"), ("Serial", c["serial"]),
                                     ("Occurrences", ids([oid for oid, _ in assets['cert.self-signed']['occ']]))]) + "\n")
    p = spec.PROTOCOLS["tls13-client"]
    w(table(["Property", "Value"], [("Asset", "`tls13-client`"), ("Type / version", f"{p['type']} {p['version']}"),
                                     ("Cipher suites", "; ".join(f"{cs['name']} ({','.join(cs['identifiers'])})" for cs in p["cipherSuites"])),
                                     ("Note", p["note"]),
                                     ("Occurrences", ids([oid for oid, _ in assets['tls13-client']['occ']]))]) + "\n")
    w("## Related cryptographic material\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "related-crypto-material":
            continue
        d = spec.MATERIALS[aid]
        where = []
        for oid, rel in a["occ"]:
            o = A["by_id"][oid]
            where.append(f"{oid} @ {loc(o)}" + (" (produced)" if rel == "produced" else ""))
        rows.append((f"`{aid}`", d["name"], d["type"], d["size"] or "-", d["provenance"], d["value"] or "-",
                     f"`{d['algorithmRef']}`", d["scenario"], "; ".join(where) or "implicit", d["note"] or "-"))
    w(table(["Asset", "Name", "Type", "Size (bits)", "Provenance", "Test-vector value", "Used with", "Scenario",
             "Defined / produced at", "Note"], rows) + "\n")
    w("## Scenario map\n")
    rows = []
    for sid, desc, det in spec.SCENARIOS:
        so = [o for o in occs if o["scenario"] == sid]
        al = sorted({o["asset"] for o in so} | {o["parent"] for o in so if o["parent"]} |
                    {p for o in so for p in o["produces"]}, key=sort_key)
        lines_ = f"{min(o['start']['line'] for o in so)}-{max(o['end']['line'] for o in so)}" if so else "-"
        rows.append((sid, desc, det, len(so), lines_, ", ".join(f"`{x}`" for x in al)))
    w(table(["Scenario", "What it does", "Output", "Occurrences", "Lines", "Assets"], rows) + "\n")
    w("## Occurrence ledger\n")
    w("Every occurrence, in file order. Evidence longer than one line is shortened here and given in full in the next section and in `ground-truth.json`.\n")
    rows = []
    for o in occs:
        rows.append((o["id"], o["scenario"], f"`{o['role']}`", f"`{o['asset']}`" + (f" ^`{o['parent']}`" if o["parent"] else ""),
                     loc(o), loc(o, "end"), f"[{o['start']['charOffset']}, {o['end']['charOffset']})",
                     f"[{o['start']['byteOffset']}, {o['end']['byteOffset']})", o["length"]["chars"], o["nesting"],
                     f"`{o['scope']}`", code(o["symbol"]) if o["symbol"] else "-", f"`{o['library']}`",
                     ", ".join(f"`{p}`" for p in o["produces"]) or "-", ev(o["evidence"]), o["note"] or "-"))
    w(table(["ID", "Scn", "Role", "Asset (^parent)", "Start L:C", "End L:C", "Chars", "Bytes", "Len", "Nest", "Scope",
             "API symbol", "Library", "Produces", "Evidence", "Note"], rows) + "\n")
    multi = [o for o in occs if "\n" in o["evidence"]]
    if multi:
        w("## Full text of multi-line evidence\n")
        for o in multi:
            w(f"**{o['id']}** (`{o['asset']}`, {loc(o)} to {loc(o, 'end')}):\n")
            w("```text\n" + o["evidence"] + "\n```\n")
    w("## Non-asset mentions (negative ground truth)\n")
    w("Every case-insensitive match of the algorithm-name lexicon (see `_tooling/spec.py`, `DECOY_PATTERN`) that lies "
      "outside all occurrence spans. A scanner that reports any of these as a cryptographic asset produces a false positive.\n")
    rows = [(d["id"], f"{d['line']}:{d['column']}", f"[{d['byteOffset']}, {d['byteOffset'] + d['length']})",
             code(d["text"]), d["context"], ev(d["token"], 80), d["reason"]) for d in A["decoys"]]
    w(table(["ID", "L:C", "Bytes", "Match", "Context", "Containing token / line", "Why it is not an asset"], rows) + "\n")
    w("## Implicit and runtime-dependent cryptography\n")
    w("Behaviour that is fixed by the runtime or library rather than visible in the source. These are the places where "
      "source-level ground truth and the cryptography that actually executes can diverge.\n")
    w(table(["Asset", "What happens"], [(f"`{k}`", t) for k, t in lang.implicit]) + "\n")
    if lang.key == "java":
        w("Provider resolution observed on OpenJDK 25.0.4.1 with the default `java.security` (Bouncy Castle is used only "
          "through its lightweight API and is not registered as a JCA provider):\n")
        w(table(["Engine", "Algorithm", "Resolved provider"], VERIFY["java"]["providers"]) + "\n")
    if lang.key == "go":
        w(f"Default `crypto/tls` key-exchange preferences in Go 1.26: {VERIFY['go']['defaultCurves']}.\n")
    w("## Detection notes\n")
    w("Notes referenced from the ledger. Together they describe what makes each occurrence hard (or easy) to recognise statically.\n")
    w(table(["Note", "Explanation", "Occurrences"], [(f"`{k}`", A["notes_all"][k], ids(v_)) for k, v_ in A["notes_used"].items()]) + "\n")
    w("## Machine-readable files\n")
    w("`ground-truth.json` holds every field shown above, including the full evidence text of each span. `cbom.cdx.json` is "
      "a CycloneDX 1.6 BOM: one `library` component per library, one `cryptographic-asset` component per asset "
      "(with `evidence.occurrences`), library `provides` relations and algorithm `dependsOn` relations. Corpus-specific facts "
      "(NIST status, CNSA 2.0, implicit flags, provenance) are carried as `cbom-corpus:*` properties.\n")
    return "\n".join(L)


def ground_truth(A):
    lang = A["lang"]
    return OrderedDict([
        ("corpus", "cbom-ground-truth"), ("language", lang.title), ("file", lang.target), ("generated", GEN_TIME),
        ("conventions", OrderedDict(line="1-based", column="1-based Unicode code points", end="exclusive",
                                    charOffset="0-based code-point offset from file start", byteOffset="0-based UTF-8 byte offset from file start",
                                    cyclonedxOffset="column - 1")),
        ("verification", VERIFY[lang.key]),
        ("libraries", lang.libs),
        ("assets", [OrderedDict([("id", aid), ("kind", a["kind"]), ("bomRef", bom_ref(aid)), ("implicit", a["implicit"]),
                                 ("functions", a["functions"]),
                                 ("occurrences", [OrderedDict(id=oid, relation=rel) for oid, rel in a["occ"]]),
                                 ("properties", spec.ALGORITHMS.get(aid) or spec.MATERIALS.get(aid) or spec.CERTIFICATES.get(aid) or spec.PROTOCOLS.get(aid))])
                    for aid, a in A["assets"].items()]),
        ("occurrences", A["occs"]),
        ("nonAssetMentions", A["decoys"]),
        ("notes", OrderedDict((k, A["notes_all"][k]) for k in A["notes_used"])),
        ("runtimeNotes", [OrderedDict(asset=k, note=t) for k, t in lang.implicit]),
        ("expectedOutput", EXPECTED)])


def short(sym):
    if not sym:
        return "?"
    s = re.split(r"[:/]", sym)[-1]
    parts = s.split(".")
    return ".".join(parts[-2:]) if len(parts) > 1 else s


def root_readme(analyses):
    L = []
    w = L.append
    total_libs = sum(len(A["lang"].libs) for A in analyses)
    w("# CBOM ground-truth corpus: one cryptographic program in five languages\n")
    w("The same program is implemented in **Python, Java, Go, TypeScript and C#**. It runs 24 scenarios covering "
      "hashing, an XOF, MAC, KDFs and password hashing, AEAD and block-cipher modes, legacy ciphers, RSA, elliptic-curve "
      "signatures and key agreement, ML-KEM and ML-DSA, an X.509 certificate and a TLS 1.3 configuration, across "
      f"{total_libs} library components in total. Each language directory contains the program, its build manifest, and a "
      "README.md that records **every occurrence of every cryptographic asset** with exact coordinates, role, API symbol, "
      "library, scope, scenario and asset properties, plus a ground-truth CycloneDX 1.6 CBOM and a JSON ledger.\n")
    w("## Layout\n")
    w("```text\n" + "\n".join([
        ".",
        "├── README.md               this file",
        "├── expected_output.txt     stdout shared by all five programs",
        "├── Python/                 crypto_showcase.py, requirements.txt, README.md, cbom.cdx.json, ground-truth.json",
        "├── Java/                   src/main/java/corpus/CryptoShowcase.java, pom.xml, ...",
        "├── Go/                     main.go, go.mod, ...",
        "├── TypeScript/             src/main.ts, package.json, tsconfig.json, ...",
        "├── CSharp/                 Program.cs, CryptoShowcase.csproj, ...",
        "└── _tooling/               annotated templates and the generator that produced the ground truth",
    ]) + "\n```\n")
    w("`CSharp/` is spelled out because `#` breaks some shells, URLs and build tools. Scan the five language directories, "
      "not the archive root: `_tooling/templates` contains annotated copies of every program (with `.tmpl` extensions) "
      "and would double-count.\n")
    w("## Verified equivalence\n")
    w("All five programs were built and run; their standard output is byte-identical (31 lines, see `expected_output.txt`). "
      "Deterministic scenarios reproduce published test vectors: SHA-256/512, SHA3-256, BLAKE2b-512, MD5, SHA-1, SHAKE128 and "
      "HMAC-SHA256 of the 'quick brown fox' message, RFC 5869 A.1 (HKDF), RFC 7914 sections 11 and 12 (PBKDF2, scrypt), "
      "GCM test case 16 (AES-256-GCM), FIPS 197 C.1 (first AES-128-ECB block) and the RFC 8032 TEST 1 public key (Ed25519).\n")
    rows = []
    for A in analyses:
        lang = A["lang"]
        rows.append((lang.title, VERIFY[lang.key]["toolchain"], VERIFY[lang.key]["build"], VERIFY[lang.key]["result"]))
    w(table(["Language", "Toolchain", "How it was built and run", "Result"], rows) + "\n")
    w("## Corpus statistics\n")
    rows = []
    for A in analyses:
        lang = A["lang"]
        kinds = Counter(a["kind"] for a in A["assets"].values())
        rows.append((lang.title, f"`{lang.dir}/{lang.target}`", A["lines"], len(A["occs"]), kinds["algorithm"],
                     kinds["related-crypto-material"], sum(1 for a in A["assets"].values() if a["implicit"]),
                     len(lang.libs), len(A["decoys"])))
    w(table(["Language", "Program", "Lines", "Occurrences", "Algorithms", "Material", "Implicit assets", "Libraries",
             "Non-asset mentions"], rows) + "\n")
    w("## Scenarios and the APIs that implement them\n")
    w("Each cell lists the operations recorded for that scenario (library ID, then API). The logic is the same everywhere; "
      "the APIs, the libraries and the way algorithms are named are deliberately varied.\n")
    rows = []
    for sid, desc, det in spec.SCENARIOS:
        row = [f"**{sid}** {desc}"]
        for A in analyses:
            ops = [o for o in A["occs"] if o["scenario"] == sid and o["kind"] == "op"] or \
                  [o for o in A["occs"] if o["scenario"] == sid and o["kind"] in ("ctor", "cfg")]
            seen = OrderedDict()
            for o in ops:
                seen.setdefault(o["library"].replace("lib.", ""), OrderedDict())[short(o["symbol"])] = 1
            row.append("<br>".join(f"{lib}: " + ", ".join(code(x) for x in syms) for lib, syms in seen.items()))
        rows.append(row)
    w(table(["Scenario"] + [A["lang"].title for A in analyses], rows) + "\n")
    w("## How the ground truth was produced\n")
    w("Each program was written once as an annotated template in which every cryptographic span is wrapped in a marker "
      "carrying its role, asset, parent asset, produced material, API symbol and a note key "
      "(`«ROLE ASSET^PARENT>PRODUCED#SYMBOL!NOTE|code»`). `_tooling/build_sources.py` strips the markers to produce the "
      "delivered source and `_tooling/docs.py` computes positions on the stripped text, so coordinates are exact by "
      "construction rather than found by searching. Asset properties live in one shared registry (`_tooling/spec.py`), so "
      "the same asset ID means the same thing in every language. To change a program, edit its template and run "
      "`python3 build_sources.py && python3 docs.py` inside `_tooling/`.\n")
    w("## Caveats\n")
    w("- The build sandbox could not reach Maven Central, NuGet or the Go module proxy. Java was compiled and run against "
      "Bouncy Castle 1.86 built from the `r1rv86` source tag (and re-run against the 1.80 jars), C# against "
      "BouncyCastle.Cryptography 2.7.0 built from the `release-2.7.0` tag, and Go against x/crypto v0.58.0, CIRCL v1.6.5 and "
      "x/sys v0.49.0 from their tagged sources. `pom.xml` and `CryptoShowcase.csproj` pin those same versions but were not "
      "themselves exercised through Maven or NuGet.\n"
      "- `Go/` ships without `go.sum`; run `go mod tidy` once to record checksums.\n"
      "- Asset-level security levels and compliance statements (`_tooling/spec.py`) are analyst judgements with stated "
      "sources (FIPS, SP 800-131A Rev. 2, NIST IR 8547, CNSA 2.0); review them against your own policy baseline.\n"
      "- 'Implicit' assets (for example the TLS 1.3 cipher suites in Python and Go, or MGF1 in Go, TypeScript and C#) are part "
      "of the runtime CBOM but have no source occurrence by design.\n")
    return "\n".join(L)


def main():
    analyses = [analyse(lang) for lang in LANGS]
    for A in analyses:
        d = OUT / A["lang"].dir
        (d / "README.md").write_text(readme(A), encoding="utf-8")
        (d / "cbom.cdx.json").write_text(json.dumps(cbom(A), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (d / "ground-truth.json").write_text(json.dumps(ground_truth(A), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{A['lang'].key:11s} occurrences={len(A['occs'])} assets={len(A['assets'])} decoys={len(A['decoys'])}")
    (OUT / "README.md").write_text(root_readme(analyses), encoding="utf-8")


if __name__ == "__main__":
    main()
