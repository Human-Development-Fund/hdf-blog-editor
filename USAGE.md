# Usage

## The simplest way to begin

Type:

> I would like to review the next blog.

Attach the full WordPress-page PDF or screenshot and the current Code/Text-view HTML. If the full capture does not show them, also attach the current Yoast results and featured-image details.

The skill should infer what to do. Users do not need to specify SEO fields, output sections or internal modes.

## Common requests

| What you need | What to say |
|---|---|
| Initial assessment | `Review this next blog post.` |
| Full improvement | `Improve the full post.` |
| SEO diagnosis | `Help me fix these Yoast warnings.` |
| WordPress guidance | `What should I enter in these fields?` |
| Image accessibility | `Write alt text for these images.` |
| Limited edit | `Only rewrite the introduction.` |
| No rewriting | `Do not change the content; just audit it.` |
| Final check | `Check this before I publish it.` |

## Review modes

- **Quick review:** Finds the material issues without silently rewriting the article.
- **Full retrofit:** Produces a polished `.md` handoff containing WordPress fields, a readable article preview, matching HTML, image guidance and implementation notes.
- **Focused edit:** Changes only the requested passage or concern.
- **Yoast troubleshooting:** Fixes real issues and identifies demonstrable false positives.
- **WordPress field help:** Supplies or maps only the requested fields.
- **Image accessibility:** Reviews visual purpose, alt text, captions, placement and unknown credits.
- **Fact and link check:** Separates confirmed, attributed, unverified and contradicted claims.
- **Pre-publication check:** Audits the final body and fields without an unsolicited rewrite.

## Evidence to provide

The strongest review bundle is:

1. Full WordPress editor PDF or screenshot.
2. Current Code/Text-view HTML.
3. Expanded Yoast SEO and Readability results.
4. Featured-image Media Library view or the original image.
5. Live URL when the post is already published.
6. Approved source material for statistics, quotations and program claims.
7. Intended primary action, if the post has one.

Partial material is acceptable. The assistant should begin safely and ask only for the next genuinely necessary item.

## Expected Full Retrofit format

A Full Retrofit should be delivered as a downloadable Markdown file containing:

1. Editorial direction.
2. WordPress fields.
3. Reader preview.
4. Matching WordPress HTML.
5. Image fields and exact placement.
6. Social fields.
7. Yoast and schema guidance.
8. WordPress implementation notes.
9. Material editorial decisions.
10. Confirmed facts and unresolved items.

## Model recommendations

Reviewed: **2026-08-05**. Review model guidance before every minor or major release.

Model names and availability change. Check the platform's model selector when the named option is unavailable.

### ChatGPT

- **Recommended default for Full Retrofits:** GPT-5.6 Sol at **High** reasoning.
- **Quick reviews and Yoast troubleshooting:** GPT-5.6 Sol at **Medium** reasoning.
- **Highest-stakes or unusually complex posts:** GPT-5.6 Sol **Pro**, when available.
- **Avoid for final publication copy:** Instant mode when a stronger reasoning option is available.

High is the practical quality-first default. Pro should be reserved for difficult posts with extensive evidence, disputed claims or unusually sensitive editorial judgment.

### Claude

- **Recommended default:** Claude Sonnet 5.
- **High-stakes final review:** Claude Opus 4.8.
- **Simple field mapping or mechanical checks:** Haiku may be sufficient, but it is not recommended for the final rewrite.

Use Sonnet for normal production work and Opus when the quality gain justifies the greater usage.

### Google Antigravity

- **Recommended default:** Gemini 3.6 Flash at **High**.
- **Quick field checks:** Gemini 3.6 Flash at **Medium**.
- **Alternative deep-reasoning comparison:** Gemini 3.1 Pro at **High**, if available.

Gemini 3.6 Flash is the preferred workhorse because Google positions it as the newer, more efficient knowledge-work and agentic model.

### Official model references

The recommendations above were checked against official platform guidance on 2026-08-05:

- [GPT-5.6 in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-5-6-in-chatgpt)
- [ChatGPT Skills](https://help.openai.com/en/articles/20001066)
- [Claude model configuration](https://support.claude.com/en/articles/11940350-claude-code-model-configuration)
- [Claude model and consumption guidance](https://support.claude.com/en/articles/14782391-claude-enterprise-consumption-guide)
- [Using custom Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Antigravity model availability](https://antigravity.google/docs/models?authuser=09)
- [Antigravity Skills codelab](https://codelabs.developers.google.com/getting-started-agy-ide)

When a named model is unavailable, use the strongest non-instant reasoning model the workspace permits for Full Retrofits. Faster or smaller models remain suitable for field mapping and simple structural checks, but not for final sensitive copy.

## Consistency practices

For the most reliable output:

- Start a fresh conversation for each blog.
- Use the same production skill version across the team.
- Attach the current WordPress content rather than an earlier draft.
- Keep factual confirmations in the same conversation as the retrofit.
- Do not ask the model to make every Yoast indicator green.
- Compare the Reader preview with the HTML before pasting.
- Have a human editor verify statistics, links, religious assertions, image rights and publication status.
- Record durable new HDF rules in the canonical skill, not only in conversation history.

## Final human check

Before publication, confirm:

- Facts and links are approved.
- The title and opening sound human rather than mechanically optimized.
- The published slug has not changed unintentionally.
- Images have accurate alt text and verified credits where required.
- The primary CTA is intentional.
- The visible preview matches the copy-ready HTML.
- Remaining Yoast warnings are either fixed or documented false positives.
