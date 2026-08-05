#!/usr/bin/env python3
"""Validate the structure of a completed HDF Full Retrofit Markdown file."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from check_markup import MarkupChecker


REQUIRED_SECTIONS = (
    "Editorial direction",
    "WordPress fields",
    "Reader preview",
    "Revised WordPress HTML",
    "Image fields and placement",
    "Social fields",
    "Yoast and schema settings",
    "WordPress implementation notes",
    "Editorial decisions",
    "Confirmed facts and unresolved items",
)

REQUIRED_FIELDS = (
    "Visible title",
    "Existing slug",
    "Slug action",
    "Focus keyphrase",
    "SEO title",
    "Meta description",
    "Category",
    "Tags",
    "Primary CTA",
    "CTA URL",
    "Social title",
    "Social description",
    "Social image",
)

PLACEHOLDERS = (
    "[Post title]",
    "[Briefly explain",
    "[Title]",
    "[slug]",
    "[Keep or change",
    "[Keyphrase]",
    "[SEO title]",
    "[Meta description]",
    "[Category]",
    "[Up to five",
    "[CTA or None]",
    "[Confirmed URL",
    "[Visible title]",
    "[Complete readable",
    "[Complete matching",
    "[Alt text",
    "[Confirmed image",
    "[Only relevant",
    "[Material decision",
    "[Confirmed fact",
)


def normalize_heading(value: str) -> str:
    value = re.sub(r"[*_`]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip().casefold()


class HeadingCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._current: str | None = None
        self._parts: list[str] = []
        self.h2: list[str] = []
        self.links: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h2":
            self._current = tag
            self._parts = []
        if tag == "a":
            href = (dict(attrs).get("href") or "").strip()
            if href:
                self.links.append(href)

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._current:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == self._current:
            self.h2.append(normalize_heading("".join(self._parts)))
            self._current = None
            self._parts = []


def validate(source: str) -> list[str]:
    problems: list[str] = []

    if not re.search(r"^# HDF Blog Retrofit:\s*\S", source, re.MULTILINE):
        problems.append("The document needs a completed '# HDF Blog Retrofit: …' title.")

    level_two = re.findall(r"^##[ \t]+(.+?)[ \t]*$", source, re.MULTILINE)
    if tuple(level_two) != REQUIRED_SECTIONS:
        problems.append(
            "H2 sections are missing, renamed, duplicated or out of order. "
            f"Expected: {', '.join(REQUIRED_SECTIONS)}."
        )

    lower = source.casefold()
    for field in REQUIRED_FIELDS:
        match = re.search(
            rf"\|\s*{re.escape(field)}\s*\|\s*([^|\n]*?)\s*\|",
            source,
            re.IGNORECASE,
        )
        if not match:
            problems.append(f"Missing WordPress field row: {field}.")
        elif not match.group(1).strip():
            problems.append(f"WordPress field has no value: {field}.")

    for placeholder in PLACEHOLDERS:
        if placeholder.casefold() in lower:
            problems.append(f"Unresolved template placeholder: {placeholder}.")

    html_blocks = re.findall(r"^```html[ \t]*\n(.*?)^```[ \t]*$", source, re.MULTILINE | re.DOTALL)
    if len(html_blocks) != 1:
        problems.append("The deliverable must contain exactly one non-empty ```html code block.")
        return problems

    html = html_blocks[0].strip()
    if not html:
        problems.append("The WordPress HTML code block is empty.")
        return problems

    markup = MarkupChecker()
    markup.feed(html)
    if markup.h1 > 1:
        problems.append("The WordPress HTML contains more than one H1.")
    if markup.empty_h2:
        problems.append("The WordPress HTML contains an empty H2.")
    if markup.images_in_heading:
        problems.append("The WordPress HTML contains an image inside a heading.")
    if markup.links_missing_href:
        problems.append("The WordPress HTML contains a link with no usable href.")
    if any(
        marker in html
        for marker in (
            "qMYqUG_convSearchResultHighlightRoot",
            "data-turn-id-container=",
            "data-message-author-role=",
            'data-testid="conversation-turn',
            "utm_source=chatgpt.com",
        )
    ):
        problems.append("The WordPress HTML contains copied ChatGPT interface or tracking markup.")

    preview_match = re.search(
        r"^## Reader preview[ \t]*\n(.*?)^## Revised WordPress HTML[ \t]*$",
        source,
        re.MULTILINE | re.DOTALL,
    )
    if not preview_match or not preview_match.group(1).strip():
        problems.append("The Reader preview is empty or cannot be located.")
    else:
        preview = preview_match.group(1)
        preview_titles = re.findall(r"^###[ \t]+(.+?)[ \t]*$", preview, re.MULTILINE)
        if len(preview_titles) != 1:
            problems.append("The Reader preview must contain exactly one H3 visible title.")
        preview_sections = [
            normalize_heading(item)
            for item in re.findall(r"^####[ \t]+(.+?)[ \t]*$", preview, re.MULTILINE)
        ]
        html_headings = HeadingCollector()
        html_headings.feed(html)
        if preview_sections != html_headings.h2:
            problems.append(
                "Reader-preview H4 headings do not match the WordPress HTML H2 headings in wording and order."
            )

        preview_body = re.sub(r"^###[ \t]+.+?[ \t]*$", "", preview, count=1, flags=re.MULTILINE)
        preview_body = re.sub(r"!\[[^\]]*\]\([^\n)]*\)", " ", preview_body)
        preview_links = re.findall(r"(?<!!)\[[^\]]+\]\(([^\n)]+)\)", preview_body)
        preview_body = re.sub(r"(?<!!)\[([^\]]+)\]\([^\n)]*\)", r"\1", preview_body)
        preview_body = re.sub(r"<[^>]+>", " ", preview_body)

        html_body = re.sub(r"<h1\b[^>]*>.*?</h1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
        visible_html = HeadingCollector()
        visible_html.feed(html_body)
        preview_words = re.findall(r"\w+(?:[’']\w+)?", preview_body.casefold())
        html_words = re.findall(r"\w+(?:[’']\w+)?", " ".join(visible_html.text).casefold())
        if preview_words != html_words:
            problems.append("Reader-preview text does not match the visible text in the WordPress HTML.")
        if Counter(item.strip() for item in preview_links) != Counter(visible_html.links):
            problems.append("Reader-preview links do not match the WordPress HTML links.")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    source = args.markdown.read_text(encoding="utf-8")
    problems = validate(source)
    if problems:
        print("Full Retrofit validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("Full Retrofit structure passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
