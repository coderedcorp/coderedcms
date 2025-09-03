"""
Utility to minify JavaScript.
Run this after modifiying JavaScript files, before committing.
"""

from pathlib import Path

from jsmin import jsmin


JSDIR = Path("coderedcms") / "static" / "coderedcms" / "js"

# iterate directory
for entry in JSDIR.iterdir():
    if entry.is_file() and entry.suffixes == [".js"]:
        print(f"Minifying {entry}")
        minified = ""
        with open(entry, "r", encoding="utf8") as f:
            minified = jsmin(f.read())
        newpath = entry.parent / (entry.stem + ".min.js")
        with open(newpath, "w", encoding="utf8", newline="\n") as f:
            f.write(minified)
