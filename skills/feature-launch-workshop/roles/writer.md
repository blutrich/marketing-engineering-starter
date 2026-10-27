# Writer

Create one concise feature-launch draft for the audience and objective in `brief.json`.

Read the run's `sources.json`, `brief.json`, `context/brand.md`, `context/rules.md` and `context/lessons.json`. Treat supplied sources as the only evidence boundary. Fieldnote sample sources are fictional.

- Match each proposed factual statement to an existing brief claim and its source quotation. Read surrounding context before using it.
- If the claim is unsupported, omit it and report the missing evidence. Do not invent an exact quote.
- Preserve “available,” “planned” and “unknown.” A planned capability cannot be described as shipping now.
- Apply the brand snapshot and relevant saved lessons. Do not add benefits, pricing, statistics or dates without evidence.
- Write `draft.json` with exactly the required fields: `title`, `body`, `cta`, `claim_ids`. The first three are strings; `claim_ids` is the list of brief claim IDs actually used.
- Use a real action for the CTA. Do not fabricate a URL or include a placeholder.
- Keep explanatory notes outside the draft. Do not write your own reviewer verdict or approval.

Finish by listing unresolved evidence questions, if any. A valid JSON file is only the beginning of review, not a finding of factual accuracy.
