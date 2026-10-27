"""Setup checker tests: isolated fixtures, no writes to participant brand files."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().with_name("check-setup.py")
REQUIRED = ("voice-guide.md", "rules.md", "product.md", "audience.md")


class SetupCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / "participant"
        (self.root / "brand").mkdir(parents=True)
        for name in REQUIRED:
            self.write(f"brand/{name}", "# Fieldnote\nThis fictional example contains filled-in context.\n")
        self.other_cwd = self.directory / "elsewhere"
        self.other_cwd.mkdir()

    def write(self, relative_path, text):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_check(self, *args, script=SCRIPT, include_root=True):
        command = [sys.executable, str(script)]
        if include_root:
            command += ["--root", str(self.root)]
        return subprocess.run(
            command + list(args), cwd=self.other_cwd,
            capture_output=True, text=True, check=False,
        )

    def test_filled_files_pass_with_explicit_limitations(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Setup ready", result.stdout)
        self.assertIn("does not verify factual accuracy", result.stdout)
        self.assertIn("brand fit, or approval", result.stdout)

    def test_new_and_legacy_placeholders_fail_with_file_and_line(self):
        self.write("brand/voice-guide.md", "# {{BRAND_NAME}}\nVoice: {{VOICE_PILLAR_1}}\n[YOUR BRAND]\nCHANGE_ME\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("[NEEDS INPUT] brand/voice-guide.md", result.stdout)
        for line, token in enumerate(("{{BRAND_NAME}}", "{{VOICE_PILLAR_1}}", "[YOUR BRAND]", "CHANGE_ME"), 1):
            self.assertIn(f"line {line}: unresolved placeholder {token}", result.stdout)

    def test_missing_and_whitespace_only_files_fail(self):
        (self.root / "brand/product.md").unlink()
        self.write("brand/audience.md", " \n\t\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("brand/product.md\n  - missing file", result.stdout)
        self.assertIn("brand/audience.md\n  - empty file", result.stdout)

    def test_unreadable_utf8_is_a_content_failure(self):
        (self.root / "brand/rules.md").write_bytes(b"\xff\xfe")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot read as a UTF-8 text file", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_directory_instead_of_file_is_a_content_failure(self):
        (self.root / "brand/product.md").unlink()
        (self.root / "brand/product.md").mkdir()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot read as a UTF-8 text file", result.stdout)

    def test_default_root_comes_from_script_not_current_directory(self):
        hooks = self.root / "hooks"
        hooks.mkdir()
        copied_script = hooks / "check-setup.py"
        shutil.copyfile(SCRIPT, copied_script)
        result = self.run_check(script=copied_script, include_root=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(str(self.root.resolve()), result.stdout)

    def test_visuals_are_optional_and_fail_when_missing_or_unfinished(self):
        self.assertEqual(self.run_check().returncode, 0)
        result = self.run_check("--visual")
        self.assertEqual(result.returncode, 1)
        self.assertIn("brand/DESIGN.md\n  - missing file", result.stdout)
        self.write("brand/DESIGN.md", "Font: {{BODY_FONT}}\n")
        self.assertEqual(self.run_check().returncode, 0)
        self.assertEqual(self.run_check("--visual").returncode, 1)
        self.write("brand/DESIGN.md", "Font: system-ui\n")
        self.assertEqual(self.run_check("--visual").returncode, 0)

    def test_brief_is_opt_in_and_relative_to_root_not_cwd(self):
        self.write("data/briefs/launch.md", "Audience: {{PRIMARY_AUDIENCE}}\n")
        self.assertEqual(self.run_check().returncode, 0)
        result = self.run_check("--brief", "data/briefs/launch.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("data/briefs/launch.md", result.stdout)
        self.assertIn("{{PRIMARY_AUDIENCE}}", result.stdout)
        self.write("data/briefs/launch.md", "Audience: field service team leads.\n")
        self.assertEqual(self.run_check("--brief", "data/briefs/launch.md").returncode, 0)

    def test_absolute_brief_and_missing_brief(self):
        external = self.other_cwd / "external.md"
        external.write_text("A completed external brief.\n", encoding="utf-8")
        self.assertEqual(self.run_check("--brief", str(external)).returncode, 0)
        external.unlink()
        result = self.run_check("--brief", str(external))
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing file", result.stdout)

    def test_markdown_link_labels_are_not_legacy_placeholders(self):
        self.write("brand/voice-guide.md", (
            "[YOUR BRAND](https://example.test/brand)\n"
            "[YOUR PRODUCT][product]\n"
            "[YOUR COMPANY]\n"
            "[YOUR COMPANY]: https://example.test/company\n"
            "[product]: https://example.test/product\n"
            "[ordinary prose] is not a supported placeholder.\n"
        ))
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_explicit_placeholder_in_markdown_link_is_still_unfinished(self):
        self.write("brand/voice-guide.md", "[Brand](https://{{BRAND_DOMAIN}}/brand)\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("{{BRAND_DOMAIN}}", result.stdout)

    def test_cli_errors_exit_two(self):
        self.assertEqual(self.run_check("--unknown").returncode, 2)
        self.assertEqual(self.run_check("--brief").returncode, 2)
        self.assertEqual(self.run_check("--root", str(self.directory / "missing")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
