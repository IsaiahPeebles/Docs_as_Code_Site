# Page through results

List endpoints return results in batches. There are two styles.

| Endpoints | Batch size | Next batch | Total |
|---|---|---|---|
| `/search.json` | `limit` | `offset`, or `page` | `numFound` |
| `/works/{id}/editions.json`, `/authors/{id}/works.json` | `limit` | `links.next` in the response | `size` |

## Page through search results

Set `limit` to the batch size and `offset` to the index of the first result you want. `offset` starts at 0.

```python
import time

import requests

HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}
LIMIT = 3

for page in range(2):
    params = {"q": "dune", "fields": "key,title", "limit": LIMIT, "offset": page * LIMIT}
    response = requests.get(
        "https://openlibrary.org/search.json", params=params, headers=HEADERS, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    print(f"start={data['start']} of {data['numFound']}")
    for book in data["docs"]:
        print(" ", book["key"], book["title"])
    if data["start"] + LIMIT >= data["numFound"]:
        break
    time.sleep(1)  # stay under 1 request per second
```

Output:

```text
start=0 of 48279
  /works/OL893414W Dune
  /works/OL893461W Dune Messiah
  /works/OL893516W Children of Dune
start=3 of 48279
  /works/OL893515W God Emperor of Dune
  /works/OL893502W Heretics of Dune
  /works/OL893508W Chapterhouse Dune
```

The sample stops after two pages on purpose. This search has 48,279 matches, so loop over all of them only if you need them.

### `page` instead of `offset`

`page` counts from 1, in steps of `limit`. These two requests returned the same three results, and both had `start: 3`:

```text
/search.json?q=dune&fields=key,title&limit=3&offset=3
/search.json?q=dune&fields=key,title&limit=3&page=2
```

With `page`, the response field `offset` is `null`. Read `start` to know where the batch begins.

## Follow `links.next` on list endpoints

The editions and author works endpoints return a `links` object:

```sh
curl -s -A "openlibrary-unofficial-docs/0.1" \
  "https://openlibrary.org/authors/OL26320A/works.json?limit=2"
```

Output (trimmed):

```json
{
  "links": {
    "self": "/authors/OL26320A/works.json?limit=2",
    "author": "/authors/OL26320A",
    "next": "/authors/OL26320A/works.json?limit=2&offset=2"
  },
  "size": 359,
  "entries": [
    {"key": "/works/OL46165393W", "title": "Der Schmied von Großholzingen"},
    {"key": "/works/OL46147739W", "title": "El Hobbit"}
  ]
}
```

Request `https://openlibrary.org` + `links.next` to get the next batch.

## Tips

- Results can shift between requests as the catalog changes. Do not treat page boundaries as stable IDs.
- Send at most 1 request per second, or 3 per second if you identify your app. See [Handle errors and rate limits](errors.md).
- For large exports, Open Library asks you to use its [monthly data dumps](https://openlibrary.org/developers/dumps) instead of paging through the API.
