# Semester Week 11 Progress Report



## Completed Work

- No code was committed during the Week 11 window (9-15 November 2026). The initial LLM integration was done on 16 November and belongs to Week 12 by date.
- Wrote the project proposal (`reports/proposal.md`) for ShopBuddy, a shopping assistant for local shops.
- Set up the Python environment (Python 3.15.2, virtual environment `.venv`).
- Installed `langchain-openai`, `python-dotenv` and `pytest`.
- Created `src/llm.py` to connect the OpenAI API using the `gpt-4o-mini` model.
- Added a system prompt that forbids inventing products, prices or stock.
- Implemented `ask()` with handling of empty input and model errors (bad key, network failure).
- Stored the API key in an ignored `.env` file and kept `.env.example` without secrets.
- Created `src/first_request.py` to send the first request from the command line.
- Wrote 3 tests with a labelled fake model (`tests/test_llm.py`) and ran them successfully.
- Pushed the files to GitHub.

## Important Commits

- Commit hash: 0383d88a70f64e374b74bd552ce3e65cb865e96f
- Description: Add first LLM request, system prompt, error handling and tests (made on 16 Nov)
- Link: https://github.com/ademaabai-glitch/css4007-ai-agents-final/commit/0383d88a70f64e374b74bd552ce3e65cb865e96f
- Files added:
  - `src/llm.py`
  - `src/first_request.py`
  - `tests/test_llm.py`
  - `requirements.txt`

## Current Functionality

- The program sends a user message to `gpt-4o-mini` and prints the reply.
- For example, for "I need a bouquet for tomorrow" the model answers that it has no shop data and asks for details instead of inventing products.
- Empty input does not call the model.
- Model failures return a clear message instead of crashing.
- All 3 tests pass without an API key.
- Shop data, tools and the agent loop are not implemented yet.

## Problems Encountered

- I started the project late, so the Week 11 window was missed.
- My `.env` file was first created with a wrong name, so the program could not find the API key.
- The first request failed with an authentication error until the key was entered correctly.
- The default Python on my Mac was too old (3.9.6) for the packages.

## Solutions

- Installed a newer Python and created a virtual environment; all packages installed successfully.
- Renamed `.env` and checked with `git status` that Git ignores it before committing.
- Replaced the API key and ran the request again successfully.
- Moved the fictional shop data and the first tools into Week 12.

## What I Learned

- How to connect the OpenAI API to a Python project and load the key from environment variables.
- Why secrets must stay out of Git, and how `.gitignore` protects them.
- How to write a system prompt that stops the model from inventing information.
- How to test code that calls an LLM by using a fake model, so tests need no API key.
- How to commit and push files to GitHub from the terminal.

## Next Week

- Create fictional shop data in `data/shops.json` (3-4 shops: flowers, clothing, accessories).
- Implement `search_products()` and `check_stock()` with input validation.
- Add tests for both functions.
- Prepare the functions to be exposed as LLM tools.
