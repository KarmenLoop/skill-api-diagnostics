import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliIOTests(unittest.TestCase):
    def call(self, *args, content=None):
        return subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), *args], input=content, capture_output=True, timeout=10)

    def test_stdin_matches_the_example_file(self):
        sample = (ROOT / "examples/input.json").read_bytes()
        result = self.call("--input", "-", content=sample)
        expected = self.call("--input", str(ROOT / "examples/input.json"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), json.loads(expected.stdout))

    def test_version_does_not_need_an_input(self):
        metadata = json.loads((ROOT / "skill.json").read_text())
        result = self.call("--version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.decode().strip(), metadata["name"] + " " + metadata["version"])

    def test_stdin_validation_keeps_the_output_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "result.json"
            for invalid in [b"[]", b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":' * 1500 + b"0" + b"}" * 1500]:
                with self.subTest(invalid=invalid[:30]):
                    result = self.call("--input", "-", "--output", str(target), content=invalid)
                    self.assertEqual(result.returncode, 2)
                    self.assertNotIn(b"Traceback", result.stderr)
                    self.assertFalse(target.exists())

    def test_stdin_can_save_a_new_output(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "result.json"
            result = self.call("--input", "-", "--output", str(target), content=(ROOT / "examples/input.json").read_bytes())
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b"")
            self.assertIsInstance(json.loads(target.read_text()), dict)


if __name__ == "__main__":
    unittest.main()
