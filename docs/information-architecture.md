# Information architecture

This page explains who this site is for, what they need to do, and how the site is organized to help them do it.

## Readers

| Reader | Goal | What they need from the docs |
|---|---|---|
| App developer | Add book search or book details to an app or website. | A fast first call, copy-paste samples, and clear field meanings. |
| Data hobbyist or student | Pull book or author data into a script or notebook. | Python samples, pagination, and how to stay within polite use. |
| Librarian or researcher | Look up records by ISBN, author, or subject. | Lookup by identifier, and how works, editions, and authors relate. |

All three readers share the same first question: "How do I get data about a book?" The site answers that first.

## Top tasks

These tasks come from what the live API offers. Tasks 1 to 6 map to endpoints that were called and returned data on 2026-11-11. Tasks 7 and 8 are behaviors of those endpoints and will be tested in their guides.

| # | Task | Endpoint |
|---|---|---|
| 1 | Search for books by title, author, or text | `GET /search.json` |
| 2 | Get details for one book (a work) | `GET /works/{id}.json` |
| 3 | Look up a specific edition by ISBN | `GET /isbn/{isbn}.json` |
| 4 | Get author details | `GET /authors/{id}.json` |
| 5 | Show a cover image | `GET https://covers.openlibrary.org/b/{key}/{value}-{size}.jpg` |
| 6 | Browse books by subject | `GET /subjects/{subject}.json` |
| 7 | Page through large result sets | `limit` and `offset` on search |
| 8 | Handle errors and use the API politely | `User-Agent` header, status codes |

Search comes first because almost every other task starts with a key that search returns.

## The core concept: works, editions, and authors

Most confusion with this API comes from its data model. The site explains it once and links to it from every guide.

- A **work** is a book in the abstract, such as *The Lord of the Rings*. Key format: `/works/OL...W`.
- An **edition** is one published version of a work, with its own ISBN. Key format: `/books/OL...M`.
- An **author** is linked from works by key, not by name. Key format: `/authors/OL...A`.

## Navigation design

The site uses four top-level sections, ordered by when a reader needs them.

```text
Home
Get started
  Quickstart
  Works, editions, and authors
Guides
  Search for books
  Get author details
  Show cover images
  Page through results
  Handle errors and rate limits
Reference
  API reference (OpenAPI)
About this site
  Information architecture
  Style guide
  Changelog
```

Every page in this tree is published.

## Why this structure

- **Task-first guides.** Readers arrive with a task, not an endpoint name. Guide titles start with a verb and name the task.
- **Quickstart before concepts.** A working call builds trust. The data model page comes second, once the reader has seen a real key.
- **Reference is separate from guides.** Guides show one path through a task. The reference lists every parameter and field. Mixing them makes both harder to scan.
- **Shallow navigation.** No section is more than two levels deep, so every page is reachable from the sidebar.
- **Meta pages stay out of the way.** The style guide, changelog, and this page go under "About this site", last in the sidebar. Most readers never need them.

## How this differs from the official docs

The [official API docs](https://openlibrary.org/developers/api) start with usage guidelines and rate limits, then an index of APIs organized by data type (search, covers, works and editions, and so on). They also link to an interactive OpenAPI page.

This site takes a different angle. It groups content by reader task, starts with one tested end-to-end call, and shows real output for every sample.
