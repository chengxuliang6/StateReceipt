from __future__ import annotations
from importlib.resources import files
import json
from jsonschema import Draft202012Validator, FormatChecker


def get_schema() -> dict:
    p = files("statereceipt.schema").joinpath("statereceipt-v0.1.schema.json")
    return json.loads(p.read_text(encoding="utf-8"))


def schema_errors(doc: dict) -> list[str]:
    validator = Draft202012Validator(get_schema(), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    out = []
    for e in errors:
        loc = ".".join(str(x) for x in e.absolute_path) or "$"
        out.append(f"{loc}: {e.message}")
    return out
