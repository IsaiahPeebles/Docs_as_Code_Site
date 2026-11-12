# Handle errors and rate limits

The API does not use one error format. This page lists what was observed on 2026-11-11 and how to handle each case.

## What errors look like

| Request | Status | Body |
|---|---|---|
| Missing work, such as `/works/OL0000000000W.json` | `404` | `{"error": "notfound", "key": "/works/OL0000000000W"}`, with no `Content-Type` header |
| Missing ISBN, such as `/isbn/0000000000.json` | `404` | An HTML page, not JSON |
| `/search.json` with no query | `200` | `numFound: 0` and empty `docs` |
| Missing cover with `?default=false` | `404` | Empty |
| Missing cover without `default=false` | `200` | A 1x1 blank GIF |
| `/isbn/{isbn}.json` that exists | `302` | Redirect to `/books/{id}.json` |

What this means for your code:

- **Check the status code before you parse.** A 404 body can be HTML, so `response.json()` can fail.
- **Do not read the `Content-Type` header to decide.** The work 404 above has no `Content-Type` header at all.
- **Follow redirects.** ISBN lookups and some cover URLs redirect.
- **Treat an empty search as "no results", not as an error.**

## Return `None` for a missing record

```python
import requests

HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}


def get_work(work_id):
    url = f"https://openlibrary.org/works/{work_id}.json"
    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


work = get_work("OL0000000000W")
print("Not found" if work is None else work["title"])
```

Output:

```text
Not found
```

`raise_for_status()` raises an exception for any other 4xx or 5xx status, so failures are not silent.

## Rate limits

Open Library's [usage guidelines](https://openlibrary.org/developers/api) set these limits:

| Your requests | Limit |
|---|---|
| No identification | 1 request per second |
| `User-Agent` with your app name and a contact email | 3 requests per second |

Example identified `User-Agent`: `MyApp/1.0 (you@example.org)`.

The guidelines also say:

- Cache responses when you can.
- Use `/search.json` for batch results instead of hundreds of single-record requests.
- Do not scrape HTML pages or spread requests across many IP addresses.
- Use the [monthly data dumps](https://openlibrary.org/developers/dumps) for bulk data.

Violations can lead to stricter rate limits or a block.

!!! note "Not tested here"
    This site did not test what happens when you go over the limit, because that would break the guidelines above. If a request fails with a 429 or 5xx status, wait a few seconds before you retry, and slow down.

## Set a timeout

Always pass a timeout. The samples on this site use `timeout=10` seconds. Without one, a slow response can hang your app.
