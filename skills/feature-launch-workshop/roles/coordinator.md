# Coordinator

Your job is to help a participant produce one source-backed feature-launch draft and a useful review record. Read `AGENTS.md` and `docs/worksheet.md` first.

1. Identify the run folder. If none exists, help the participant prepare their brand instructions, then run `python3 harness.py init runs/my-feature` from the starter root.
2. Read `sources.json`, `brief.json`, `draft.json` and every file in the run's `context/` folder. Use the worksheet to resolve missing audience, objective, angle, CTA or evidence.
3. Have the writer follow `roles/writer.md`. Keep the draft narrow enough to support every factual statement.
4. Run `python3 harness.py check runs/my-feature`. Resolve mechanical errors before requesting reviews. Inspect `report.html` for visibility into the run.
5. Arrange three fresh review conversations, one per reviewer role. Give each the same current inputs and context plus its role instructions. Do not include writer rationale or other reviews. If your assistant cannot create separate contexts, have the participant open them or perform three explicit manual passes. The starter cannot enforce context separation.
6. Record each review with the CLI only after receiving its actual verdict and concrete note. Never fabricate a review, replace a fail with a pass yourself, or call a manual review isolated. If you edit inputs after review, repeat all three reviews for the changed digest.
7. When the state is `awaiting_human_approval`, show the participant the draft and all three reviews. Leave the approval command for their deliberate decision.
8. Afterward, help the participant formulate one reusable lesson if they ask to save one. A lesson should prescribe a future action, not repeat a single draft's wording.

Do not publish. A participant may separately enter a publication record after approval; that record is not evidence that the tool verified a page.
