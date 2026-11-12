# Style guide

These rules keep the site consistent. Rules marked **Vale** are checked on every run of `make check`. The Vale rules live in `styles/OLDocs/`.

## Voice

- Write for a developer who wants to finish a task. Start with what to do, then explain.
- Use short sentences and the second person ("you").
- Use plain words. Say what a thing does, not how good it is.

| Rule | Instead of | Write | Check |
|---|---|---|---|
| No marketing words | `simply`, `easily`, `seamless`, `powerful`, `robust`, `leverage` | Say what happens | Vale: `OLDocs.Marketing` |
| No `please` in instructions | `Please send a User-Agent` | `Send a User-Agent` | Vale: `OLDocs.Please` |
| No Latin abbreviations | `e.g.`, `i.e.`, `etc.` | for example, that is, and so on | Vale: `OLDocs.Latin` |
| No wordy phrases | `in order to`, `utilize` | to, use | Vale: `OLDocs.Wordy` (warning) |
| No em dashes (U+2014) | A long dash between clauses | Split the sentence, or use a colon | Vale: `OLDocs.EmDash` |

## Headings

- Use sentence case: "Show cover images", not "Show Cover Images". Vale: `OLDocs.Headings`.
- Name guides with a verb and a task: "Get author details", not "Authors".

## Code samples

- Run every sample against the live API before you publish it.
- Show the real output. Trimming is fine. Label trimmed output "Output (trimmed)".
- Send `User-Agent: openlibrary-unofficial-docs/0.1`. Never put an email address or other personal details in a sample.
- Pass a timeout in every Python request.
- Keep requests polite: no more than 1 per second.

## Formatting

- Put endpoints, parameters, field names, and values in code: `/search.json`, `limit`, `numFound`.
- Use tables for parameters and fields.
- Use admonitions (`!!! note`, `!!! warning`) only for information a reader could miss and regret.

## Accuracy

- Say "observed" or "in tests" for behavior found by testing that the official docs do not state.
- Say what was not tested instead of guessing.
- Date facts that can change, such as result counts.
