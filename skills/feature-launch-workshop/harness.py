#!/usr/bin/env python3
"""Original, offline workshop harness. It records work; it never calls a model."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
GATES = ("facts", "voice", "completeness")
INPUTS = (
    "sources.json", "brief.json", "draft.json", "context/brand.md",
    "context/rules.md", "context/lessons.json",
)
LIMITATION = (
    "Mechanical checks validate structure, references, and exact evidence quotations. "
    "They cannot establish semantic truth, brand taste, reviewer independence, or human identity. "
    "Reviewer names and approval are self-attested. This tool makes no model, network, or publishing calls."
)


class UserError(Exception):
    """A clear, recoverable command/input error."""


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise UserError(f"Cannot read {path}: {exc}") from exc


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def substantive(value):
    return text_value(value) and len(value.strip()) >= 24 and len(value.split()) >= 5


def digest_files(run, names):
    """Length-prefixed bytes bind exact files, including whitespace-only edits."""
    digest = hashlib.sha256()
    for name in names:
        data = (run / name).read_bytes()
        encoded_name = name.encode("utf-8")
        digest.update(len(encoded_name).to_bytes(8, "big") + encoded_name)
        digest.update(len(data).to_bytes(8, "big") + data)
    return digest.hexdigest()


def require_run(run):
    run = Path(run)
    if not run.is_dir():
        raise UserError(f"Run directory does not exist: {run}. Use init first.")
    return run


def validate_inputs(run):
    errors = []
    documents = {}
    for name in INPUTS:
        path = run / name
        try:
            raw = path.read_text(encoding="utf-8")
            if not raw.strip():
                errors.append(f"{name}: file must not be empty.")
            documents[name] = json.loads(raw) if name.endswith(".json") else raw
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{name}: cannot read valid input ({exc}).")

    def object_at(name):
        value = documents.get(name)
        if not isinstance(value, dict):
            errors.append(f"{name}: expected a JSON object.")
            return {}
        return value

    def nonempty_list(value, label):
        if not isinstance(value, list) or not value:
            errors.append(f"{label}: expected a nonempty list.")
            return []
        return value

    def strings(obj, fields, label):
        for field in fields:
            if not text_value(obj.get(field)):
                errors.append(f"{label}.{field}: expected nonempty text.")

    sources = {}
    for index, source in enumerate(nonempty_list(object_at("sources.json").get("sources"), "sources")):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label}: expected an object.")
            continue
        strings(source, ("id", "title", "text"), label)
        source_id = source.get("id")
        if text_value(source_id):
            if source_id in sources:
                errors.append(f"{label}.id: duplicate source ID {source_id!r}.")
            sources[source_id] = source

    brief = object_at("brief.json")
    strings(brief, ("audience", "objective", "angle", "cta"), "brief")
    claims = {}
    for index, claim in enumerate(nonempty_list(brief.get("claims"), "brief.claims")):
        label = f"brief.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label}: expected an object.")
            continue
        strings(claim, ("id", "text"), label)
        claim_id = claim.get("id")
        if text_value(claim_id):
            if claim_id in claims:
                errors.append(f"{label}.id: duplicate claim ID {claim_id!r}.")
            claims[claim_id] = claim
        if claim.get("availability") not in ("available", "planned", "unknown"):
            errors.append(f"{label}.availability: use available, planned, or unknown.")
        for evidence_index, evidence in enumerate(nonempty_list(claim.get("evidence"), label + ".evidence")):
            ev_label = f"{label}.evidence[{evidence_index}]"
            if not isinstance(evidence, dict):
                errors.append(f"{ev_label}: expected an object.")
                continue
            strings(evidence, ("source_id", "quote"), ev_label)
            source_id, quote = evidence.get("source_id"), evidence.get("quote")
            if not text_value(source_id) or source_id not in sources:
                errors.append(f"{ev_label}: unknown source ID.")
            elif text_value(quote):
                source_text = sources[source_id].get("text")
                if not isinstance(source_text, str) or quote not in source_text:
                    errors.append(f"{ev_label}: quotation is not an exact substring of source {source_id!r}.")

    draft = object_at("draft.json")
    strings(draft, ("title", "body", "cta"), "draft")
    refs = nonempty_list(draft.get("claim_ids"), "draft.claim_ids")
    seen = set()
    for ref in refs:
        if not text_value(ref) or ref not in claims:
            errors.append("draft.claim_ids: every entry must name a known brief claim.")
        elif ref in seen:
            errors.append(f"draft.claim_ids: duplicate reference {ref!r}.")
        else:
            seen.add(ref)

    lessons = object_at("context/lessons.json").get("lessons")
    if not isinstance(lessons, list):
        errors.append("context/lessons.json: lessons must be a list.")
    else:
        for index, lesson in enumerate(lessons):
            if not isinstance(lesson, dict):
                errors.append(f"context/lessons.json: lesson {index} must be an object.")
            else:
                strings(lesson, ("id", "rule", "created_at"), f"lessons[{index}]")
    try:
        digest = digest_files(run, INPUTS)
    except OSError:
        digest = None
    return documents, errors, digest


def inspect_run(run):
    run = require_run(run)
    documents, errors, digest = validate_inputs(run)
    reviews = {}
    review_issues = []
    has_failure = False
    for gate in GATES:
        path = run / "reviews" / f"{gate}.json"
        if not path.exists():
            review_issues.append(f"{gate}: review missing.")
            continue
        try:
            review = read_json(path)
        except UserError:
            review_issues.append(f"{gate}: review is unreadable or invalid JSON.")
            continue
        if not isinstance(review, dict):
            review_issues.append(f"{gate}: review must be an object.")
            continue
        reviews[gate] = review
        if review.get("input_digest") != digest or not digest:
            review_issues.append(f"{gate}: stale review; review the current inputs again.")
        elif (
            review.get("gate") != gate or review.get("decision") not in ("pass", "fail")
            or not text_value(review.get("by")) or not substantive(review.get("note"))
            or not text_value(review.get("created_at"))
            or review.get("origin") not in ("operator", "demo_fixture")
        ):
            review_issues.append(f"{gate}: incomplete review; needs a name, verdict, and substantive note.")
        elif review["decision"] == "fail":
            has_failure = True
            review_issues.append(f"{gate}: reviewer returned fail. {review['note']}")

    state = "blocked" if errors or has_failure else "needs_review" if review_issues else "awaiting_human_approval"
    approval = None
    publication = None
    notices = []
    if (run / "approval.json").exists():
        try:
            candidate = read_json(run / "approval.json")
            valid = (
                state == "awaiting_human_approval" and isinstance(candidate, dict)
                and candidate.get("input_digest") == digest
                and text_value(candidate.get("by")) and text_value(candidate.get("created_at"))
                and candidate.get("attestation") == "I reviewed this version and approve its content."
                and candidate.get("reviews_digest") == digest_files(run, [f"reviews/{gate}.json" for gate in GATES])
            )
            if valid:
                approval = candidate
                state = "approved"
            else:
                notices.append("Previous approval is stale or invalid; approve again after current reviews pass.")
        except (UserError, OSError):
            notices.append("Previous approval is unreadable; approve again after current reviews pass.")
    if (run / "publication.json").exists():
        try:
            candidate = read_json(run / "publication.json")
            valid = (
                state == "approved" and isinstance(candidate, dict)
                and candidate.get("input_digest") == digest
                and candidate.get("approval_digest") == digest_files(run, ["approval.json"])
                and candidate.get("kind") == "manual_operator_record"
                and text_value(candidate.get("by")) and text_value(candidate.get("created_at"))
                and valid_url(candidate.get("url"))
            )
            if valid:
                publication = candidate
                state = "publication_recorded"
            else:
                notices.append("Previous publication record does not establish publication of this version.")
        except (UserError, OSError):
            notices.append("Previous publication record is unreadable.")
    fixture_reviews = any(review.get("origin") == "demo_fixture" for review in reviews.values())
    return {
        "state": state, "input_digest": digest, "checked_at": now(),
        "mechanical_checks_passed": not errors, "errors": errors,
        "review_issues": review_issues, "notices": notices,
        "reviews": reviews, "approval": approval, "publication": publication,
        "demo": (run / "demo-history.json").exists() or fixture_reviews,
        "limitation": LIMITATION, "documents": documents,
    }


def valid_url(value):
    if not text_value(value) or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("https", "http") and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


def render_report(run, result):
    esc = lambda value: html.escape(str(value), quote=True)
    def pretty(value):
        return "<pre>" + esc(json.dumps(value, indent=2, ensure_ascii=False)) + "</pre>"
    def items(values):
        return "<ul>" + "".join("<li>" + esc(value) + "</li>" for value in values) + "</ul>"
    docs = result["documents"]
    draft = docs.get("draft.json")
    if not isinstance(draft, dict):
        draft = {}
    demo = (
        '<div class="demo"><strong>DEMO · fictional fixture replay</strong><br>'
        'All Fieldnote product facts, content, reviews, and URLs are fictional. '
        'These saved reviews are scripted examples, not fresh AI review or human approval.</div>'
        if result["demo"] else ""
    )
    review_cards = ""
    for gate in GATES:
        review = result["reviews"].get(gate, {})
        current = review.get("input_digest") == result["input_digest"] and bool(result["input_digest"])
        review_cards += (
            '<article><h3>' + esc(gate.title()) + '</h3><p><strong>'
            + esc(review.get("decision", "missing").upper() if isinstance(review.get("decision", "missing"), str) else "INVALID")
            + '</strong> · ' + ("current version" if current else "missing or stale")
            + '</p><p>' + esc(review.get("note", "No substantive review recorded."))
            + '</p><small>' + esc(review.get("by", "—")) + ' · '
            + esc(review.get("origin", "operator review needed")) + '</small></article>'
        )
    history = ""
    if (run / "demo-history.json").exists():
        try:
            history = '<section><h2>Demo: bad → corrected</h2>' + pretty(read_json(run / "demo-history.json")) + '</section>'
        except UserError as exc:
            history = '<section><h2>Demo history</h2><p>' + esc(exc) + '</p></section>'
    approval = (
        '<p>Approved by ' + esc(result["approval"]["by"]) + '. Self-attested operator approval for this version.</p>'
        if result["approval"] else '<p>No valid human approval for this version. Passing reviews stop at awaiting_human_approval.</p>'
    )
    publication = (
        '<p><strong>Manual publication record only.</strong> Supplied by '
        + esc(result["publication"]["by"]) + ': <a href="' + esc(result["publication"]["url"])
        + '" rel="noreferrer">' + esc(result["publication"]["url"]) + '</a>. '
        'The tool did not publish or independently verify this URL.</p>'
        if result["publication"] else '<p>No current publication evidence recorded. This tool has no publishing connector.</p>'
    )
    css = """
    :root{color-scheme:light;font-family:system-ui,sans-serif;color:#20313a;background:#f4f2eb}
    body{margin:0}main{max-width:1080px;margin:auto;padding:38px 24px 72px}
    h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.06;letter-spacing:-.04em;margin:14px 0}
    h2{font-size:1.3rem}h3{margin:0}p,li{line-height:1.55}small{color:#52626a}
    .eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:.76rem;font-weight:700}
    .demo{background:#fff0c9;border:1px solid #ddb957;padding:16px;border-radius:10px;margin:20px 0}
    .state{display:inline-block;background:#806013;color:white;border-radius:30px;padding:9px 17px;font-weight:700}
    .state.blocked{background:#9d302e}.state.approved,.state.publication_recorded{background:#193f38}
    section{background:white;border:1px solid #dddcd4;border-radius:12px;margin:20px 0;padding:22px}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
    article{background:#f4f6f3;border-radius:8px;padding:18px}.body{white-space:pre-wrap}
    pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.83rem;line-height:1.5;background:#f5f5f1;padding:16px;border-radius:8px}
    code{overflow-wrap:anywhere;font-size:.78rem}a{color:#1c626a}details{margin:12px 0}
    summary{cursor:pointer;font-weight:650}.quiet{color:#52626a;font-size:.9rem}
    @media print{body{background:white}main{padding:0}section{break-inside:avoid}details{display:block}}
    """
    report = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Local workflow report</title><style>' + css + '</style></head><body><main>'
        '<div class="eyebrow">Marketing engineering · local workshop</div><h1>From evidence to a reviewed draft.</h1>'
        + demo + '<span class="state ' + esc(result["state"]) + '">' + esc(result["state"]) + '</span><p class="quiet">Run: '
        + esc(run.name) + '<br>Checked: ' + esc(result["checked_at"]) + '<br>Version: <code>'
        + esc(result["input_digest"] or "unavailable: missing input") + '</code></p>'
        '<section><h2>Checks and next action</h2><p>Mechanical checks: <strong>'
        + ("pass" if result["mechanical_checks_passed"] else "fail") + '</strong>.</p>'
        + items(result["errors"] + result["review_issues"] + result["notices"])
        + '<p class="quiet">' + esc(LIMITATION) + '</p></section>'
        '<section><h2>Draft</h2><h3>' + esc(draft.get("title", "Draft missing")) + '</h3>'
        '<p class="body">' + esc(draft.get("body", "")) + '</p><p><strong>CTA:</strong> '
        + esc(draft.get("cta", "")) + '</p><p class="quiet">Claim references: '
        + esc(draft.get("claim_ids", [])) + '</p></section>'
        '<section><h2>Three reviews</h2><div class="grid">' + review_cards + '</div></section>'
        '<section><h2>Human decision and publication evidence</h2>' + approval + publication + '</section>'
        '<section><h2>Evidence and run context</h2>'
        + ''.join('<details><summary>' + esc(name) + '</summary>'
                  + (pretty(docs.get(name)) if name.endswith('.json') else '<pre>' + esc(docs.get(name, 'Missing')) + '</pre>')
                  + '</details>' for name in INPUTS if name != 'draft.json')
        + '</section>' + history
        + '<p class="quiet">Brain: role instructions and checks · Visibility: this report · '
        'Movement: local file operations · Memory: explicit lessons copied into new runs.</p>'
        '</main></body></html>'
    )
    (run / "report.html").write_text(report, encoding="utf-8")


def refresh(run):
    result = inspect_run(run)
    save(run / "check.json", {key: value for key, value in result.items() if key != "documents"})
    render_report(run, result)
    return result


def init_run(run, fixture_context=None):
    run = Path(run)
    if run.exists():
        raise UserError(f"Output already exists: {run}. Choose a new run directory.")
    snapshots = {}
    for source, destination in (
        ("config/brand.md", "context/brand.md"),
        ("config/rules.md", "context/rules.md"),
        ("memory/lessons.json", "context/lessons.json"),
    ):
        try:
            source_path = fixture_context / Path(destination).name if fixture_context else ROOT / source
            snapshots[destination] = source_path.read_bytes()
        except OSError as exc:
            raise UserError(f"Missing starter configuration {source}: {exc}") from exc
    run.mkdir(parents=True)
    for name, data in snapshots.items():
        destination = run / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    save(run / "sources.json", {"sources": [{"id": "s1", "title": "", "text": ""}]})
    save(run / "brief.json", {"audience": "", "objective": "", "angle": "", "cta": "", "claims": [
        {"id": "c1", "text": "", "availability": "unknown", "evidence": [{"source_id": "s1", "quote": ""}]}
    ]})
    save(run / "draft.json", {"title": "", "body": "", "cta": "", "claim_ids": ["c1"]})
    return refresh(run)


def record_review(run, gate, by, decision, note, origin="operator"):
    if not text_value(by):
        raise UserError("A nonempty reviewer name is required.")
    if not substantive(note):
        raise UserError("Review note must contain at least 24 characters and 5 words explaining the verdict.")
    result = inspect_run(run)
    if result["errors"]:
        refresh(run)
        raise UserError("Fix mechanical input errors before recording a review. See report.html.")
    save(run / "reviews" / f"{gate}.json", {
        "gate": gate, "by": by.strip(), "decision": decision, "note": note.strip(),
        "input_digest": result["input_digest"], "created_at": now(), "origin": origin,
    })
    return refresh(run)


def approve_run(run, by):
    if not text_value(by):
        raise UserError("A nonempty approver name is required.")
    result = refresh(run)
    if result["state"] not in ("awaiting_human_approval", "approved", "publication_recorded"):
        raise UserError("Approval requires all three current, substantive passing reviews and valid inputs.")
    save(run / "approval.json", {
        "by": by.strip(), "created_at": now(), "input_digest": result["input_digest"],
        "reviews_digest": digest_files(run, [f"reviews/{gate}.json" for gate in GATES]),
        "attestation": "I reviewed this version and approve its content.",
    })
    return refresh(run)


def record_publication(run, by, url):
    if not text_value(by):
        raise UserError("A nonempty operator name is required.")
    if not valid_url(url):
        raise UserError("Use an http or https URL with a hostname, without credentials or whitespace.")
    result = refresh(run)
    if result["state"] not in ("approved", "publication_recorded"):
        raise UserError("A current explicit approval is required before recording publication evidence.")
    save(run / "publication.json", {
        "kind": "manual_operator_record", "by": by.strip(), "url": url,
        "created_at": now(), "input_digest": result["input_digest"],
        "approval_digest": digest_files(run, ["approval.json"]),
        "notice": "Operator-supplied evidence only. This tool neither published nor verified the URL.",
    })
    return refresh(run)


def add_lesson(rule):
    if not substantive(rule):
        raise UserError("A lesson needs at least 24 characters and 5 words describing a reusable rule.")
    path = ROOT / "memory" / "lessons.json"
    document = read_json(path)
    if not isinstance(document, dict) or not isinstance(document.get("lessons"), list):
        raise UserError("memory/lessons.json must be an object with a lessons list.")
    if any(isinstance(item, dict) and item.get("rule") == rule.strip() for item in document["lessons"]):
        raise UserError("This exact lesson already exists; no duplicate was added.")
    lesson = {"id": "lesson-" + hashlib.sha256(rule.strip().encode()).hexdigest()[:12], "rule": rule.strip(), "created_at": now()}
    document["lessons"].append(lesson)
    save(path, document)
    return lesson


def run_demo(run):
    fixture = ROOT / "examples" / "fieldnote"
    init_run(run, fixture_context=fixture)
    for name in ("sources.json", "brief.json", "draft.json"):
        save(run / name, read_json(fixture / name))
    bad_brief = read_json(run / "brief.json")
    bad_brief["claims"][1]["text"] = "Live collaboration is available today."
    bad_brief["claims"][1]["availability"] = "available"
    save(run / "brief.json", bad_brief)
    save(run / "draft.json", read_json(fixture / "bad-draft.json"))
    caught = record_review(run, "facts", "Fictional fixture: facts reviewer", "fail",
        "The draft calls live collaboration available and promises free forever. The quoted source says collaboration is planned and pricing is unknown.", "demo_fixture")
    history = {
        "label": "DEMO: fictional deterministic fixture replay, not fresh AI output or human approval.",
        "steps": [{"step": "bad", "state": caught["state"], "input_digest": caught["input_digest"],
                   "mechanical_checks_passed": caught["mechanical_checks_passed"],
                   "draft": read_json(run / "draft.json"), "facts_review": caught["reviews"]["facts"]}],
    }
    save(run / "demo-history.json", history)
    for name in ("brief.json", "draft.json"):
        save(run / name, read_json(fixture / name))
    corrected_before_reviews = refresh(run)
    history["steps"].append({"step": "corrected; old review stale", "state": corrected_before_reviews["state"],
                              "input_digest": corrected_before_reviews["input_digest"],
                              "review_issues": corrected_before_reviews["review_issues"]})
    notes = {
        "facts": "The corrected draft identifies checklists as available, collaboration as planned, and pricing as unspecified; these match the fictional source quotations.",
        "voice": "The corrected draft uses direct, practical language for project leads, avoids hype, and keeps the invitation clear under the fictional sample brand rules.",
        "completeness": "The draft has a title, feature explanation, explicit availability limits, and a fictional example.invalid call to action; all three claim references are present.",
    }
    for gate in GATES:
        result = record_review(run, gate, f"Fictional fixture: {gate} reviewer", "pass", notes[gate], "demo_fixture")
    history["steps"].append({"step": "corrected and reviewed", "state": result["state"],
                              "input_digest": result["input_digest"],
                              "draft": read_json(run / "draft.json"),
                              "note": "Fixture reviews are examples. No approval or publication record was created."})
    save(run / "demo-history.json", history)
    return refresh(run)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "check", "status", "review", "approve", "record-publication"):
        command = commands.add_parser(name)
        command.add_argument("run", type=Path)
        if name in ("review", "approve", "record-publication"):
            command.add_argument("--by", required=True, help="Self-attested operator/reviewer name")
        if name == "review":
            command.add_argument("--gate", choices=GATES, required=True)
            command.add_argument("--decision", choices=("pass", "fail"), required=True)
            command.add_argument("--note", required=True)
        if name == "record-publication":
            command.add_argument("--url", required=True)
    commands.add_parser("demo").add_argument("--out", type=Path, required=True)
    commands.add_parser("learn").add_argument("--rule", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "learn":
            lesson = add_lesson(args.rule)
            print(f"Added {lesson['id']}. New runs will copy this explicit lesson; existing runs stay unchanged.")
            return 0
        run = args.out if args.command == "demo" else args.run
        if args.command == "init":
            result = init_run(run)
        elif args.command == "demo":
            result = run_demo(run)
            print("DEMO — fictional deterministic replay. Bad claim caught → corrected → no human approval.")
        else:
            require_run(run)
            if args.command in ("check", "status"):
                result = refresh(run)
            elif args.command == "review":
                result = record_review(run, args.gate, args.by, args.decision, args.note)
            elif args.command == "approve":
                result = approve_run(run, args.by)
            else:
                result = record_publication(run, args.by, args.url)
        print(f"State: {result['state']}")
        print(f"Version: {result['input_digest'] or 'unavailable'}")
        for issue in result["errors"] + result["review_issues"] + result["notices"]:
            print(f"- {issue}")
        print(f"Report: {(run / 'report.html').resolve()}")
        if args.command == "record-publication":
            print("Manual evidence recorded only. No publication or URL verification was performed.")
        return 1 if args.command == "check" and result["state"] == "blocked" else 0
    except (UserError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
