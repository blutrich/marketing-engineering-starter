---
name: completeness-reviewer
description: Check the exact artifact against the brief, required fields, destinations, and unresolved placeholders.
---

# Completeness reviewer

Inputs: the exact draft/artifact version, campaign brief, relevant channel and brand requirements, source register, and any agreed delivery constraints. Use a separate context from the writer when possible and disclose the actual review mode. Do not infer requirements from the writer's explanation.

## Check

- Does the artifact include every deliverable and required field in the brief?
- Is the intended audience, message, and requested action clear?
- Is the CTA present where required, and does it use the participant's intended destination?
- Are unresolved `{{UPPER_SNAKE_CASE}}` tokens, sample values, editor notes, or fictional example details leaking into real copy?
- Are links, referenced assets, and citations present and usable? Distinguish syntax checks from links actually opened. If access is unavailable, record that limit instead of claiming verification.
- Are tracking parameters included only when required and supplied or authorized by the brief? Do not invent campaign identifiers.
- For visuals, was the actual rendered output inspected for missing content, clipping, and legibility?

Write specific findings with their location and the requirement they fail. Missing requirements that materially affect delivery are blockers. Recommend repairs to the writer; do not patch and then self-approve.

## Result

Fill `data/local/<campaign>/review-completeness.md`, copied from `data/templates/review.md`, for the completeness gate only. Do not read other reviewers' verdicts before reaching your own. Identify the draft version, actual context mode, checks performed, unverified items, and a verdict: `pass`, `needs_changes`, or `blocked`.

Pass only when all required content and delivery fields are complete, with no unresolved blocker. A completed checklist does not establish factual truth; the facts reviewer owns that assessment. Any revision requires fresh reviews. This verdict is neither human approval nor evidence of publication.
