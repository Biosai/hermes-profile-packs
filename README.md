# gh-pages

GitHub Pages for the Hermes Telegram mini-apps. Nothing here is built; files are served as they are.

- `model-map/` is the page behind the `/modelmap` command:
  https://biosai.github.io/hermes-profile-packs/model-map/

The page contains no data. The bot puts the data in the URL fragment (`#d=...`), which the
browser never sends to GitHub, and the page's Content-Security-Policy blocks every network request.

`.nojekyll` turns off Jekyll so the files are served unchanged.
