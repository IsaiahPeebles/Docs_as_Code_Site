# Get author details

Works link to authors by key, such as `/authors/OL26320A`. This guide shows how to find an author key, then get the author's name, bio, and works.

## Find an author key by name

Use `GET /search/authors.json`.

```sh
curl -s -A "openlibrary-unofficial-docs/0.1" \
  "https://openlibrary.org/search/authors.json?q=tolkien&limit=2"
```

Output (trimmed):

```json
{
  "numFound": 29,
  "start": 0,
  "numFoundExact": true,
  "docs": [
    {
      "key": "OL14431239A",
      "name": "F. Tolkien",
      "top_work": "Thug Life",
      "work_count": 21
    },
    {
      "key": "OL26320A",
      "name": "J.R.R. Tolkien",
      "birth_date": "3 January 1892",
      "death_date": "2 September 1973",
      "top_work": "The Hobbit",
      "work_count": 346
    }
  ]
}
```

The best-known author is not always first. Use `top_work` and `work_count` to pick the right one.

!!! note
    Here `key` is a bare ID (`OL26320A`). Add the `/authors/` prefix to build the record URL.

If you already have a work, you do not need to search. Read the key from the work's `authors[].author.key`.

## Get the author and their works

| Endpoint | Returns |
|---|---|
| `GET /authors/{id}.json` | Name, dates, bio, alternate names, photo IDs, links |
| `GET /authors/{id}/works.json` | The author's works, in batches. Supports `limit` and `offset`. |

```python
import requests

BASE = "https://openlibrary.org"
HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}


def get(path, **params):
    response = requests.get(BASE + path, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def text(value):
    # bio and description can be a plain string or {"type": "/type/text", "value": "..."}
    return value["value"] if isinstance(value, dict) else value


author = get("/authors/OL26320A.json")
print(author["name"], f"({author.get('birth_date')} to {author.get('death_date')})")
print(text(author.get("bio", ""))[:100] + "...")

works = get("/authors/OL26320A/works.json", limit=3)
print(f"{works['size']} works. First {len(works['entries'])}:")
for work in works["entries"]:
    print(" ", work["key"], work["title"])
```

Output:

```text
J.R.R. Tolkien (3 January 1892 to 2 September 1973)
John Ronald Reuel Tolkien (1892-1973) was a major scholar of the English language, specialising in O...
359 works. First 3:
  /works/OL46165393W Der Schmied von Großholzingen
  /works/OL46147739W El Hobbit
  /works/OL46147738W Los Hijos de Hurin
```

## Things to watch for

- **Text fields have two shapes.** For this author, `bio` is a plain string. For the work `/works/OL27448W`, `description` is an object: `{"type": "/type/text", "value": "..."}`. Handle both, as the `text()` helper above does.
- **Counts differ by endpoint.** Author search said `work_count: 346`. The works endpoint said `size: 359`. The search index and the records are updated at different times.
- **Works are not sorted by fame.** The first works returned were recent translations, not *The Hobbit*. To find an author's best-known works, use [search](search-books.md) with `author=` instead.
- **Optional fields can be missing.** Use `.get()` for `bio`, `birth_date`, and `death_date`.

## Get an author photo

`photos` holds photo IDs. To show a photo, see [Show cover images](cover-images.md#author-photos).
