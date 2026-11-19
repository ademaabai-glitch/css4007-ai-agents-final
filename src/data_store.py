"""Reads the fictional shop data. All tools use this one module, so the data source can be replaced later."""
import json
import os
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_shops() -> list:
    """Returns the list of shops from shops.json (path can be changed with SHOPBUDDY_DATA_DIR)."""
    data_dir = Path(os.environ.get("SHOPBUDDY_DATA_DIR") or DEFAULT_DATA_DIR)
    data = json.loads((data_dir / "shops.json").read_text(encoding="utf-8"))
    return data["shops"]


def get_shop(shop_id: str):
    return next((s for s in load_shops() if s["shop_id"] == shop_id), None)


def get_product(shop_id: str, product_id: str):
    shop = get_shop(shop_id)
    if shop is None:
        return None
    return next((p for p in shop["products"] if p["product_id"] == product_id), None)


def all_districts() -> list:
    names = set()
    for shop in load_shops():
        names.update(shop["delivery"]["districts"])
    return sorted(names)
