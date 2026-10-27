# Marketing Engineering — Starter

A personal, forkable starter by Ofer Blutrich for building a marketing workflow with an AI assistant. Fill in your product, audience, brand and evidence; use separate reviews before deciding whether to publish.

**Start here:** [setup and first campaign](START_HERE.md) · [templates](data/templates/README.md) · [completed fictional example](data/examples/fieldnote/README.md) · [Hebrew workshop guide](skills/feature-launch-workshop/START_HERE.md)

## Choose what to try

| Your goal | Start with | What runs |
| --- | --- | --- |
| Adapt the starter to your own brand | [START_HERE.md](START_HERE.md) | Your assistant follows role instructions; you arrange reviews and make the final decision |
| See a completed example | [Fieldnote](data/examples/fieldnote/README.md) | Read-only fictional files; no account or setup needed |
| Run a mistake → correction → review demo | [Workshop](skills/feature-launch-workshop/README.md) | A Python runner replays fictional fixtures and generates an HTML report |

Role files are instructions, not automatic enforcement. The setup checker checks missing files and unfilled placeholders. The workshop runner separately tracks version-bound reviews and approvals. Neither Python tool calls a model or publishes content.

## Quick start

```sh
git clone https://github.com/blutrich/marketing-engineering-starter.git
cd marketing-engineering-starter
python3 hooks/check-setup.py
```

**The first check should report unfinished setup.** The repository deliberately ships with `{{PLACEHOLDERS}}`. Follow the file and token names in its output, or open the folder in your AI coding assistant and paste:

> Read AGENTS.md and START_HERE.md. Help me fill the brand templates from information I provide. Ask about missing product facts, audience and voice; do not invent them or borrow the fictional example's facts. Keep unresolved fields visible. Then help me prepare one campaign in data/local/my-launch using the templates. Run the setup check and stop before drafting if required inputs are missing.

Python 3.10+ is needed for the checks and workshop, with no dependencies to install. You can read and fill the Markdown templates without Python. Your chosen assistant's account or API access is separate.

## What to fill in

| File | What you provide | Required for |
| --- | --- | --- |
| [Product](brand/product.md) | Capabilities, availability, evidence, pricing and limitations | Every real draft |
| [Audience](brand/audience.md) | One audience, their task, friction, language and objections | Every real draft |
| [Voice](brand/voice-guide.md) | Vocabulary and examples of acceptable wording | Every real draft |
| [Rules](brand/rules.md) | Checks reviewers can apply to specific lines | Every real draft |
| [Design](brand/DESIGN.md) | Approved colors, fonts, logo assets and visual rules | Visual work |
| [Channels](brand/channels.md) | Purpose and format choices | Your chosen channel |

Use [the template index](data/templates/README.md) for a campaign brief, source register, draft, three review records, handoff and optional lesson. Keep internal sources and runs in `data/local/`, which is ignored by Git. Review changes before pushing customized brand files to a public repository.

## One campaign, end to end

1. **Collect evidence.** Separate available capabilities, plans and unknowns.
2. **Agree on a brief.** Choose one audience, message, channel, CTA and success measure.
3. **Write.** The [writer](agents/writer.md) uses the brief, sources and brand files.
4. **Review separately.** [Facts](agents/fact-checker.md), [voice](agents/brand-guardian.md) and [completeness](agents/completeness-reviewer.md) each produce a verdict on the same version. Changes require fresh reviews.
5. **Make a human decision.** Record whether this exact draft is approved. Publishing is a separate action.
6. **Keep a useful lesson.** Record observed feedback and choose explicitly whether to reuse it. No feedback means no invented learning.

The [Fieldnote example](data/examples/fieldnote/README.md) uses fictional product facts and illustrative reviews, not live agent or human approval.

## The four layers

| Layer | Where it lives | What it does here |
| --- | --- | --- |
| Brain | `brand/`, `agents/`, `skills/` | Supplies context and role instructions |
| Visibility | Review and handoff files; local `activity-log.md` | Records checks, decisions and publication evidence when available |
| Movement | `hooks/log-run.sh`; workshop runner | Local operations invoked by the operator; no installed scheduler or external connector |
| Memory | `memory/` and campaign lessons | Stores feedback selected for reuse, without retraining a model |

## Check your setup

From the repository root:

```sh
# Required brand files
python3 hooks/check-setup.py

# Also check visual guidance
python3 hooks/check-setup.py --visual

# Include a campaign brief you have prepared
python3 hooks/check-setup.py --brief data/local/my-launch/brief.md

# A completed fictional fixture passes the same checks
python3 hooks/check-setup.py --root data/examples/fieldnote --visual --brief campaign-brief.md

# Tests for the setup checker
python3 -m unittest discover -s hooks -p 'test_*.py' -v
```

A successful check means selected files are present, nonempty and free of recognized placeholders. It does not verify claims, evidence quality, brand fit or approval.

## Runnable workshop

The workshop is a separate exercise with its own configuration. Root `brand/` edits do not automatically configure it.

```sh
cd skills/feature-launch-workshop
python3 harness.py demo --out runs/demo
```

Open `runs/demo/report.html`. The fictional replay stops at `awaiting_human_approval`; review outcomes are supplied fixtures. For a real exercise, open the workshop directory in your assistant and follow [its guide](skills/feature-launch-workshop/README.md).

## License and attribution

[MIT](LICENSE). This is Ofer Blutrich's independent educational starter, not an official Base44 distribution. It contains generic templates and fictional examples. See the workshop's [notice](skills/feature-launch-workshop/NOTICE.md) for its inspiration and scope.
