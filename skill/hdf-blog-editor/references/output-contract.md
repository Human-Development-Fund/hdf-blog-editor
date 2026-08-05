# Retrofit output contract

Start from `assets/full-retrofit-template.md` and return a polished Markdown artifact in that order. For a Full retrofit, save the artifact as a clearly named `.md` file by default and provide only a concise link and handoff summary in chat. Use inline delivery only when the user requests it or the result is a small focused edit.

Make the document easy to operate from WordPress:

- Use clear sections and compact field tables.
- Include a **Reader preview** that presents the complete revised article as readable Markdown before the HTML.
- Put publishable HTML in one copy-ready code block.
- Keep editor-only notes outside the HTML.
- Avoid repeating the same recommendation in several sections.
- Add a short editorial-direction note when it helps explain the human and strategic choices.
- Show meaningful inline images in the Reader preview when a confirmed source URL is available.
- Place each inline image in the HTML at its recommended story position, not merely in an image-notes section.
- State the image position explicitly in the implementation notes, including the heading and the paragraphs or elements it sits between.

## WordPress fields

- Recommended visible title.
- Existing slug and explicit keep/change action.
- Focus keyphrase.
- SEO title.
- Meta description.
- Category and up to five provisional tags.
- Primary CTA and confirmed URL, when applicable.

## Revised post

First provide the complete readable article under **Reader preview** using an H3 for the visible title and H4s for article sections, followed by links, lists, emphasis and inline images as needed. Then provide the same publishable article as clean WordPress HTML in one copy-ready code block, mapping the preview's H4 article headings to H2s. Use one H1 only when the title must be represented in the HTML artifact, descriptive H2s, restrained emphasis and descriptive links.

Do not place verification markers inside publishable copy unless the user explicitly wants inline placeholders.

## WordPress implementation

Keep editor-only instructions outside the article. Include only relevant items:

- Heading and HTML corrections.
- Link and CTA changes.
- Featured and inline image alt text, captions and unknown credits.
- Exact inline-image placement in both the Reader preview and HTML.
- Yoast or Schema settings.
- Facts needing confirmation.

## Change summary

List the material editorial decisions in roughly five to eight bullets. Explain important removals or preserved constraints.

## Pre-delivery gate

Before handing off a Full retrofit, confirm that:

- The Reader preview and WordPress HTML contain the same article, links, emphasis, headings and image placements.
- Every statistic, quote, name, location, capability, URL and religious assertion is approved, attributed or clearly flagged outside the publishable copy.
- No ChatGPT interface wrapper, `utm_source=chatgpt.com`, empty link target or copied metadata remains.
- The WordPress title is the only H1 unless the artifact specifically needs to show it.
- Meaningful images have descriptive alt text; decorative images use empty alt text.
- Published slugs remain unchanged unless a redirect plan is explicitly authorized.
- The final refinement check in `house-style.md` passes.
- `scripts/check_markup.py` passes against the copy-ready HTML, with any non-blocking image observations reviewed manually.
- `scripts/check_retrofit.py` passes against the finished Markdown deliverable.
