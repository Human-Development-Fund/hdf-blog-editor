#!/usr/bin/env python3
"""Check common structural defects in HDF WordPress Code-view HTML."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path


class MarkupChecker(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.h2 = 0
        self.empty_h2 = 0
        self.images = 0
        self.images_missing_alt = 0
        self.images_in_heading = 0
        self.links_missing_href = 0
        self._heading_depth = 0
        self._h2_stack: list[bool] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if tag == "h1":
            self.h1 += 1
            self._heading_depth += 1
        elif tag == "h2":
            self.h2 += 1
            self._heading_depth += 1
            self._h2_stack.append(False)
        elif tag == "h3":
            self._heading_depth += 1
        elif tag == "img":
            self.images += 1
            if "alt" not in attrs_map or not (attrs_map.get("alt") or "").strip():
                self.images_missing_alt += 1
            if self._heading_depth:
                self.images_in_heading += 1
            if self._h2_stack:
                self._h2_stack[-1] = True
        elif tag == "a":
            href = (attrs_map.get("href") or "").strip()
            if not href:
                self.links_missing_href += 1

    def handle_data(self, data: str) -> None:
        if self._h2_stack and data.strip():
            self._h2_stack[-1] = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            if self._h2_stack and not self._h2_stack.pop():
                self.empty_h2 += 1
            self._heading_depth = max(0, self._heading_depth - 1)
        elif tag in {"h1", "h3"}:
            self._heading_depth = max(0, self._heading_depth - 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    source = args.html.read_text(encoding="utf-8")
    checker = MarkupChecker()
    checker.feed(source)

    chatgpt_markers = (
        "qMYqUG_convSearchResultHighlightRoot",
        "data-turn-id-container=",
        "data-message-author-role=",
        "data-testid=\"conversation-turn",
    )
    chatgpt_wrapper_markers = sum(source.count(marker) for marker in chatgpt_markers)
    chatgpt_tracking_links = source.count("utm_source=chatgpt.com")

    print(f"H1 elements: {checker.h1}")
    print(f"H2 elements: {checker.h2}")
    print(f"Empty H2 elements: {checker.empty_h2}")
    print(f"Images: {checker.images}")
    print(f"Images with empty/missing alt: {checker.images_missing_alt}")
    print(f"Images inside headings: {checker.images_in_heading}")
    print(f"Links with empty/missing href: {checker.links_missing_href}")
    print(f"ChatGPT wrapper markers: {chatgpt_wrapper_markers}")
    print(f"ChatGPT tracking parameters: {chatgpt_tracking_links}")

    defects = (
        checker.empty_h2
        + checker.images_in_heading
        + checker.links_missing_href
        + chatgpt_wrapper_markers
        + chatgpt_tracking_links
    )
    if checker.h1 > 1:
        defects += checker.h1 - 1
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
