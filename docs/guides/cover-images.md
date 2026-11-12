# Show cover images

Cover images come from a separate host, `covers.openlibrary.org`. You build the image URL yourself. There is no JSON step.

## Build the URL

```text
https://covers.openlibrary.org/{type}/{id_type}/{value}-{size}.jpg
```

| Part | Values |
|---|---|
| `type` | `b` for books, `a` for authors |
| `id_type` | `id` (a cover or photo ID), `isbn`, or `olid` (an Open Library ID, such as `OL33912545M`) |
| `size` | `S`, `M`, or `L` |

Where to get the value:

| You have | Use | Example |
|---|---|---|
| A search result | `cover_i` | `b/id/14627509-M.jpg` |
| A work or edition | `covers[0]` | `b/id/12013118-M.jpg` |
| An ISBN | The ISBN | `b/isbn/9780261103252-S.jpg` |
| An edition key | The ID after `/books/` | `b/olid/OL33912545M-L.jpg` |
| An author key | The ID after `/authors/` | `a/olid/OL26320A-M.jpg` |

Use `id` when you have it. It returns the image directly. In tests, `isbn` and `olid` URLs answered with a `302` redirect to `archive.org`, so your client must follow redirects.

```sh
curl -s -o /dev/null -A "openlibrary-unofficial-docs/0.1" \
  -w "%{http_code} %{content_type} %{redirect_url}\n" \
  "https://covers.openlibrary.org/b/isbn/9780261103252-S.jpg"
```

Output:

```text
302  https://archive.org/download/s_covers_0012/s_covers_0012_01.zip/0012013118-S.jpg
```

In an HTML `<img>` tag, the browser follows the redirect for you.

## Detect a missing cover

By default, a missing cover returns `200 OK` with a 1x1 blank GIF. Your app cannot tell it apart from a real cover by status code.

Add `?default=false` to get `404 Not Found` instead:

```sh
curl -s -o /dev/null -A "openlibrary-unofficial-docs/0.1" \
  -w "%{http_code} %{content_type}\n" \
  "https://covers.openlibrary.org/b/isbn/0000000000-M.jpg"
curl -s -o /dev/null -A "openlibrary-unofficial-docs/0.1" \
  -w "%{http_code} %{content_type}\n" \
  "https://covers.openlibrary.org/b/isbn/0000000000-M.jpg?default=false"
```

Output:

```text
200 image/gif
404 
```

## Download a cover in Python

```python
import requests

HEADERS = {"User-Agent": "openlibrary-unofficial-docs/0.1"}


def download_cover(cover_id, size="M"):
    url = f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"
    # default=false makes a missing cover return 404 instead of a blank image
    response = requests.get(url, params={"default": "false"}, headers=HEADERS, timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    path = f"cover-{cover_id}-{size}.jpg"
    with open(path, "wb") as f:
        f.write(response.content)
    return path, len(response.content)


print(download_cover(14627509))
```

Output:

```text
('cover-14627509-M.jpg', 16302)
```

The file is a 180 x 298 JPEG, the cover of *The Hobbit*. `requests` follows redirects by default, so the same function works with `isbn` or `olid` URLs.

## Author photos

Author records have a `photos` array of IDs. Use them with `a/id`, or use the author key with `a/olid`:

```text
https://covers.openlibrary.org/a/id/6155606-S.jpg
https://covers.openlibrary.org/a/olid/OL26320A-M.jpg
```

Both returned `200 OK` with a JPEG for J.R.R. Tolkien.
