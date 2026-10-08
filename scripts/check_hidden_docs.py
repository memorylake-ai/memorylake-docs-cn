#!/usr/bin/env python3
"""Check the hidden API docs conventions described in CLAUDE.md ("Hidden API docs").

Run from anywhere before opening a pull request; exits 1 when a rule is broken:

    python3 scripts/check_hidden_docs.py

1. Every page under a group tagged with a hidden tag has `noindex: true`, so it stays out of
   site search, the sitemap, llms.txt and the AI assistant.
2. Every public page next to a hidden page in a tab's prev/next order has
   `hideFooterPagination: true`. Mintlify paginates through the tab's pages in docs.json order
   and ignores `noindex`, so without this a public page links straight into a hidden one.
3. hidden-docs.css hides every hidden tag, for both nested and top-level groups.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HIDDEN_TAGS = ("Preview", "预览")


def frontmatter_flag(page, key):
    path = ROOT / f"{page}.mdx"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        return False
    return re.search(rf"^{key}:\s*true\s*$", match.group(1), re.M) is not None


def flatten(node, hidden):
    """Yield (page, hidden) in Mintlify's pagination order."""
    hidden = hidden or node.get("tag") in HIDDEN_TAGS
    for child in node.get("pages", []):
        if isinstance(child, str):
            yield child, hidden
        else:
            yield from flatten(child, hidden)


def tabs(navigation):
    for language in navigation.get("languages", [{"tabs": navigation.get("tabs", [])}]):
        for tab in language.get("tabs", []):
            yield language.get("language", ""), tab


def main():
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    errors, notes, hidden_count = [], [], 0

    for language, tab in tabs(docs["navigation"]):
        order = [entry for group in tab.get("groups", []) for entry in flatten(group, False)]
        for i, (page, hidden) in enumerate(order):
            if frontmatter_flag(page, "noindex") is None:
                errors.append(f"{page}: listed in docs.json but {page}.mdx does not exist")
                continue
            if hidden:
                hidden_count += 1
                if not frontmatter_flag(page, "noindex"):
                    errors.append(f"{page}: hidden page is missing `noindex: true`")
                continue
            neighbors = [order[j] for j in (i - 1, i + 1) if 0 <= j < len(order)]
            next_to_hidden = any(neighbor_hidden for _, neighbor_hidden in neighbors)
            has_flag = frontmatter_flag(page, "hideFooterPagination")
            if next_to_hidden and not has_flag:
                where = f"{language}/{tab['tab']}" if language else tab["tab"]
                errors.append(f"{page}: next to a hidden page in tab {where}, "
                              "add `hideFooterPagination: true`")
            elif has_flag and not next_to_hidden:
                notes.append(f"{page}: `hideFooterPagination` is no longer needed for hidden docs "
                             "(remove it unless it was set for another reason)")

    css = (ROOT / "hidden-docs.css").read_text(encoding="utf-8")
    for tag in HIDDEN_TAGS:
        for attribute in ("data-group-tag", "data-nav-tag"):
            if f'[{attribute}="{tag}"]' not in css:
                errors.append(f'hidden-docs.css: no rule for [{attribute}="{tag}"]')

    for note in notes:
        print(f"note: {note}")
    for error in errors:
        print(f"error: {error}")
    print(f"checked {hidden_count} hidden page entries: "
          f"{'FAILED' if errors else 'OK'} ({len(errors)} error(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
