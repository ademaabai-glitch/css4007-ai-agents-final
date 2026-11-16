# Project Proposal — Semester Week 10

# Project Proposal

## Project Title

ShopBuddy: an LLM shopping assistant that searches several local shops, checks stock and delivery, and prepares an order draft

## Problem Description

Small businesses in Kazakhstan (flower shops, clothing and accessory boutiques) mostly sell through social networks and messengers. A buyer who wants, for example, a bouquet for tomorrow must message many shops one by one, wait for replies, and often learns that the item is not in stock. This takes a lot of time and the search has to be repeated.

The application is one conversational entry point. The user describes what they need (item, budget, date, district). The agent searches the catalogues of several shops, checks availability, estimates delivery, asks for missing details, and prepares an order draft only after the user confirms it.

Important limits: all shops, products and users are fictional. The application does not connect to real shops, does not take payments and does not send real orders. An order is a local draft file. The data layer is designed so a real source could replace the JSON files later.

## Target Users

- Buyers who want to find and order a gift, clothes or accessories quickly without writing to many shops.
- In the future, small shop owners who would publish their catalogue in one common format.

## Selected Difficulty

A

Plan: first reach a working C-level agent (tools, validation, logs, 8 tests) by semester Week 14, then add the A-level parts (state, planning, execution limits, approval and guardrails, 12 tests, paper) in Weeks 14-16.

## Expected Functionality

- Natural-language product search across several fictional shops (flowers, clothing, accessories).
- Filters by budget, category, size, colour and district.
- Stock check for a chosen product in a chosen shop.
- Delivery cost and time estimate by district and requested date.
- Clarifying questions when information is missing (budget, date, address, size).
- If an item is unavailable, the agent proposes the next best option from another shop.
- Order draft saved as a local JSON file, created only after explicit user confirmation.
- Conversation memory (current request) and user memory (reply language, preferred district, clothing size) saved between runs.
- Execution log of every model request and tool result.
- Guardrails: no invented products or prices, no order without confirmation, loop limit, protection against instructions hidden in product descriptions.

## Proposed Functions

Data layer: `data/shops.json` holds shops (id, name, category, districts served, delivery rules) and their products (id, name, category, price_kzt, stock, attributes such as size and colour, description).

```python
def search_products(query: str, category: str | None = None,
                    max_price: int | None = None, district: str | None = None,
                    limit: int = 5) -> list[dict]:
    """Searches the fictional catalogues and returns matching products."""
```
- Purpose: find candidate products across all shops.
- Input: free-text query, optional category, maximum price in tenge, delivery district, result limit.
- Output: list of dicts (product_id, shop_id, name, price_kzt, short description). An error dict for invalid arguments.
- Dependencies: `data/shops.json`.

```python
def check_stock(shop_id: str, product_id: str, quantity: int = 1) -> dict:
    """Checks whether the product is available in the requested quantity."""
```
- Purpose: confirm availability before an order.
- Input: shop id, product id, quantity.
- Output: dict with status (`in_stock`, `low_stock`, `out_of_stock`, `unknown`), available quantity. An error dict for unknown ids.
- Dependencies: `data/shops.json` and a stock snapshot.

```python
def estimate_delivery(shop_id: str, district: str, date: str) -> dict:
    """Estimates delivery cost and whether the requested date is possible."""
```
- Purpose: tell the user the cost and whether delivery on time is possible.
- Input: shop id, district, requested date (YYYY-MM-DD).
- Output: dict with cost_kzt, earliest_date, possible (bool). Error dict if the district is not served.
- Dependencies: delivery rules in `data/shops.json`.

```python
def create_order_draft(user_id: str, items: list[dict], district: str,
                       date: str, confirmed: bool) -> dict:
    """Saves a local order draft. Refuses if the user has not confirmed."""
```
- Purpose: produce the final draft.
- Input: user id (set by the program), items (product id, shop id, quantity), district, date, confirmation flag.
- Output: dict with order id and file path, or `created: false` with a list of what is missing.
- Dependencies: file system (`outputs/orders/`), stock check.

```python
def save_user_preference(key: str, value: str) -> dict:
    """Saves one allowed preference for the current user."""
```
- Purpose: user memory (reply language, district, clothing size).
- Input: key from an allowed list, short value.
- Output: dict saved true/false.
- Dependencies: SQLite user memory keyed by user id.

## Proposed Agent Tools

| Tool | Why the agent needs it |
|---|---|
| `search_products` | The model cannot know the catalogues. It must retrieve real items instead of inventing them. |
| `check_stock` | Availability changes and decides the next step (offer another shop or continue). |
| `estimate_delivery` | Delivery cost and date decide whether an option fits the user's request. |
| `create_order_draft` | The only action with a side effect. It is guarded by the confirmation rule. |
| `save_user_preference` | Lets the agent remember allowed preferences between conversations. |

The model only requests tools. The program executes them and sets `user_id`, `thread_id` and the data snapshot, so the model cannot choose whose data is used.

## Model Selection

OpenAI API, model `gpt-4o-mini` (tool calling), temperature 0, through LangChain and LangGraph (same setup as HW5). The key is read from an environment variable and `.env` is ignored by Git. Tests use a clearly labelled fake model and need no API key. [Update here if the model changes.]

## Architecture

```
user message
   │
   ▼
START → agent (LLM) ─┬─ no tool calls ───────────────→ END (answer)
           ▲         ├─ tool calls, rounds < limit ──→ run_tools (program)
           │         │        │  validate arguments, check permissions
           └─────────┘        │  run tool, log result
                     └─ limit reached ───────────────→ stop with message
```

- Conversation state (messages, current request, rounds) is saved by the LangGraph checkpointer in SQLite, keyed by `thread_id`.
- User memory is a separate SQLite table keyed by `user_id`.
- Guardrails run in `run_tools`: argument validation, confirmation check before `create_order_draft`, round limit, rejection of tool names that do not exist.
- Data source sits behind one module, so JSON files can later be replaced by a real source.

## Example Requests

1. "I need a bouquet under 15,000 tenge for tomorrow, delivery to Medeu district." The agent searches flower shops, checks stock, estimates delivery, offers options and asks for confirmation.
2. "Find a black dress, size M, and a silver necklace from the same shop if possible." The agent searches clothing and accessories, compares shops, and reports if no single shop has both.
3. "The roses you found are out of stock. What else is available?" The agent checks stock, finds an alternative in another shop and says honestly if nothing fits.
4. (Edge case) "Order it now" with no item chosen. The agent must ask what to order and must not create a draft.

## Evaluation Plan

- Unit tests for each tool called directly (valid input, unknown id, bad arguments, empty results).
- Routing and loop tests with a fake model (tool is chosen, loop limit works, unknown tool name is rejected).
- Guardrail tests: no draft without confirmation, no draft for an out-of-stock item, prompt injection in a product description is ignored, delivery to an unserved district is refused.
- Memory tests with separate Python processes: data survives a restart, users and conversations stay separate.
- A set of about 15 scripted scenarios run with the real model; results logged in `outputs/` and described honestly, including failures.
- Targets: at least 12 tests (4 guardrail) in CI without an API key; scenario success rate reported with run-to-run differences.

## Weekly Milestones

| Semester week | Plan |
|---|---|
| 10 (2-8 Nov) | Proposal written (submitted late, on 16 Nov). |
| 11 (9-15 Nov) | Not completed in this window. The first LLM request is done together with Week 12. |
| 12 (16-22 Nov) | Repository setup, fictional data, first LLM call, `search_products` and `check_stock`, first tests. |
| 13 (23-29 Nov) | `estimate_delivery`, `create_order_draft`, model-chosen tool calls, argument validation. |
| 14 (30 Nov-6 Dec) | Full tool loop with logs, memory, C-level baseline; select recent research paper. |
| 15 (7-13 Dec) | Guardrails, execution limits, approval step, tracing, failure handling, 12 tests. |
| 16 (14-20 Dec) | Full evaluation, failure analysis, improvements, paper presentation preparation. |
| 17 (21-22 Dec) | Final README, final report, commit hash, demonstration and defense. |
