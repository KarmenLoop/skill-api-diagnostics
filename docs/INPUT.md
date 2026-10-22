# Input and output

English | [简体中文](input.zh-CN.md)

Supply a UTF-8 JSON object (maximum 10 MiB). Use `--input PATH` for a file or `--input -` for standard input. Run `--version` to inspect the installed helper version. Duplicate JSON keys and non-finite JSON constants are rejected. Arrays are required unless documented as optional. IDs must be stable and unique. Dates use ISO 8601; timestamps require an explicit UTC offset.

| Field | Contract |
| --- | --- |
| endpoint | HTTP(S) URL; output omits userinfo, query, and fragment. |
| budget_seconds/elapsed_seconds | Nonnegative numbers. |
| replay_safe | Boolean established by the actual operation contract. |
| attempts | Nonempty objects: id, optional status integer 100..599, error_kind (dns/tls/timeout/connection/context/quota/none), optional retry_after_seconds. Use quota when the provider identifies exhausted credits or a hard quota, rather than a transient rate limit. |

## Example

```json
{
  "endpoint": "https://api.example.com/v1/chat/completions",
  "budget_seconds": 30,
  "elapsed_seconds": 4,
  "replay_safe": true,
  "attempts": [
    {
      "id": "1",
      "status": 503,
      "error_kind": "none",
      "retry_after_seconds": 2
    }
  ]
}
```

## Result

category, next_action, retry_allowed, retry_delay_seconds, endpoint, attempt_count, and remaining_budget_seconds.

See [the complete sample result](../examples/expected.json). Exit 0 means processing completed, not that all reported findings passed.

## Errors and side effects

The helper makes no network requests and executes no submitted commands. It reads the input and explicitly documented local paths. It writes only a requested new output file; stdout is the default. Invalid input exits 2. Existing output is preserved. An output write failure can leave a partial new file; remove that file before retrying. Installation is a separate explicit action.
