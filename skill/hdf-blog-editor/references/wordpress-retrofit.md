# WordPress retrofit guide

## Field mapping

| Deliverable | WordPress location |
|---|---|
| Visible title | Large title field at the top |
| Slug | Permalink below the title |
| Focus keyphrase | Yoast SEO > Focus keyphrase |
| SEO title | Yoast SEO > Search appearance > SEO title |
| Meta description | Yoast SEO > Search appearance > Meta description |
| Category | Right sidebar > Categories |
| Tags | Right sidebar > Tags |
| Alt text | Image settings or Media > Library > Alt Text |
| Caption and credit | Media Library fields; follow HDF's credit convention |

## Common defects found in pilots

- Bold paragraphs used instead of real H2 headings.
- Empty H2 elements left around images.
- Images wrapped inside H2 elements.
- More than one H1.
- Raw internal URLs repeated throughout the article.
- Empty alt text on meaningful images.
- Featured images with filenames as titles and no credit record.
- Focus keyphrase and meta description copied from the previous post.
- Yoast counting template or generated images that editors cannot see.
- Yoast highlighting unrelated body fragments because its offsets do not match Classic Editor content.
- ChatGPT conversation wrappers copied around otherwise usable article HTML.
- `utm_source=chatgpt.com` left on links.
- Link text placed inside an `<a>` element with no working `href`.

## Yoast decision rule

Address a warning only when the underlying issue is real. Inspect Code view before changing prose.

Ignore a warning when:

- The exact keyphrase is demonstrably in the first paragraph or real H2 but Yoast highlights unrelated text.
- Yoast requests changing an established live slug.
- It counts theme or generated images as missing article alt text.
- It asks for unrelated outbound links.
- It requests mechanical transition words or marginal sentence changes that worsen the voice.

When the exact keyphrase is visibly present in the first paragraph or a real H2 and Yoast continues to flag it after updating, treat the warning as a Classic Editor mapping failure. Do not keep rewriting correct prose.

## Source hierarchy

Do not move details from a related HDF landing page into an article as confirmed facts. Say where the detail came from and request confirmation, or omit it.
