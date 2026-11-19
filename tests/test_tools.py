"""Tests for the shop tools. No model and no API key are needed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_store import load_shops
from tools import check_stock, search_products


def test_data_file_is_valid():
    shops = load_shops()
    ids = [p["product_id"] for s in shops for p in s["products"]]
    assert len(shops) >= 3 and len(ids) == len(set(ids))


def test_search_finds_red_roses():
    r = search_products("red roses")
    assert r["count"] > 0 and "roses" in r["results"][0]["name"].lower()


def test_search_respects_budget():
    r = search_products("bouquet", category="flowers", max_price=10000)
    assert r["count"] > 0 and all(x["price_kzt"] <= 10000 for x in r["results"])


def test_search_category_filter():
    r = search_products("silver", category="accessories")
    assert r["count"] > 0 and all(x["category"] == "accessories" for x in r["results"])


def test_search_district_without_delivery_excludes_shop():
    r = search_products("dress", district="Turksib")      # only Urban Thread delivers to Turksib
    assert r["count"] > 0 and {x["shop_id"] for x in r["results"]} == {"SHOP-CL1"}


def test_search_nothing_found_is_empty_not_error():
    assert search_products("spaceship") == {"count": 0, "results": []}


def test_search_rejects_bad_arguments():
    assert "error" in search_products("roses", category="cars")
    assert "error" in search_products("roses", max_price=-5)
    assert "error" in search_products("roses", limit=0)
    assert "error" in search_products("roses", district="Atlantis")
    assert "error" in search_products("")
    assert "error" in search_products(12345)


def test_search_does_not_crash_on_strange_text():
    assert "error" not in search_products("'; DROP TABLE products; -- " * 20)


def test_stock_in_stock_low_and_out():
    assert check_stock("SHOP-FL1", "F1-103")["status"] == "in_stock"
    assert check_stock("SHOP-FL1", "F1-104")["status"] == "low_stock"
    assert check_stock("SHOP-FL2", "F2-201")["status"] == "out_of_stock"


def test_stock_quantity_more_than_available():
    r = check_stock("SHOP-FL1", "F1-104", quantity=5)      # only 3 left
    assert r["enough"] is False and r["available"] == 3


def test_stock_unknown_ids_and_bad_quantity():
    assert "error" in check_stock("SHOP-XX", "F1-101")
    assert "error" in check_stock("SHOP-FL1", "NOPE")
    assert "error" in check_stock("SHOP-FL1", "F2-201")    # product exists, but in another shop
    assert "error" in check_stock("SHOP-FL1", "F1-101", quantity=0)
    assert "error" in check_stock("SHOP-FL1", "F1-101", quantity=True)
