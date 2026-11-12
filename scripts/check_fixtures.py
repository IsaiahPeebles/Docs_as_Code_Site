"""Validate saved live responses in openapi/fixtures/<Schema>/*.json against the spec.

Also fails if a documented top-level field never appears in any fixture,
so the spec cannot describe fields nobody has seen. Runs offline.
"""
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

spec = yaml.safe_load(Path("openapi/openlibrary.yaml").read_text())
schemas = spec["components"]["schemas"]
problems = []

for folder in sorted(Path("openapi/fixtures").iterdir()):
    name = folder.name
    validator = Draft202012Validator({**spec, "$ref": f"#/components/schemas/{name}"})
    seen = set()
    for fixture in sorted(folder.glob("*.json")):
        data = json.loads(fixture.read_text())
        seen |= set(data)
        for error in validator.iter_errors(data):
            problems.append(f"{fixture}: {list(error.path)}: {error.message[:150]}")
    for field in sorted(set(schemas[name].get("properties", {})) - seen):
        problems.append(f"{name}.{field}: documented but not in any fixture")

print("\n".join(problems) or f"Fixtures match the spec ({len(list(Path('openapi/fixtures').glob('*/*.json')))} files).")
sys.exit(1 if problems else 0)
