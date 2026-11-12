# Search for books

Use `GET /search.json` to find works by title, author, or free text. Each result is a work. See [Works, editions, and authors](../concepts.md).

## Choose how to search

| Parameter | Matches | Example |
|---|---|---|
| `q` | Any text: title, author, subject | `q=the lord of the rings` |
| `title` | The title only | `title=the hobbit` |
| `author` | The author name only | `author=tolkien` |

You can combine `title` and `author` to narrow results.

## Ask only for the fields you need

Without `fields`, each result has dozens of fields, including long lists of ISBNs. Set `fields` to a comma-separated list to keep responses small.

Useful fields:

| Field | Type | Meaning |
|---|---|---|
| `key` | string | Work key, such as `/works/OL27482W` |
| `title` | string | Work title |
| `author_name` | array of strings | Author names |
| `author_key` | array of strings | Author IDs, such as `OL26320A`, without the `/authors/` prefix |
| `first_publish_year` | integer | Year of the first edition |
| `edition_count` | integer | Number of editions |
| `cover_i` | integer | Cover ID. See [Show cover images](cover-images.md). |
| `isbn` | array of strings | ISBNs of all editions. Can be very long. |

## Search by title and author

=== "curl"

    ```sh
    curl -s -A "openlibrary-unofficial-docs/0.1" \
      "https://openlibrary.org/search.json?title=the+hobbit&author=tolkien&fields=key,title,author_name,author_key,first_publish_year,edition_count,cover_i,isbn&limit=2"
    ```

    Output (trimmed):

    ```json
    {
      "numFound": 24,
      "start": 0,
      "numFoundExact": true,
      "q": "",
      "offset": null,
      "docs": [
        {
          "author_key": ["OL26320A"],
          "author_name": ["J.R.R. Tolkien"],
          "cover_i": 14627509,
          "edition_count": 482,
          "first_publish_year": 1937,
          "isbn": ["9780613870665", "0061952842", "..."],
          "key": "/works/OL27482W",
          "title": "The Hobbit"
        }
      ]
    }
    ```

    `q` is empty because this search used `title` and `author` instead.

=== "Python"

    ```python
    import requests

    HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}
    params = {
        "title": "the hobbit",
        "author": "tolkien",
        "fields": "key,title,author_name,first_publish_year,edition_count",
        "limit": 3,
    }

    response = requests.get(
        "https://openlibrary.org/search.json", params=params, headers=HEADERS, timeout=10
    )
    response.raise_for_status()
    data = response.json()

    print(f"Found {data['numFound']} works")
    for book in data["docs"]:
        print(f"{book['key']}  {book['title']} ({book['first_publish_year']}), "
              f"{book['edition_count']} editions, by {', '.join(book['author_name'])}")
    ```

    Output:

    ```text
    Found 24 works
    /works/OL27482W  The Hobbit (1937), 482 editions, by J.R.R. Tolkien
    /works/OL219602W  The Hobbit (1990), 10 editions, by Charles Dixon, Sean Deming, J.R.R. Tolkien
    /works/OL14926019W  The Hobbit & The Lord of the Rings [collection/set] (1979), 27 editions, by J.R.R. Tolkien
    ```

Results include adaptations and box sets. Check `author_name` and `edition_count` to pick the work you want.

## Read the response

| Field | Meaning |
|---|---|
| `numFound` | Total number of matches |
| `start` | Index of the first result in this response |
| `docs` | The results |

The response also has `num_found` (same value as `numFound`), `q`, `offset`, and `documentation_url`.

## An empty search is not an error

A request to `/search.json` with no parameters returns `200 OK` with no results. Output (trimmed):

```json
{"numFound": 0, "start": 0, "numFoundExact": true, "q": "", "offset": null, "docs": []}
```

Check `numFound` before you read `docs`.

## Browse by subject

To list works on a topic instead of searching for text, use `GET /subjects/{subject}.json`. Write the subject in lowercase, with underscores for spaces: `science_fiction`.

```python
import requests

HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}

response = requests.get(
    "https://openlibrary.org/subjects/science_fiction.json",
    params={"limit": 3},
    headers=HEADERS,
    timeout=10,
)
response.raise_for_status()
data = response.json()

print(f"{data['name']}: {data['work_count']} works")
for work in data["works"]:
    authors = ", ".join(a["name"] for a in work["authors"])
    print(f"{work['key']}  {work['title']} ({work['first_publish_year']}) by {authors}")
```

Output:

```text
science fiction: 21278 works
/works/OL138052W  Alice's Adventures in Wonderland (1865) by Lewis Carroll
/works/OL450063W  Frankenstein; or, The Modern Prometheus (1818) by Mary Shelley
/works/OL18417W  The Wonderful Wizard of Oz (1899) by L. Frank Baum
```

Subject results differ from search results:

- The total is `work_count`, and the results are in `works`, not `docs`.
- Each work has `authors` as objects with `key` and `name`, so you get author names without a second request.
- The cover ID is `cover_id`, not `cover_i`.

## Next steps

- [Page through results](pagination.md) to get more than one page.
- [Get author details](author-details.md) for the authors in `author_key`.
