# Validation

Observed on 2026-10-18T19:54:18.143320+00:00 with Python 3.9.6 on macOS-27.0-arm64-arm-64bit.

| Check | Observed result |
| --- | --- |
| python3 scripts/run.py --input examples/input.json | Exit 0; expected.json saved from actual output |
| python3 -m unittest discover -s tests -v | Exit 0; 9 tests passed |
| skill-creator quick_validate.py | Exit 0; skill metadata accepted |

The test suite includes the real CLI, malformed input, preserved existing output, temporary-directory installation, duplicate JSON keys, and domain-specific regression cases. The fixture result is not used as the sole behavior oracle.

## Host acceptance

Not run: authenticated conversations inside every supported host, live account connectors, and native Windows/Linux execution. These require the actual host and relevant accounts. The installer and helper are locally tested; model interpretation remains a host responsibility.

To accept a host integration, install into a temporary or chosen skill directory, confirm discovery of the exact SKILL.md, invoke the example request from README.md, inspect the helper result, and try the domain failure case in tests/test_skill.py. Do not count a displayed skill name as proof of completed work.
