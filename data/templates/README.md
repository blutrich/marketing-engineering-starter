# Start a campaign folder

These files are blank working documents. The [Fieldnote example](../examples/fieldnote/README.md) shows one completed fictional set.

1. Copy this folder into `data/local/my-campaign/` from the repository root:

   ```sh
   mkdir -p data/local
   mkdir data/local/my-campaign
   cp -n data/templates/campaign-brief.md data/local/my-campaign/brief.md
   cp -n data/templates/source-register.md data/local/my-campaign/sources.md
   cp -n data/templates/content-draft.md data/local/my-campaign/draft.md
   cp -n data/templates/review.md data/local/my-campaign/review-facts.md
   cp -n data/templates/review.md data/local/my-campaign/review-voice.md
   cp -n data/templates/review.md data/local/my-campaign/review-completeness.md
   cp -n data/templates/handoff.md data/local/my-campaign/handoff.md
   cp -n data/templates/lesson.md data/local/my-campaign/lesson.md
   ```

2. Use a new campaign name for each run. The copy commands use `cp -n` to avoid overwriting existing files. Fill the root `brand/` guides, then the `{{UPPER_SNAKE_CASE}}` fields in `sources.md` and `brief.md`. Supply facts you are authorized to use. Write `unknown`, `none supplied` or `not applicable` with a reason where appropriate; never make up an answer just to fill a field. Leave draft, review and handoff decisions unfinished until those steps actually occur.
3. Complete `sources.md` and `brief.md` before `draft.md`. Their starting templates are [source-register.md](source-register.md), [campaign-brief.md](campaign-brief.md) and [content-draft.md](content-draft.md).
4. Keep a snapshot of the brand and source inputs alongside the draft. Record the draft/input versions in each `review-*.md` file. Each copy of the [review template](review.md) records only its named gate: facts, voice or completeness. Have facts, voice and completeness reviewed independently of the writer; pass only the draft, brief, sources and relevant rules, not the writer's justification.
5. Use [handoff.md](handoff.md) for the human's decision and any later publication evidence. Use [lesson.md](lesson.md) only when a real correction merits a reusable lesson.

`data/local/` is ignored by this repository's Git configuration. Verify that with `git check-ignore data/local/my-campaign/brief.md` before using sensitive material. Ignoring a path does not protect files already tracked or uploaded elsewhere. The public `brand/` folder is tracked; keep its contents suitable for sharing or use a separate private copy of the repo.

## Check the setup

From the repository root:

```sh
python3 hooks/check-setup.py --brief data/local/my-campaign/brief.md
```

Add `--visual` when the campaign includes visuals. This checks required files, readable/nonempty text and unresolved placeholder tokens. It does **not** verify facts, brand quality, approvals, links or publication.

## Version discipline

Use a unique revision label each time the draft or an input changes, or record a Git commit / file digest. Keep the reviewed copies. A review applies only to those recorded versions. Any change to the draft or inputs invalidates all three reviews and any prior approval; repeat all three and obtain a new human decision. This Markdown workflow does not detect edits or authenticate reviewers automatically. The separate executable workshop under `skills/feature-launch-workshop/` demonstrates mechanical version binding.
