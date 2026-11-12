# Works, editions, and authors

Open Library stores books as three linked record types. Most calls return one of them, and most confusion comes from mixing them up.

| Record | What it is | Key format | Example |
|---|---|---|---|
| Work | A book in the abstract, across all its versions | `/works/OL...W` | `/works/OL27448W` (*The Lord of the Rings*) |
| Edition | One published version of a work, with its own ISBN, publisher, and page count | `/books/OL...M` | `/books/OL33912545M` (HarperCollins paperback, 2004) |
| Author | A person linked from works | `/authors/OL...A` | `/authors/OL26320A` (J.R.R. Tolkien) |

To get any record as JSON, add `.json` to its key: `https://openlibrary.org/works/OL27448W.json`.

## How the records link

```text
Author  <--  Work  <--  Edition
             authors[]   works[]
```

- A work lists its authors in `authors[].author.key`.
- An edition lists its work in `works[].key`.
- Links are keys, not names. To get a name or title, request the linked record.

## List the editions of a work

```sh
curl -s -A "openlibrary-unofficial-docs/0.1" \
  "https://openlibrary.org/works/OL27448W/editions.json?limit=2"
```

Output (trimmed):

```json
{
  "links": {
    "self": "/works/OL27448W/editions.json?limit=2",
    "work": "/works/OL27448W",
    "next": "/works/OL27448W/editions.json?limit=2&offset=2"
  },
  "size": 253,
  "entries": [
    {
      "key": "/books/OL62536872M",
      "title": "El seños de los anillos 2, las dos torres",
      "publishers": ["Booket"],
      "isbn_13": ["9788445077504"],
      "languages": [{"key": "/languages/spa"}],
      "works": [{"key": "/works/OL27448W"}]
    },
    {
      "key": "/books/OL62445425M",
      "title": "Il Signore degli Anelli",
      "publishers": ["Bompiani"],
      "isbn_13": ["978-8830119000"],
      "isbn_10": ["8830119008"],
      "works": [{"key": "/works/OL27448W"}]
    }
  ]
}
```

`size` is the total number of editions. Use `links.next` to get the next batch. See [Page through results](guides/pagination.md).

!!! note
    Edition data is entered by many contributors. Formats vary. In the output above, one ISBN has hyphens and one does not, and a Spanish edition is linked to the whole trilogy.

## Look up an edition by ISBN

`/isbn/{isbn}.json` accepts an ISBN-10 or ISBN-13. It answers with a redirect to the edition's `/books/` key, so tell your client to follow redirects (`-L` in curl).

```sh
curl -sL -A "openlibrary-unofficial-docs/0.1" \
  "https://openlibrary.org/isbn/9780261103252.json"
```

Output (trimmed):

```json
{
  "key": "/books/OL33912545M",
  "title": "The Lord of the Rings",
  "publishers": ["HarperCollins"],
  "publish_date": "2004",
  "physical_format": "Paperback",
  "number_of_pages": 1031,
  "isbn_10": ["0261103253"],
  "covers": [12013118],
  "works": [{"key": "/works/OL27448W"}]
}
```

This edition has no `authors` field. Follow `works[0].key` to the work, then the work's `authors` to the author.

## Next steps

- [Search for books](guides/search-books.md) to find work keys.
- [Get author details](guides/author-details.md) to turn an author key into a name and bio.
