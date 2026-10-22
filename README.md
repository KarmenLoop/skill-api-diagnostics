# API Diagnostics

English | [简体中文](README.zh-CN.md)

Work out what to fix after an API call fails. Feed in recorded attempts, a time budget, and the operation’s replay policy; get a failure category and a bounded retry recommendation.

[Download v0.2.1](https://github.com/KarmenLoop/skill-api-diagnostics/releases/tag/v0.2.1) · [Tutorial](docs/tutorial.en.md) · [Input reference](docs/INPUT.md) · [Report an issue](https://github.com/KarmenLoop/skill-api-diagnostics/issues)

## What it does

The sample records one 503 response, leaves 26 seconds, and recommends a 2-second delay because replay_safe is true.

The helper analyzes records; it makes no HTTP requests and cannot establish that replaying an operation is safe.

![API Diagnostics sample JSON output from version 0.2.1](docs/images/example-output-v0.2.1.svg)

*Actual local output from v0.2.1, rendered as an image. [Complete result](examples/expected.json) · [Image provenance](docs/images/provenance.json).*

## Start here

Download `karmen-api-diagnostics-v0.2.1.zip` and its `.sha256` file from the release, verify the hash, then extract the ZIP. In the extracted directory, use Python 3.9 or later:

```sh
python3 scripts/run.py --version
python3 scripts/run.py --input examples/input.json
```

Expected version: `karmen-api-diagnostics 0.2.1`. The sample records one 503 response, leaves 26 seconds, and recommends a 2-second delay because replay_safe is true.

To install the complete skill into a host that reads `~/.agents/skills`:

```sh
python3 install.py --host agents
```

The installer refuses an existing destination. Host discovery and invocation vary; see the [full setup and practice guide](docs/tutorial.en.md). You can run the helper directly without an AI host.

## Use it with your own work

Set replay_safe from the endpoint’s actual contract. Include elapsed_seconds and any provider Retry-After value. Record a hard credit limit as quota.

Try a 401 response and then an exhausted budget. Compare next_action and retry_allowed before deciding how your calling application should respond.

Read the [field contract](docs/INPUT.md) before preparing a new input. The helper runs locally with the Python standard library; it needs no model account, API key, or network connection. An AI host has its own data and permission settings.

## Questions

**Will it retry a failed payment?** No. It neither sends requests nor authorizes repeats. A payment’s idempotency rules must come from the payment service.

**Where does the result go?** JSON is printed to stdout unless you request a new file with `--output`. Existing output files are preserved. The helper reads only the submitted records and any local paths documented in its input contract.

## Documentation and support

- [Download, install, configure, practice, upgrade, and remove](docs/tutorial.en.md)
- [Input/output contract](docs/INPUT.md) and [compatibility](docs/COMPATIBILITY.md)
- [Changelog](CHANGELOG.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), and [security reports](SECURITY.md)

## License

[MIT](LICENSE). Keep the license and [notice](NOTICE.md) with redistributed copies. Maintained by [KarmenLoop](https://karmenloop.com).
