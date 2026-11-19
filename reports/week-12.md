# Semester Week 12 Progress Report


## Completed Work

- Created a fictional dataset `data/shops.json`: 4 shops (2 flower shops, 1 clothing shop, 1 accessories shop), 40 products and delivery rules by Almaty district.
- Added test situations to the data: out-of-stock products, the same product in two shops, districts that some shops do not serve, and a product description with a hidden instruction to the assistant (for a later prompt-injection test).
- Created `src/data_store.py`, one module that reads the data, so the data source can be replaced later.
- Implemented `search_products()` in `src/tools.py`: text search with filters by category, maximum price and delivery district, with ranking and a result limit.
- Implemented `check_stock()` in `src/tools.py`: returns `in_stock`, `low_stock` or `out_of_stock` and whether the requested quantity is available.
- Added input validation: wrong types, unknown categories, districts or ids, negative prices and invalid quantities return an error message instead of crashing.
- Wrote 13 new tests in `tests/test_tools.py` and 2 more in `tests/test_llm.py`. All 16 tests pass without an API key.
- Pushed the work to GitHub in two commits.

## Important Commits

- Commit hash: [paste the full hash of "Add fictional shops dataset for ShopBuddy"]
- Description: Add fictional shops dataset for ShopBuddy
- Link: https://github.com/ademaabai-glitch/css4007-ai-agents-final/commit/[hash]
- Files added:
  - `data/shops.json`

- Commit hash: [paste the full hash of "Add search_products and check_stock tools with validation and tests"]
- Description: Add search_products and check_stock tools with validation and tests
- Link: https://github.com/ademaabai-glitch/css4007-ai-agents-final/commit/[hash]
- Files added or changed:
  - `src/data_store.py`
  - `src/tools.py`
  - `tests/test_tools.py`
  - `tests/test_llm.py`

## Current Functionality

- The program can search the catalogues of all shops, for example "black dress size M" or "bouquet under 10,000 tenge for Medeu district".
- A search with a district excludes shops that do not deliver there (for example, only one shop delivers to Turksib).
- If nothing matches, the search returns an empty result, and an invalid argument returns an error. These two cases are different.
- The stock check reports availability and says when fewer items are left than requested.
- Both functions work on their own, without a model.
- The model does not call these functions yet. Delivery estimate, order draft and the tool loop are not implemented.
- 16 tests pass (Python 3.15.2, pytest).

## Problems Encountered

- Some files were created empty in the editor, so a test run found nothing to import.
- `shops.json` was first saved in the wrong folder (`diagnostic/data`) and then was empty.
- `git push` was rejected because I had edited a report on the GitHub website, so my computer did not have that commit.
- The search must handle plural words and filler words ("I need a bouquet").

## Solutions

- Wrote the files again from the terminal and checked their size with `wc -c`.
- Moved `shops.json` to `data/` and checked that it loads (4 shops, 40 products).
- Ran `git pull --rebase` and pushed again.
- Added a small word normalization and a list of filler words to the search, and tested it.

## What I Learned

- How to design tool functions with validation, so wrong input returns a clear error and nothing crashes.
- Why it is better for a tool to return an empty result and an error separately.
- How to keep the data behind one module so the source can be replaced later.
- How to test tools without a model and without an API key.
- How to fix a rejected push with `git pull --rebase`.

## Next Week

- Implement `estimate_delivery()` (cost and earliest date by district) and `create_order_draft()` (local file, only after user confirmation).
- Connect the tools to the model so the model chooses which tool to call.
- Add the tool loop with a round limit and argument validation before execution.
- Add tests for the new tools and for the loop with a fake model.
