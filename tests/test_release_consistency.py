from __future__ import annotations

import json
import tomllib
from pathlib import Path

import statereceipt


ROOT = Path(__file__).resolve().parents[1]


def test_package_version_matches_pyproject():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == statereceipt.__version__


def test_repository_schema_matches_packaged_schema():
    repository_schema = json.loads(
        (ROOT / "spec" / "statereceipt-v0.1.schema.json").read_text(encoding="utf-8")
    )
    packaged_schema = json.loads(
        (ROOT / "src" / "statereceipt" / "schema" / "statereceipt-v0.1.schema.json").read_text(encoding="utf-8")
    )
    assert repository_schema == packaged_schema


def test_schema_identifies_v0_1():
    schema = json.loads(
        (ROOT / "spec" / "statereceipt-v0.1.schema.json").read_text(encoding="utf-8")
    )
    assert schema["properties"]["spec"]["properties"]["name"]["const"] == "StateReceipt"
    assert schema["properties"]["spec"]["properties"]["version"]["const"] == "0.1"
