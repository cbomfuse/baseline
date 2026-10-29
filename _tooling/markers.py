"""Parse annotated templates.

Marker grammar (never present in the delivered sources):

    «ROLE ASSET[^PARENT][>PRODUCED,...][#SYMBOL][!NOTE]|CODE»

* ROLE      kind[:qualifier], e.g. op:encrypt, prm:iterations, alg, imp
* ASSET     asset id (spec.py) or library id (languages.py)
* ^PARENT   composite asset this identifier parameterises (e.g. sha-256^hkdf-sha256)
* >PRODUCED material asset(s) whose value is produced at this location
* #SYMBOL   fully-qualified API symbol
* !NOTE     note key (resolved per language) or free text
* CODE      exact source text; may contain nested markers

Positions are computed on the stripped output:
  line / column      : 1-based, column counted in Unicode code points
  byte offsets       : 0-based UTF-8 offsets into the file, end exclusive
"""
import re

OPEN, CLOSE = "\u00ab", "\u00bb"
META_RE = re.compile(
    r"^(?P<role>[a-z]+(?::[A-Za-z0-9_.-]+)?)\s+(?P<asset>[^\^>#!]+?)"
    r"(?:\^(?P<parent>[^>#!]+))?(?:>(?P<prod>[^#!]+))?(?:#(?P<sym>[^!]+))?(?:!(?P<note>.+))?$")


class MarkerError(Exception):
    pass


def parse(template: str, filename: str):
    out = []
    stack = []
    spans = []
    i, n = 0, len(template)
    out_len = 0
    while i < n:
        ch = template[i]
        if ch == OPEN:
            bar = template.find("|", i)
            if bar < 0:
                raise MarkerError(f"{filename}: unterminated marker meta at {i}")
            meta = template[i + 1:bar]
            if OPEN in meta or CLOSE in meta or "\n" in meta:
                raise MarkerError(f"{filename}: malformed meta {meta!r}")
            m = META_RE.match(meta.strip())
            if not m:
                raise MarkerError(f"{filename}: cannot parse meta {meta!r}")
            stack.append((m.groupdict(), out_len, meta))
            i = bar + 1
            continue
        if ch == CLOSE:
            if not stack:
                raise MarkerError(f"{filename}: unbalanced close at {i}")
            meta, start, raw = stack.pop()
            spans.append(dict(meta=meta, start=start, end=out_len, raw=raw, depth=len(stack)))
            i += 1
            continue
        out.append(ch)
        out_len += 1
        i += 1
    if stack:
        raise MarkerError(f"{filename}: {len(stack)} unclosed marker(s): {[s[2] for s in stack]}")
    text = "".join(out)
    return text, sorted(spans, key=lambda s: (s["start"], -s["end"], s["depth"]))


def positions(text: str):
    """Return a function mapping a char offset to (line, col, byte_offset)."""
    line_starts = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(idx + 1)
    # prefix byte counts per char for exact UTF-8 offsets
    byte_prefix = [0] * (len(text) + 1)
    acc = 0
    for idx, ch in enumerate(text):
        byte_prefix[idx] = acc
        acc += len(ch.encode("utf-8"))
    byte_prefix[len(text)] = acc

    import bisect

    def pos(offset: int):
        li = bisect.bisect_right(line_starts, offset) - 1
        return li + 1, offset - line_starts[li] + 1, byte_prefix[offset]

    return pos
