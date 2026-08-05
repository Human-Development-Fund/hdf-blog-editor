# HDF Blog Editor

HDF Blog Editor is a reusable editorial skill for reviewing and improving Human Development Fund WordPress posts. It protects approved facts and the human voice while handling SEO, Yoast, headings, links, images, alt text and publication handoff.

The same reviewed source is packaged for:

- ChatGPT Skills
- Claude Skills
- Google Antigravity

## Start here

1. Open the repository's **Releases** page.
2. Download the ZIP for your platform.
3. Follow [INSTALL.md](INSTALL.md).
4. Start with: **“I would like to review the next blog.”**

You do not need to understand SEO, HTML or skill files to use it.

## What it does

- Reviews an existing HDF post without rewriting it unless requested.
- Produces a full, human-centered retrofit when asked.
- Preserves confirmed facts and published slugs.
- Separates real SEO problems from Yoast false positives.
- Produces descriptive image alt text without keyword stuffing.
- Detects common WordPress markup problems and copied ChatGPT wrappers.
- Delivers Full Retrofits as a polished Markdown file containing a readable preview and matching WordPress HTML.

## What it does not do

- Invent statistics, quotes, partners, locations, religious guidance or program capabilities.
- Treat an HDF page as independent verification of a claim.
- Change a published URL merely to satisfy Yoast.
- Add donation requests to every post.
- Include an Excerpt field in the handoff.

## Documentation

- [Installation for ChatGPT, Claude and Antigravity](INSTALL.md)
- [Usage, inputs, modes and model recommendations](USAGE.md)
- [How to update, test and release](CONTRIBUTING.md)
- [Privacy and security guidance](SECURITY.md)
- [Support and troubleshooting](SUPPORT.md)
- [Release history](CHANGELOG.md)

## Repository structure

```text
hdf-blog-editor-release/
├── skill/hdf-blog-editor/       # Canonical source
├── adapters/antigravity/        # Platform-specific workflow
├── tools/release.py             # Validation and packaging
├── tests/fixtures/              # Consistency fixtures
├── dist/                        # Generated release ZIPs
├── README.md
├── INSTALL.md
├── USAGE.md
└── CONTRIBUTING.md
```

Do not edit files inside `dist/`. Change the canonical skill, run the release checks, and rebuild all packages.

## Current release

Version **1.0.0**.

The skill is an editorial assistant, not an authority for legal, safeguarding, religious or factual approval. HDF remains responsible for final publication decisions.
