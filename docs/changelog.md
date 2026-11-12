# Changelog

Changes to this documentation site. The site is versioned on its own. Open Library does not version its API.

## 0.3.0 (2026-11-11)

### Added

- "Browse by subject" section in [Search for books](guides/search-books.md), and `/subjects/{subject}.json` in the [API reference](reference.md).
- Saved live responses in `openapi/fixtures/`, checked against the spec by `make fixtures` on every `make check`. This makes the "checked against live responses" claim repeatable offline.

### Changed

- The [information architecture](information-architecture.md) page no longer refers to pages as not yet published.

## 0.2.0 (2026-11-11)

### Added

- [Works, editions, and authors](concepts.md): the data model, with editions and ISBN lookup.
- Task guides: [Search for books](guides/search-books.md), [Get author details](guides/author-details.md), [Show cover images](guides/cover-images.md), [Page through results](guides/pagination.md), and [Handle errors and rate limits](guides/errors.md).
- [API reference](reference.md): a hand-written OpenAPI 3.1 description of the endpoints in the guides, checked against live responses.
- [Style guide](style-guide.md) and Vale rules that enforce it.
- `make check`: Vale, OpenAPI lint (Spectral), strict build, and link check.

### Changed

- Navigation now has Guides and Reference sections.
- The quickstart links to the guides.

## 0.1.0 (2026-11-11)

### Added

- Home page with an unofficial-docs notice.
- [Quickstart](quickstart.md): first search and work lookup with curl and Python.
- [Information architecture](information-architecture.md): readers, top tasks, and navigation design.
