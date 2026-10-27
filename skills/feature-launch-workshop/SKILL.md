---
name: feature-launch-workshop
description: Practice a source-backed feature-launch workflow with a local demo, three reviews, and an explicit human decision.
---

# Feature-launch workshop

Use this exercise when a participant wants to learn how to build and inspect an agent workflow. It is a standalone educational package inside the starter repository.

1. Work from this directory, not the repository root. Read `README.md` and `AGENTS.md`, then `roles/coordinator.md`.
2. For Hebrew guidance, use `START_HERE.md`.
3. For a demonstration, run `python3 harness.py demo --out runs/demo` and open `runs/demo/report.html`. Explain that the content and reviews are fictional saved examples, not fresh AI output.
4. For a real exercise, follow the participant path in `README.md`, using the participant's authorized sources and the brand and rules in this package's `config/` directory. Its local `AGENTS.md` and `CLAUDE.md` govern the exercise.
5. Stop at the human decision. Do not fabricate reviews, record approval on the participant's behalf, or publish a draft.

The Python runner makes no model, network, or publishing calls. The participant's assistant handles drafting and substantive review separately.
