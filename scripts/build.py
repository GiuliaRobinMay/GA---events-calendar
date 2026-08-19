#!/usr/bin/env python3
"""Build index.html and build/fragment.html from index.template.html + data/events.json.

Run from the repo root:  python3 scripts/build.py

- index.html          full standalone page (open directly in a browser)
- build/fragment.html the same page without the document shell, for publishing
                      as a claude.ai Artifact (the shell is added at publish time)
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLACEHOLDER = "__GA_DATA__"


def main() -> None:
    data_path = ROOT / "data" / "events.json"
    data = data_path.read_text(encoding="utf-8")
    obj = json.loads(data)  # fail loudly on malformed data

    for key in ("meta", "series", "instances"):
        if key not in obj:
            sys.exit(f"data/events.json is missing the '{key}' key")
    missing = sorted({r[0] for r in obj["instances"]} - set(obj["series"]))
    if missing:
        sys.exit(f"instances reference series ids missing from the series map: {missing}")
    if "</script>" in data:
        sys.exit("data must not contain '</script>'")

    template = (ROOT / "index.template.html").read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        sys.exit(f"index.template.html is missing the {PLACEHOLDER} placeholder")
    html = template.replace(PLACEHOLDER, data.strip())

    (ROOT / "index.html").write_text(html, encoding="utf-8")

    lines = html.split("\n")
    if not lines[0].startswith("<!doctype"):
        sys.exit("template line 1 must be the document shell prefix")
    if lines[-2:] != ["</html>", ""] and lines[-1] != "</html>":
        sys.exit("template must end with a bare </html> line")
    end = -2 if lines[-1] == "" else -1
    fragment = "\n".join(lines[1:end]) + "\n"
    build_dir = ROOT / "build"
    build_dir.mkdir(exist_ok=True)
    (build_dir / "fragment.html").write_text(fragment, encoding="utf-8")

    print(f"OK: {len(obj['instances'])} instances, {len(obj['series'])} series")
    print(f"  -> index.html ({len(html):,} bytes)")
    print(f"  -> build/fragment.html ({len(fragment):,} bytes)")


if __name__ == "__main__":
    main()
