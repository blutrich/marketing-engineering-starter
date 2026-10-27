"""Meaningful boundary tests for the offline workshop, using only stdlib."""

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import harness


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run = self.root / "runs" / "example"
        (self.root / "config").mkdir()
        (self.root / "config" / "brand.md").write_text("Use plain, practical language. Fictional brand.", encoding="utf-8")
        (self.root / "config" / "rules.md").write_text("Check facts, voice, and completeness against supplied evidence.", encoding="utf-8")
        harness.save(self.root / "memory" / "lessons.json", {"lessons": []})
        shutil.copytree(harness.ROOT / "examples", self.root / "examples")
        patcher = patch.object(harness, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def valid_run(self):
        harness.init_run(self.run)
        for name in ("sources.json", "brief.json", "draft.json"):
            harness.save(self.run / name, harness.read_json(self.root / "examples" / "fieldnote" / name))
        return harness.refresh(self.run)

    def pass_reviews(self):
        for gate in harness.GATES:
            harness.record_review(self.run, gate, "Test reviewer", "pass",
                                  f"I checked {gate} against the supplied context and found no blocking issues.")

    def test_demo_catches_semantic_mismatch_and_stops_before_approval(self):
        result = harness.run_demo(self.run)
        history = harness.read_json(self.run / "demo-history.json")
        self.assertEqual(history["steps"][0]["state"], "blocked")
        self.assertTrue(history["steps"][0]["mechanical_checks_passed"])
        self.assertEqual(history["steps"][1]["state"], "needs_review")
        self.assertEqual(result["state"], "awaiting_human_approval")
        self.assertFalse((self.run / "approval.json").exists())
        self.assertFalse((self.run / "publication.json").exists())
        self.assertTrue(result["demo"])
        self.assertIn("not fresh AI review or human approval", (self.run / "report.html").read_text())

    def test_missing_reviews_never_approve_or_record_publication(self):
        self.assertEqual(self.valid_run()["state"], "needs_review")
        with self.assertRaises(harness.UserError):
            harness.approve_run(self.run, "Operator")
        with self.assertRaises(harness.UserError):
            harness.record_publication(self.run, "Operator", "https://example.invalid/post")
        harness.record_review(self.run, "facts", "Reviewer", "pass", "The available claims match the quoted source evidence.")
        self.assertEqual(harness.inspect_run(self.run)["state"], "needs_review")

    def test_demo_uses_fixed_fictional_context_not_participant_settings(self):
        (self.root / "config" / "brand.md").write_text("Participant brand changed.", encoding="utf-8")
        harness.add_lesson("Always use the participant's requested naming in real work.")
        harness.run_demo(self.run)
        self.assertEqual((self.run / "context" / "brand.md").read_bytes(),
                         (self.root / "examples" / "fieldnote" / "brand.md").read_bytes())
        self.assertEqual(harness.read_json(self.run / "context" / "lessons.json"), {"lessons": []})

    def test_fail_review_blocks_and_invalidates_approval(self):
        self.valid_run()
        self.pass_reviews()
        harness.approve_run(self.run, "Operator")
        result = harness.record_review(self.run, "facts", "Reviewer", "fail",
                                       "The availability claim contradicts the supplied release source text.")
        self.assertEqual(result["state"], "blocked")
        self.assertIsNone(result["approval"])
        with self.assertRaises(harness.UserError):
            harness.record_publication(self.run, "Operator", "https://example.invalid/post")
        self.pass_reviews()
        self.assertEqual(harness.inspect_run(self.run)["state"], "awaiting_human_approval")

    def test_every_input_edit_invalidates_reviews_and_approval(self):
        self.valid_run()
        for filename in harness.INPUTS:
            with self.subTest(filename=filename):
                self.pass_reviews()
                harness.approve_run(self.run, "Operator")
                path = self.run / filename
                original = path.read_bytes()
                path.write_bytes(original + b"\n")
                result = harness.inspect_run(self.run)
                self.assertEqual(result["state"], "needs_review")
                self.assertEqual(sum("stale review" in issue for issue in result["review_issues"]), 3)
                self.assertIsNone(result["approval"])
                with self.assertRaises(harness.UserError):
                    harness.approve_run(self.run, "Operator")
                path.write_bytes(original)

    def test_quote_mismatch_blocks_even_with_matching_digest_reviews(self):
        self.valid_run()
        brief = harness.read_json(self.run / "brief.json")
        brief["claims"][0]["evidence"][0]["quote"] = "An invented quotation absent from the source."
        harness.save(self.run / "brief.json", brief)
        result = harness.refresh(self.run)
        self.assertEqual(result["state"], "blocked")
        self.assertTrue(any("exact substring" in issue for issue in result["errors"]))
        for gate in harness.GATES:
            harness.save(self.run / "reviews" / f"{gate}.json", {
                "gate": gate, "by": "Self-attested", "decision": "pass", "origin": "operator",
                "note": "I claim to have reviewed these input documents carefully.",
                "created_at": harness.now(), "input_digest": result["input_digest"],
            })
        with self.assertRaises(harness.UserError):
            harness.approve_run(self.run, "Operator")

    def test_unknown_source_and_claim_ids_are_blocked(self):
        self.valid_run()
        brief = harness.read_json(self.run / "brief.json")
        brief["claims"][0]["evidence"][0]["source_id"] = "missing-source"
        harness.save(self.run / "brief.json", brief)
        draft = harness.read_json(self.run / "draft.json")
        draft["claim_ids"] = ["missing-claim"]
        harness.save(self.run / "draft.json", draft)
        result = harness.refresh(self.run)
        self.assertEqual(result["state"], "blocked")
        self.assertTrue(any("unknown source" in issue for issue in result["errors"]))
        self.assertTrue(any("known brief claim" in issue for issue in result["errors"]))

    def test_empty_substantive_review_is_not_accepted(self):
        self.valid_run()
        for note in ("", "looks good", "x" * 100):
            with self.subTest(note=note), self.assertRaises(harness.UserError):
                harness.record_review(self.run, "facts", "Reviewer", "pass", note)
        self.pass_reviews()
        review = harness.read_json(self.run / "reviews" / "voice.json")
        review["note"] = "ok"
        harness.save(self.run / "reviews" / "voice.json", review)
        self.assertEqual(harness.inspect_run(self.run)["state"], "needs_review")
        with self.assertRaises(harness.UserError):
            harness.approve_run(self.run, "Operator")

    def test_missing_empty_and_malformed_inputs_fail_closed(self):
        self.valid_run()
        draft_path = self.run / "draft.json"
        original = draft_path.read_bytes()
        for data in (b"", b"{", b"[]", b'{"title":[]}', b'null'):
            with self.subTest(data=data):
                draft_path.write_bytes(data)
                self.assertEqual(harness.refresh(self.run)["state"], "blocked")
                with self.assertRaises(harness.UserError):
                    harness.record_review(self.run, "facts", "Reviewer", "pass", "I have checked every claim and supporting evidence quotation.")
        draft_path.unlink()
        self.assertEqual(harness.refresh(self.run)["state"], "blocked")
        draft_path.write_bytes(original)

    def test_malformed_review_and_approval_never_pass(self):
        self.valid_run()
        self.pass_reviews()
        harness.approve_run(self.run, "Operator")
        (self.run / "reviews" / "voice.json").write_text("[]", encoding="utf-8")
        self.assertEqual(harness.inspect_run(self.run)["state"], "needs_review")
        self.pass_reviews()
        for content in ("null", "{", "{}", "[]"):
            (self.run / "approval.json").write_text(content, encoding="utf-8")
            self.assertEqual(harness.inspect_run(self.run)["state"], "awaiting_human_approval")

    def test_publication_is_manual_record_and_expires_after_edit(self):
        self.valid_run()
        self.pass_reviews()
        harness.approve_run(self.run, "Operator")
        for url in ("javascript:alert(1)", "https:///missing-host", "https://user:secret@example.invalid", "https://example.invalid/a b"):
            with self.subTest(url=url), self.assertRaises(harness.UserError):
                harness.record_publication(self.run, "Operator", url)
        result = harness.record_publication(self.run, "Operator", "https://example.invalid/post")
        self.assertEqual(result["state"], "publication_recorded")
        self.assertEqual(result["publication"]["kind"], "manual_operator_record")
        self.assertIn("neither published nor verified", result["publication"]["notice"])
        draft = harness.read_json(self.run / "draft.json")
        draft["title"] += " Changed"
        harness.save(self.run / "draft.json", draft)
        result = harness.refresh(self.run)
        self.assertEqual(result["state"], "needs_review")
        self.assertIsNone(result["publication"])

    def test_html_escapes_all_supplied_content(self):
        self.valid_run()
        attack = '<script>alert("x")</script><img src=x onerror=alert(1)>'
        draft = harness.read_json(self.run / "draft.json")
        draft["title"] = attack
        draft["body"] = attack
        harness.save(self.run / "draft.json", draft)
        (self.run / "context" / "brand.md").write_text(attack, encoding="utf-8")
        harness.record_review(self.run, "facts", attack, "fail", f"This review contains supplied text for escaping: {attack}")
        report = (self.run / "report.html").read_text(encoding="utf-8")
        self.assertNotIn(attack, report)
        self.assertNotIn("<script>", report)
        self.assertIn("&lt;script&gt;", report)
        self.assertNotIn('src="http', report)

    def test_existing_output_is_preserved(self):
        self.valid_run()
        original = (self.run / "draft.json").read_bytes()
        for operation in (harness.init_run, harness.run_demo):
            with self.assertRaises(harness.UserError):
                operation(self.run)
            self.assertEqual((self.run / "draft.json").read_bytes(), original)

    def test_lessons_are_explicit_and_copied_only_to_new_runs(self):
        self.valid_run()
        original = (self.run / "context" / "lessons.json").read_bytes()
        rule = "Describe planned features as planned until supplied release evidence says otherwise."
        harness.add_lesson(rule)
        self.assertEqual((self.run / "context" / "lessons.json").read_bytes(), original)
        new_run = self.root / "runs" / "new"
        harness.init_run(new_run)
        self.assertEqual(harness.read_json(new_run / "context" / "lessons.json")["lessons"][0]["rule"], rule)
        with self.assertRaises(harness.UserError):
            harness.add_lesson(rule)

    def test_cli_exit_codes_and_report_creation(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(harness.main(["init", str(self.run)]), 0)
            self.assertEqual(harness.main(["check", str(self.run)]), 1)
            self.assertEqual(harness.main(["status", str(self.run)]), 0)
            self.assertEqual(harness.main(["init", str(self.run)]), 2)
            self.assertEqual(harness.main(["status", str(self.root / "missing")]), 2)
        self.assertTrue((self.run / "report.html").exists())
        self.assertTrue((self.run / "check.json").exists())


if __name__ == "__main__":
    unittest.main()
