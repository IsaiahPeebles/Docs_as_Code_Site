# Open Library API: unofficial docs

!!! warning "Unofficial documentation"
    This is unofficial community documentation. It is not affiliated with or endorsed by Open Library or the Internet Archive. For the official docs, see <https://openlibrary.org/developers/api>.

The [Open Library](https://openlibrary.org) API has data about books, authors, and covers. This site covers the public read endpoints, which are free and need no API key.

## Start here

- [Quickstart](quickstart.md): make your first call in under 5 minutes with curl or Python.
- [Information architecture](information-architecture.md): who this site is for and how it is organized.

## What you can do with the API

| Task | Endpoint |
|---|---|
| Search for books | `GET /search.json` |
| Get a work (a book across all its editions) | `GET /works/{id}.json` |
| Look up an edition by ISBN | `GET /isbn/{isbn}.json` |
| Get an author | `GET /authors/{id}.json` |
| Browse books by subject | `GET /subjects/{subject}.json` |
| Get a cover image | `GET https://covers.openlibrary.org/b/{key}/{value}-{size}.jpg` |
