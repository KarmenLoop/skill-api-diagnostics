"""Standard-library utilities. No network calls or hidden configuration."""
import argparse
import json
import math
import sys
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

def text(value, label="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonempty string")
    return value

def records(data, key):
    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
        raise ValueError(key + " must be an array of objects")
    return value

def strings(value, label):
    if not isinstance(value, list):
        raise ValueError(label + " must be an array")
    return [text(x, label) for x in value]

def number(value, label, minimum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(label + " must be finite")
    if minimum is not None and value < minimum:
        raise ValueError(label + " is below its minimum")
    return value

def integer(value, label, minimum=0):
    number(value, label, minimum)
    if not isinstance(value, int):
        raise ValueError(label + " must be an integer")
    return value

def money(value):
    if isinstance(value, bool):
        raise ValueError("amount must be a decimal")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("invalid decimal amount") from exc
    if not result.is_finite():
        raise ValueError("amount must be finite")
    return result

def day(value):
    return date.fromisoformat(text(value, "date"))

def instant(value):
    value = datetime.fromisoformat(text(value, "timestamp").replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("timestamps require a UTC offset")
    return value.astimezone(timezone.utc)

def unique(rows, key="id"):
    seen = set()
    for row in rows:
        ident = text(row.get(key), key)
        if ident in seen:
            raise ValueError("duplicate " + key + ": " + ident)
        seen.add(ident)
    return seen

def choice(value, values, label):
    if value not in values:
        raise ValueError(label + " must be one of: " + ", ".join(values))
    return value

def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result

def load_json(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(10 * 1024 * 1024 + 1)
    if len(raw) > 10 * 1024 * 1024:
        raise ValueError("input exceeds 10 MiB; split it into batches")
    def invalid_constant(value):
        raise ValueError("non-finite JSON constant: " + value)
    value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_object, parse_constant=invalid_constant)
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value

def main(process, description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", required=True, help="UTF-8 JSON input; see docs/INPUT.md")
    parser.add_argument("--output", help="new output file; existing files are never overwritten")
    args = parser.parse_args()
    try:
        result = process(load_json(args.input))
        rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            with Path(args.output).open("x", encoding="utf-8") as stream:
                stream.write(rendered)
        else:
            sys.stdout.write(rendered)
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        print("Error: " + str(exc), file=sys.stderr)
        return 2
