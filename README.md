# Open Library API: unofficial docs

Unofficial community documentation for the [Open Library](https://openlibrary.org) API, built as docs-as-code with MkDocs Material.

This project is not affiliated with or endorsed by Open Library or the Internet Archive.

## Run it locally

You need [uv](https://docs.astral.sh/uv/).

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/mkdocs serve -a 127.0.0.1:8802
```

Open <http://127.0.0.1:8802>.

## Run the checks

```sh
make check
```

This runs, in order:

| Step | Tool | What it checks |
|---|---|---|
| `make vale` | Vale (pip) | Prose against the [style guide](docs/style-guide.md), using rules in `styles/OLDocs/` |
| `make spec` | Spectral (via `npx`, needs Node) | `openapi/openlibrary.yaml` against the `spectral:oas` ruleset, failing on warnings |
| `make fixtures` | `scripts/check_fixtures.py` (jsonschema) | Saved live responses in `openapi/fixtures/` against the spec schemas, offline. Also fails if the spec documents a field no fixture has. |
| `make build` | MkDocs | `mkdocs build --strict`: broken internal links, anchors, and pages missing from nav |
| `make links` | LinkChecker (pip) | Every internal link in the built site. External links are not checked. |

The same checks run in GitHub Actions (`.github/workflows/check.yml`) once the repo is public.

## Layout

- `docs/`: the Markdown pages.
- `mkdocs.yml`: site config and navigation.
- `docs/guides/`: task guides.
- `openapi/openlibrary.yaml`: hand-written OpenAPI 3.1 description, rendered on the Reference page by `neoteroi-mkdocs`.
- `styles/OLDocs/`: Vale rules. `.vale.ini` turns them on.
- `openapi/fixtures/`: trimmed live responses (2026-11-11), one folder per schema.
- `scripts/check_fixtures.py`: validates the fixtures against the spec.
- `.spectral.yaml`: Spectral ruleset.
- `Makefile`: the checks.

## Contribute

1. Edit or add a page in `docs/`.
2. Run every code sample against the live API. Paste the real output.
3. If you change what an endpoint returns or accepts, update `openapi/openlibrary.yaml` to match the real response, and save a trimmed real response in `openapi/fixtures/<SchemaName>/`.
4. Add a line to `docs/changelog.md`.
5. Run `make check`. It must pass.

Author: Isaiah Peebles. License: the docs and the OpenAPI description are under [CC BY 4.0](LICENSE).
