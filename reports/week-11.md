# Semester Week 11 Progress Report



## Completed Work

No code was committed during the Week 11 window (9-15 November 2026). The project proposal was written late, on 16 November. The initial LLM integration (`src/llm.py`, `src/first_request.py`, 3 tests with a fake model) was done on 16 November and belongs to Week 12 by date.

## Important Commits

- Commit hash: [fill in after commit]
- Description: Add first LLM request, system prompt, error handling and tests (made on 16 Nov)
- Link: [fill in]

## Current Functionality

The program sends one user message to gpt-4o-mini and prints the reply. Empty input and model failures (bad key, network error) are handled with a clear message. There are no tools or shop data yet.

## Problems Encountered

I started the project late, so the Week 11 window was missed.

## Solutions

I compressed the plan: Weeks 12-13 now cover the initial integration, fictional shop data and the first tools.

## What I Learned

How to load an API key from the environment and keep it out of Git, how to write a system prompt that forbids inventing products and prices, and how to test code that calls an LLM by using a clearly labelled fake model.

## Next Week

Create the fictional shop data (`data/shops.json`), implement `search_products` and `check_stock` with validation, and add tests.
