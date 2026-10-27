# Marketing Engineering — Starter

**The 4-layer AI marketing architecture — Brain · Visibility · Movement · Memory — as a forkable Claude Code starter.**

Clone it, fill in YOUR brand, and you have the framework running: a router that refuses to write without a brief, a writer that can't start before reading your voice guide, and a guardian that blocks anything below 9/10.

## The 4 layers, mapped to files

| Layer | The question | Where it lives here |
|---|---|---|
| 🧠 **Brain** | How does it think? | `skills/marketing-router/` + `agents/` — specialists with structural enforcement, not one mega-prompt |
| 👁 **Visibility** | How does the org see what it did? | `activity-log.md` — every run appends one line; share the file |
| 🦿 **Movement** | What does it actually DO? | `hooks/log-run.sh` — history writes itself; graduate to schedulers and triggers |
| 💾 **Memory** | What survives between runs? | `memory/` — read at start, updated at end; week 10 beats week 1 |

Plus: `brand/` (your voice + design canon — fill-in templates), `CLAUDE.md` (the LLM's operating contract, loaded automatically), `data/content-cards.example.jsonl` (the entity shape: status · guardian score · **evidence** — approved ≠ shipped), and `scorecard.md` (score your stack, find your next build).

## Quick start

```bash
git clone https://github.com/blutrich/marketing-engineering-starter.git
cd marketing-engineering-starter && claude
```

1. Fill `brand/voice-guide.md` and `brand/rules.md` (replace every bracket — or ask Claude to interview you; it will).
2. Ask for content. The router confirms a brief, the writer drafts, the guardian scores. You only see what passed.
3. When you reject something the guardian passed, say why — the second occurrence becomes a rule. That loop is the whole system.

## Hands-on feature-launch workshop

For the runnable exercise, start with [the workshop guide](skills/feature-launch-workshop/README.md) or [the Hebrew guide](skills/feature-launch-workshop/START_HERE.md).

The workshop takes supplied sources through a brief, draft, three reviews, and an explicit human decision. It includes a fictional mistake-and-correction demo, editable role prompts, a worksheet, and a local report. The runner uses Python 3.10+ with no dependencies, model calls, or publishing connectors; your existing assistant can help with the real drafting exercise.

```sh
cd skills/feature-launch-workshop
python3 harness.py demo --out runs/demo
```

Open `runs/demo/report.html`. The demo uses saved fictional content and review results and stops before human approval. For the real exercise, open this workshop directory in your assistant and follow its local `AGENTS.md` and guide.

## Build order

1. **Visibility** first — trust before autonomy
2. **Memory** second — cheap, compounds
3. **Brain** third — specialists, once you know what good means
4. **Movement** last — only automate what you already trust

## License

MIT — take it, fork it, build on it.

---

Built by [Ofer Blutrich](https://www.linkedin.com/in/ofer-blutrich). More free tools: [community-pulse](https://github.com/blutrich/community-pulse) · [weekly-competitor-news](https://github.com/blutrich/weekly-competitor-news)
