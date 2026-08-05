# Cross-platform acceptance tests

Automated tests protect package structure and common HTML defects. A human acceptance pass protects editorial behavior across models and platforms.

## When to run

- Run all cases before every minor or major release.
- Run the affected cases before a patch release that changes behavior.
- Re-run all cases when the recommended model changes materially.

## Test matrix

Test the same candidate version in:

| Platform | Production model | Required result |
|---|---|---|
| ChatGPT | Recommended High-reasoning model in `USAGE.md` | Pass |
| Claude | Recommended Sonnet model in `USAGE.md` | Pass |
| Antigravity | Recommended High-effort Gemini model in `USAGE.md` | Pass |

An optional second pass with each platform's strongest model helps distinguish a skill problem from a model-capability problem.

## Procedure

1. Install the candidate ZIP in a fresh environment.
2. Start a new conversation.
3. Run every scenario in `tests/evals.json` using sanitized or synthetic material.
4. Record Pass, Fail or Not applicable for every `must` assertion.
5. For the Full Retrofit scenario, save the Markdown result and run:

   ```bash
   python3 scripts/check_retrofit.py result.md
   ```

6. Extract the HTML block to a file and run:

   ```bash
   python3 scripts/check_markup.py post.html
   ```

7. Compare the three platforms for material differences in facts, tone, fields, links and image guidance.

## Pass criteria

A release passes only when:

- Every safety and factual-integrity assertion passes on all supported platforms.
- The natural activation prompt selects Quick Review without demanding a technical brief.
- Full Retrofits follow the canonical section order and both validators pass.
- Reader Preview and WordPress HTML communicate the same article.
- No model invents facts, identities, credits, consent, links or religious guidance.
- Remaining differences are cosmetic and do not change the publication decision.

If one platform fails repeatedly, fix the canonical skill rather than adding a hidden manual workaround. Add a regression case before releasing.
