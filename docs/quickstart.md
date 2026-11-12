# Quickstart

Find a book and get its details. This takes about 5 minutes.

You will:

1. Search for a book.
2. Get the full record for the book you found.

## Before you start

- You need `curl` or Python 3. The curl samples pipe into `python3 -m json.tool` only to pretty-print the output. You can drop the pipe.
- You do not need an API key or an account.
- Send a `User-Agent` header that names your app. The samples use `openlibrary-unofficial-docs/0.1`. Replace it with your own app name.

!!! tip "Rate limits"
    Open Library's [usage guidelines](https://openlibrary.org/developers/api) allow 1 request per second without identification. If your app makes regular calls, add a contact email to your `User-Agent`, for example `MyApp/1.0 (you@example.org)`. Identified requests get 3 requests per second.

## Step 1: Search for a book

Call `/search.json` with your search text in `q`. Use `fields` to get only the fields you need, and `limit` to cap the number of results.

=== "curl"

    ```sh
    curl -s -A "openlibrary-unofficial-docs/0.1" \
      "https://openlibrary.org/search.json?q=the+lord+of+the+rings&fields=key,title,author_name,first_publish_year&limit=2" \
      | python3 -m json.tool
    ```

    Output (trimmed):

    ```json
    {
        "numFound": 1105,
        "start": 0,
        "numFoundExact": true,
        "q": "the lord of the rings",
        "docs": [
            {
                "author_name": ["J.R.R. Tolkien"],
                "first_publish_year": 1954,
                "key": "/works/OL27448W",
                "title": "The Lord of the Rings"
            },
            {
                "author_name": ["J.R.R. Tolkien"],
                "first_publish_year": 1954,
                "key": "/works/OL27513W",
                "title": "The Fellowship of the Ring"
            }
        ]
    }
    ```

=== "Python"

    Install `requests`:

    ```sh
    pip install requests
    ```

    Save this as `search_books.py`:

    ```python
    import requests

    HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}
    params = {
        "q": "the lord of the rings",
        "fields": "key,title,author_name,first_publish_year",
        "limit": 3,
    }

    response = requests.get(
        "https://openlibrary.org/search.json",
        params=params,
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    print(f"Found {data['numFound']} matches")
    for book in data["docs"]:
        authors = ", ".join(book.get("author_name", ["unknown"]))
        print(f"{book['title']} ({book.get('first_publish_year')}) by {authors} -> {book['key']}")
    ```

    Run it:

    ```sh
    python3 search_books.py
    ```

    Output:

    ```text
    Found 1105 matches
    The Lord of the Rings (1954) by J.R.R. Tolkien -> /works/OL27448W
    The Fellowship of the Ring (1954) by J.R.R. Tolkien -> /works/OL27513W
    The Two Towers (1954) by J.R.R. Tolkien -> /works/OL27479W
    ```

Each result has a `key`, such as `/works/OL27448W`. A *work* is one book across all its editions. Use the key in the next step.

!!! note
    `numFound` and the order of results change as the catalog changes. Your numbers may differ.

## Step 2: Get the work

Add `.json` to the work key and request it.

```sh
curl -s -A "openlibrary-unofficial-docs/0.1" \
  "https://openlibrary.org/works/OL27448W.json"
```

Output (trimmed to a few fields):

```json
{
  "key": "/works/OL27448W",
  "title": "The Lord of the Rings",
  "authors": [
    {
      "author": {"key": "/authors/OL26320A"},
      "type": {"key": "/type/author_role"}
    }
  ],
  "subjects": [
    "The Lord of the Rings",
    "Fiction",
    "English Fantasy fiction",
    "..."
  ]
}
```

The full response also has `description`, `covers`, `first_publish_date`, `subject_places`, and more.

The author is a key, not a name. To get the name, request `/authors/OL26320A.json`.

## What you did

- Searched the catalog with `/search.json`.
- Got a full work record with `/works/{id}.json`.

## Next steps

- [Works, editions, and authors](concepts.md): how the records link.
- [Search for books](guides/search-books.md)
- [Get author details](guides/author-details.md)
- [Show cover images](guides/cover-images.md)
- [Page through results](guides/pagination.md)
- [Handle errors and rate limits](guides/errors.md)
