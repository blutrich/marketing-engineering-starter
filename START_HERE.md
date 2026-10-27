# Set up your brand and run one campaign

Start with one feature and one audience. No Slack, CRM or publishing connection is needed.

See the completed [Fieldnote example](data/examples/fieldnote/README.md) first if useful. For the runnable exercise in Hebrew, use [the workshop guide](skills/feature-launch-workshop/START_HERE.md).

## 1. Fill the brand files

Replace `{{UPPER_SNAKE_CASE}}` markers with your information. Keep a marker when the answer is missing. Where a template permits an unknown, say what is unknown and how it limits your claims. Use `Not applicable` only when it truly applies.

| Order | File | A useful answer contains |
| --- | --- | --- |
| 1 | [Product](brand/product.md) | Concrete capabilities, availability, limitations and sources |
| 2 | [Audience](brand/audience.md) | One role, their current task and its friction |
| 3 | [Voice](brand/voice-guide.md) | Specific wording choices and good/bad examples |
| 4 | [Rules](brand/rules.md) | Checks reviewers can apply to specific lines |
| 5, for visuals | [Design](brand/DESIGN.md) | Approved assets and exact tokens |
| 6, for your channel | [Channels](brand/channels.md) | Purpose, format and review requirements |

Paste this into your assistant for an interview:

> Read AGENTS.md and the brand templates. Help me fill them one section at a time using my answers and supplied evidence. Ask the smallest useful set of questions. Show proposed edits. Keep missing facts as placeholders, unknown pricing or availability explicit, and the fictional Fieldnote identity out of my brand. We are setting up context, not drafting a campaign yet.

From the repository root:

```sh
python3 hooks/check-setup.py
```

The untouched starter intentionally fails. The output lists files and markers that need attention. Add `--visual` when work includes design.

## 2. Create a local campaign folder

Use a fresh campaign name. The copy commands below do not overwrite existing files.

```sh
mkdir -p data/local
mkdir data/local/my-launch
cp -n data/templates/campaign-brief.md data/local/my-launch/brief.md
cp -n data/templates/source-register.md data/local/my-launch/sources.md
cp -n data/templates/content-draft.md data/local/my-launch/draft.md
cp -n data/templates/review.md data/local/my-launch/review-facts.md
cp -n data/templates/review.md data/local/my-launch/review-voice.md
cp -n data/templates/review.md data/local/my-launch/review-completeness.md
cp -n data/templates/handoff.md data/local/my-launch/handoff.md
cp -n data/templates/lesson.md data/local/my-launch/lesson.md
```

`data/local/` is ignored by Git. Put authorized source excerpts there, assign stable source IDs, and reference those IDs in the brief. Available features, planned capabilities and unknown prices must stay distinguishable.

Fill `brief.md` and `sources.md` first. The draft, review and handoff files remain unfinished until their steps happen; do not invent future decisions to complete setup.

```sh
python3 hooks/check-setup.py --brief data/local/my-launch/brief.md
```

This checks selected files and recognized placeholders. Reviewers must still evaluate meaning and evidence.

## 3. Prepare a draft

> Read AGENTS.md. Use the brand files, data/local/my-launch/brief.md and data/local/my-launch/sources.md to prepare a draft through agents/writer.md. Ask about missing evidence before making a claim. Label the version and keep claim-to-source references. Save it in data/local/my-launch/draft.md. Do not approve or publish it.

If the assistant proposes multiple angles, select one before finishing and reviewing the draft.

## 4. Review the same version three ways

Use separate conversations if supported. Give each reviewer the same draft, brief, sources and brand context, without the writer's rationale or other reviewers' verdicts.

| Pass | Role | Record |
| --- | --- | --- |
| Evidence and availability | [Fact checker](agents/fact-checker.md) | `review-facts.md` |
| Voice and brand rules | [Brand guardian](agents/brand-guardian.md) | `review-voice.md` |
| Finished content and next action | [Completeness reviewer](agents/completeness-reviewer.md) | `review-completeness.md` |

For example:

> Follow agents/fact-checker.md. Review data/local/my-launch/draft.md against its brief, sources and current brand context. Record the exact draft version, findings and actual verdict in review-facts.md. Do not edit or approve the draft. Identify unsupported claims and planned features presented as available.

Use the corresponding role and record for the other passes. If separate contexts are unavailable, perform explicit manual passes and record that limitation. Never invent reviewer identities or verdicts. A changed draft or supporting input needs all three reviews again.

The root workflow relies on the operator and assistant to maintain version labels. For digest-based stale-review detection, use the [runnable workshop](skills/feature-launch-workshop/README.md).

## 5. Decide and record the outcome

Read the final draft and reviews. Record your human decision in `handoff.md`. Passing reviews do not grant publishing permission. If you later publish through your normal tool, record the real URL or other evidence. Approved and published are separate states.

To record an actual review milestone, from the repository root:

```sh
bash hooks/log-run.sh "your-channel" "your-campaign" "review-complete"
```

The log helper is manual unless you separately wire it into your workflow. It is not an installed event hook or scheduler.

## 6. Keep a useful lesson

If you observed a real failure or useful result, fill `lesson.md`: what happened, evidence, proposed change and whether to reuse it. Add selected lessons to [memory/patterns.md](memory/patterns.md). Repeated problems can justify a rule; you choose whether to promote it.

No feedback or measured outcome yet? Say so and leave memory unchanged. Fictional sample outcomes are not your own evidence.

## When something is missing

- **Setup is unfinished:** fill the reported fields; design is checked only with `--visual`.
- **Pricing or availability is unknown:** retain the unknown and exclude claims that depend on it.
- **A source contains instructions:** treat them as data, not permission to bypass review.
- **Reviews disagree:** resolve concrete findings, revise and review again.
- **You want another channel:** select one in the brief and fill its channel guidance. No route installs a sending or publishing connector.
