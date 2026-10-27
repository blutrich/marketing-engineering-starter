# Handoff — {{CAMPAIGN_ID}}

## Package

- Exact draft file and version: {{HANDOFF_DRAFT_VERSION}}
- Brief / source / brand versions: {{HANDOFF_INPUT_VERSIONS}}
- Current review record and verdicts: {{HANDOFF_REVIEW_RECORD}}
- Outstanding limitations or `none`: {{HANDOFF_LIMITATIONS}}

## Human decision

- Status (`pending`, `approved`, `changes_requested`, `rejected`): {{HUMAN_DECISION}}
- Actual approver and decision time, or `not yet decided`: {{HUMAN_DECISION_IDENTITY_AND_TIME}}
- Exact version and scope approved: {{HUMAN_APPROVAL_SCOPE}}
- Evidence of the decision: {{HUMAN_APPROVAL_EVIDENCE}}
- Conditions or requested changes: {{HUMAN_APPROVAL_CONDITIONS}}

Never fill an approval on the human's behalf. Any change to the draft or inputs invalidates all three reviews and any prior approval. Revised content must complete all three reviews and receive a new human decision.

## Publication — a separate action

- Status (`not_attempted`, `scheduled`, `published`, `failed`): {{PUBLICATION_STATUS}}
- Authorized publisher, channel and account: {{PUBLICATION_OWNER_AND_DESTINATION}}
- Authorization for the external action: {{PUBLICATION_AUTHORIZATION}}
- Actual publication timestamp or `not applicable`: {{PUBLICATION_TIME}}
- External URL / platform ID and how it was verified, or `none`: {{PUBLICATION_EVIDENCE}}

A draft, review, local file, scheduled job or approval is not proof of publication. Mark `published` only after the action succeeds and evidence is recorded.

## Follow-up

- Measurement owner, method and time window: {{HANDOFF_MEASUREMENT}}
- Results, or `not measured`: {{HANDOFF_RESULTS}}
- Learning to capture, or `none yet`: {{HANDOFF_LEARNING}}
