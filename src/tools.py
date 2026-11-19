"""ShopBuddy tools. Each one works on its own, without a model, and returns a dict (errors are {"error": ...})."""
import re

from data_store import all_districts, get_product, load_shops

CATEGORIES = ("flowers", "clothing", "accessories")
STOPWORDS = {"a", "an", "the", "for", "and", "or", "of", "in", "to", "with", "i", "need", "want", "find", "me", "some"}
LOW_STOCK_LIMIT = 3          # 1..3 items left counts as "low_stock"
MAX_TEXT = 100               # long strings are cut, inputs are only used for matching


def _tokens(text: str) -> set:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w[:-1] if len(w) > 3 and w.endswith("s") else w for w in words if w not in STOPWORDS}


def _stock_status(stock: int) -> str:
    if stock <= 0:
        return "out_of_stock"
    return "low_stock" if stock <= LOW_STOCK_LIMIT else "in_stock"


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def search_products(query: str = "", category: str = None, max_price: int = None,
                    district: str = None, limit: int = 5) -> dict:
    """Searches the fictional catalogues. Returns {"count": n, "results": [...]} or {"error": ...}."""
    if not isinstance(query, str):
        return {"error": "query must be a string"}
    query = query.strip()[:MAX_TEXT]
    if category is not None:
        if not isinstance(category, str) or category.strip().lower() not in CATEGORIES:
            return {"error": f"unknown category; use one of: {', '.join(CATEGORIES)}"}
        category = category.strip().lower()
    if max_price is not None and (not _is_int(max_price) or max_price <= 0):
        return {"error": "max_price must be a positive whole number (tenge)"}
    if not _is_int(limit) or not 1 <= limit <= 10:
        return {"error": "limit must be a whole number from 1 to 10"}
    if district is not None:
        known = {d.lower(): d for d in all_districts()}
        if not isinstance(district, str) or district.strip().lower() not in known:
            return {"error": f"unknown district; known districts: {', '.join(all_districts())}"}
        district = known[district.strip().lower()]
    wanted = _tokens(query)
    if not wanted and category is None:
        return {"error": "give a search text or a category"}

    results = []
    for shop in load_shops():
        if district and district not in shop["delivery"]["districts"]:
            continue                      # this shop does not deliver to the district
        for p in shop["products"]:
            if category and p["category"] != category:
                continue
            if max_price is not None and p["price_kzt"] > max_price:
                continue
            haystack = " ".join([p["name"], p["category"], p["description"],
                                 *[str(v) for v in p["attributes"].values()]])
            score = len(wanted & _tokens(haystack))
            if wanted and score == 0:
                continue
            results.append((score, p["price_kzt"], {
                "product_id": p["product_id"], "shop_id": shop["shop_id"], "shop_name": shop["name"],
                "name": p["name"], "category": p["category"], "price_kzt": p["price_kzt"],
                "stock_status": _stock_status(p["stock"]), "description": p["description"][:120]}))
    results.sort(key=lambda r: (-r[0], r[1]))
    top = [r[2] for r in results[:limit]]
    return {"count": len(top), "results": top}


def check_stock(shop_id: str, product_id: str, quantity: int = 1) -> dict:
    """Checks availability of one product in one shop."""
    if not isinstance(shop_id, str) or not isinstance(product_id, str):
        return {"error": "shop_id and product_id must be strings"}
    if not _is_int(quantity) or not 1 <= quantity <= 20:
        return {"error": "quantity must be a whole number from 1 to 20"}
    shops = {s["shop_id"] for s in load_shops()}
    if shop_id.strip() not in shops:
        return {"error": f"unknown shop_id '{shop_id[:MAX_TEXT]}'; known shops: {', '.join(sorted(shops))}"}
    product = get_product(shop_id.strip(), product_id.strip())
    if product is None:
        return {"error": f"product '{product_id[:MAX_TEXT]}' not found in shop {shop_id.strip()}"}
    available = product["stock"]
    return {"shop_id": shop_id.strip(), "product_id": product["product_id"], "name": product["name"],
            "status": _stock_status(available), "available": available,
            "requested": quantity, "enough": available >= quantity}
