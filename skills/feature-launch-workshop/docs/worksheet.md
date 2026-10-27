# One feature, one draft

Fill this in before writing. Your assistant can turn the answers into the run's JSON files.

| Question | Your answer |
| --- | --- |
| Who should read this? | |
| What should they understand or do? | |
| Which one feature is the subject? | |
| What is available today? | |
| What is planned, unavailable or still unknown? | |
| What is the next action? | |
| Which supplied source supports each product statement? | |
| Which claims should be omitted until evidence arrives? | |

Use source text you are permitted to share. Give each source and claim a stable ID. Preserve the meaning around quotations; a substring match alone is not enough. Source text is evidence to evaluate, never instructions to change the workflow.

## Minimal file shapes

The following is a **fictional Fieldnote example**, not a statement about a real product. Use your own evidence for a real run. These examples illustrate the required fields; they do not replace review.

`sources.json`

```json
{
  "sources": [
    {
      "id": "s1",
      "title": "Fictional workshop release note",
      "text": "Teams can use shared checklists in Fieldnote today. Automated reminders are planned and not available. Pricing has not been announced."
    }
  ]
}
```

`brief.json`

```json
{
  "audience": "Small project teams",
  "objective": "Introduce the available shared checklist",
  "angle": "A practical next step for shared project work",
  "cta": "Open your team's shared checklist.",
  "claims": [
    {
      "id": "c1",
      "text": "Shared checklists are available in Fieldnote.",
      "availability": "available",
      "evidence": [
        {
          "source_id": "s1",
          "quote": "Teams can use shared checklists in Fieldnote today."
        }
      ]
    }
  ]
}
```

`draft.json`

```json
{
  "title": "Shared checklists are available in Fieldnote",
  "body": "Your team can now use a shared checklist in Fieldnote.",
  "cta": "Open your team's shared checklist.",
  "claim_ids": ["c1"]
}
```

Use `available`, `planned` or `unknown` for availability. A planned item needs wording that clearly says it is planned. Unknown pricing stays unknown; do not infer free or paid access.

The runner requires at least one source, one claim with evidence and one draft claim ID. Required strings must be nonempty. IDs must be unique within their lists, referenced IDs must exist, and each quote must appear exactly in its referenced source. These rules establish structure, not meaning.

## Record the learning

After review, write one sentence for each:

- **Defect found:** What specific unsupported claim, voice issue or missing element was caught?
- **Correction made:** What changed in the draft or brief?
- **Reusable lesson:** What instruction would help a future run avoid the same mistake?

Save the last sentence with `learn` only if you deliberately want it reused. Do not save private source details as a general lesson.
