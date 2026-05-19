# Citation Updates

This homepage syncs selected citation counts from Google Scholar through GitHub Actions.

## How It Works

- `scripts/fetch_citations.py` reads Boyuan Jiang's public Google Scholar profile.
- `.github/workflows/update-citations.yml` runs the script every day at 08:00 UTC, on manual dispatch, and when the citation workflow/script changes.
- The script writes both `_data/citations.json` and `assets/js/citations-data.js`.
- `index.html` loads `assets/js/citations-data.js` before `assets/js/main.js`, so citation badges also work when the page is opened as a local static file.
- Only papers with `data-citation-key` in `index.html` display citation badges. The current tracked papers are STM and IFRNet.

## Add A Paper

1. Add a key and title to `PAPERS` in `scripts/fetch_citations.py`.
2. Add the same key to the paper card in `index.html`:

```html
<article class="paper-item" data-citation-key="paper-key">
```

3. Run:

```bash
python3 -m pip install scholarly requests
python3 scripts/fetch_citations.py
```

GitHub Actions will keep the counts fresh after deployment.
