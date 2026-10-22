# Contributing

Keep contributions focused on api diagnostics. Start from an observable problem; discuss large changes in an issue.

1. Use Python 3.9+ and read SKILL.md and docs/INPUT.md.
2. Change the owning helper or instructions and add a meaningful regression test.
3. Run python3 -m unittest discover -s tests -v.
4. Run the example; change its expected output only for an intentional behavior change.
5. Document changed inputs, errors, and limitations.

Tests must not require real credentials. Live checks belong in a separate, explicitly identified procedure. Keep the English and Simplified Chinese README and tutorial in sync. Write concrete English commit messages; describe the change rather than instructions to an assistant. Retain required notices for imported code. Pull requests should explain the problem, resulting behavior, and checks actually run. Contributions use MIT; no additional CLA is required.
