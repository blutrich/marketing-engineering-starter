# Review record — {{CAMPAIGN_ID}}

Copy this template to `review-facts.md`, `review-voice.md` and `review-completeness.md`. Each reviewer fills one file for its named gate; it is not a combined self-review.

## Scope and versions

- Gate (`facts`, `voice` or `completeness`): {{REVIEW_GATE}}
- Draft file and exact revision: {{REVIEWED_DRAFT_PATH_AND_VERSION}}
- Brief / sources / brand snapshots: {{REVIEWED_INPUT_VERSIONS}}
- Version identifier method and retained copy locations: {{VERSION_RECORD_METHOD}}
- Reviewer, date and whether it used a fresh context: {{REVIEWER_AND_CONTEXT}}

The writer does not act as their own reviewer. Pass the draft and relevant inputs without the writer's rationale. Record actual identity and context separation; do not assert isolation that did not occur. These manual records are not authenticated or automatically enforced.

## Criteria for this gate

Use the row matching this file; the other two belong to separate reviewers.

| Gate | What the review must establish |
|---|---|
| facts | Every claim maps to exact source support; availability, scope and unknowns are preserved. Quote any unsupported wording. |
| voice | Each applicable numbered brand rule is met; cite exact draft text and rule IDs for failures. A pass requires at least 9/10 and no rule violations; a score never overrides a failed criterion. |
| completeness | All brief deliverables, CTA, destination, required assets and disclosures are present; no unresolved placeholders. Record actual link-check results and limitations. |

- Rule IDs / claims / brief requirements checked: {{REVIEW_CRITERIA_CHECKED}}
- Findings with exact draft wording and evidence: {{REVIEW_FINDINGS}}
- Required changes or `none`: {{REVIEW_REQUIRED_CHANGES}}
- Limitations and unresolved evidence or `none`: {{REVIEW_LIMITATIONS}}
- Voice score out of 10; use `not applicable` for the other gates: {{REVIEW_VOICE_SCORE}}
- Verdict (`pass`, `needs_changes`, `blocked`): {{REVIEW_VERDICT}}

## Handoff to the coordinator

- Findings owner and next action: {{REVIEW_NEXT_ACTION}}
- If this is a revision, previous verdict and what changed: {{REVIEW_REVISION_HISTORY}}

The coordinator checks all three separate files refer to the current draft and input versions. Any failed, missing or stale review prevents proceeding. Any change to the draft or inputs invalidates **all three reviews and any prior human approval**. Repeat all three against the new version and obtain a new human decision. Three current passing reviews permit presenting the exact version for that decision in `handoff.md`; they do not authorize publication.
