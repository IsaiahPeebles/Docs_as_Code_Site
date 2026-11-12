# Run every check. Needs the .venv from requirements.txt, and Node for Spectral (via npx).
BIN := .venv/bin
SPECTRAL := npx --yes @stoplight/spectral-cli@6.17.1

.PHONY: check vale spec fixtures build links

check: vale spec fixtures build links
	@echo "All checks passed."

vale:
	$(BIN)/vale docs

spec:
	$(SPECTRAL) lint --fail-severity=warn openapi/openlibrary.yaml

# Saved live responses must still match the spec (offline).
fixtures:
	$(BIN)/python scripts/check_fixtures.py

build:
	$(BIN)/mkdocs build --strict

# Internal links only (no --check-extern), so checks send no traffic to other sites.
links: build
	$(BIN)/linkchecker --no-status site/index.html
