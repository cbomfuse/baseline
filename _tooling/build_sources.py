"""Strip ground-truth markers from the annotated templates and lay out the corpus."""
import re
import shutil
import sys
from pathlib import Path

import markers
from languages import LANGS, BY_KEY

TOOLING = Path(__file__).resolve().parent
OUT = TOOLING.parent if TOOLING.name == "_tooling" else TOOLING.parent / "out" / "crypto-corpus"


def load_template(lang):
    text = (TOOLING / "templates" / lang.key / lang.template).read_text(encoding="utf-8")
    if lang.tabs:  # gofmt: indentation with tabs
        text = "\n".join(re.sub(r"^((?:    )+)", lambda m: "\t" * (len(m.group(1)) // 4), line)
                         for line in text.split("\n"))
    return text


def build(lang):
    text, spans = markers.parse(load_template(lang), lang.template)
    dest = OUT / lang.dir
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / lang.target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    static = TOOLING / "templates" / lang.key / "static"
    if static.exists():
        for item in static.rglob("*"):
            if item.is_file():
                rel = item.relative_to(static)
                (dest / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(item, dest / rel)
    return text, spans


if __name__ == "__main__":
    keys = sys.argv[1:] or [lang.key for lang in LANGS]
    for key in keys:
        text, spans = build(BY_KEY[key])
        print(f"{key}: {len(text.splitlines())} lines, {len(spans)} markers")
