# Compatibility

The standard-library helper targets Python 3.9+ on macOS, Linux, and Windows. See VALIDATION.md for the platform actually exercised. The local example needs no account, server, or API key.

| Host | Installation | Directory |
| --- | --- | --- |
| Codex | python3 install.py --host codex | CODEX_HOME/skills/karmen-api-diagnostics, or ~/.codex/skills/karmen-api-diagnostics |
| DeepSeek Harness | python3 install.py --host deepseek | DSH_HOME/skills/karmen-api-diagnostics, or ~/.dsh/skills/karmen-api-diagnostics |
| Grok Build | python3 install.py --host grok | ~/.grok/skills/karmen-api-diagnostics |
| Shared compatible host | python3 install.py --host agents | ~/.agents/skills/karmen-api-diagnostics |

These targets use documented SKILL.md discovery. Installation is tested in temporary directories. Authenticated conversations in every host have not been run. Confirm that the actual skill appears before invocation. DeepSeek's filesystem provider must be enabled; Grok's project trust and disabled-skill settings still apply. The shared directory needs a host that scans it.

Muse public product behavior and Meta's published skills informed the research. This release does not include a connector to the private Muse personal-agent service or claim a tested native Muse plugin.

To remove or upgrade, back up local modifications and remove only this skill's installed directory. The installer refuses an existing destination. A skill installation does not grant computer or account permissions.
