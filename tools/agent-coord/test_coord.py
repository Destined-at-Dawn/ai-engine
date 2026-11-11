# -*- coding: utf-8 -*-
"""Self-test for coord.py. Run: python tools/agent-coord/test_coord.py"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coord  # noqa: E402


def run(root, *argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            code = coord.main(["--root", root] + list(argv))
        except SystemExit as exc:  # check_agent exits with 2
            code = exc.code
    return code, buf.getvalue()


class CoordTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        self.assertEqual(run(self.root, "init")[0], 0)
        os.makedirs(os.path.join(self.root, "deliverables"))
        os.makedirs(os.path.join(self.root, "archive", "old"))

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_lease_is_exclusive(self):
        self.assertEqual(run(self.root, "claim", "--agent", "a", "--task", "edit")[0], 0)
        code, out = run(self.root, "claim", "--agent", "b", "--task", "edit too")
        self.assertEqual(code, 1)
        self.assertIn("CONFLICT", out)
        self.assertEqual(run(self.root, "release", "--agent", "b")[0], 1)
        self.assertEqual(run(self.root, "release", "--agent", "a")[0], 0)
        self.assertEqual(run(self.root, "claim", "--agent", "b", "--task", "edit")[0], 0)

    def test_expired_lease_takeover_is_logged(self):
        run(self.root, "claim", "--agent", "a", "--task", "x")
        lease_path = os.path.join(self.root, ".coord", "LEASE.json")
        with open(lease_path, "r", encoding="utf-8") as f:
            lease = json.load(f)
        lease["expires"] = "2000-01-01 00:00:00"
        with open(lease_path, "w", encoding="utf-8") as f:
            json.dump(lease, f)
        self.assertEqual(run(self.root, "claim", "--agent", "b", "--task", "y")[0], 0)
        with open(os.path.join(self.root, ".coord", "REGISTRY.jsonl"), encoding="utf-8") as f:
            kinds = [json.loads(line)["kind"] for line in f]
        self.assertIn("expired-takeover", kinds)

    def test_next_rev_scans_disk_and_registry(self):
        self.write("deliverables/report-r3.docx", "x")
        self.write("archive/old/report-r7.docx", "y")
        self.assertEqual(run(self.root, "next-rev", "--agent", "a")[1].strip(), "r8")
        # a second allocation before any file exists must not reuse r8
        self.assertEqual(run(self.root, "next-rev", "--agent", "b")[1].strip(), "r9")

    def test_doctor_detects_unlogged_revision_and_divergence(self):
        self.write("deliverables/report-r3.docx", "v3")
        self.assertEqual(run(self.root, "log", "--agent", "a", "--action", "r3",
                             "--artifact", "deliverables/report-r3.docx", "--baseline", "r3")[0], 0)
        self.assertEqual(run(self.root, "doctor")[0], 0)
        self.write("deliverables/report-r4.docx", "v4")
        code, out = run(self.root, "doctor")
        self.assertEqual(code, 1)
        self.assertIn("r4", out)
        os.remove(os.path.join(self.root, "deliverables", "report-r4.docx"))
        self.write("AGENTS.md", "rules A")
        self.write("CLAUDE.md", "rules B")
        code, out = run(self.root, "doctor")
        self.assertEqual(code, 1)
        self.assertIn("diverged", out)

    def test_doctor_detects_changed_artifact(self):
        self.write("deliverables/report-r3.docx", "v3")
        run(self.root, "log", "--agent", "a", "--action", "r3",
            "--artifact", "deliverables/report-r3.docx", "--baseline", "r3")
        self.write("deliverables/report-r3.docx", "edited without logging")
        code, out = run(self.root, "doctor")
        self.assertEqual(code, 1)
        self.assertIn("without logging", out)

    def test_log_missing_artifact_fails(self):
        code, out = run(self.root, "log", "--agent", "a", "--action", "x", "--artifact", "nope.docx")
        self.assertEqual(code, 1)
        self.assertIn("not found", out)

    def test_agent_allow_list(self):
        cfg_path = os.path.join(self.root, coord.CONFIG_NAME)
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["agents"] = ["claude-code", "codex"]
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        self.assertEqual(run(self.root, "claim", "--agent", "someone", "--task", "x")[0], 2)
        self.assertEqual(run(self.root, "claim", "--agent", "codex", "--task", "x")[0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
