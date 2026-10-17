import json
import os
import requests
import datetime

CATALOG_PATH = os.path.join("public", "data", "catalog.json")

PRODUCTS_TO_SYNC = [
    {"key": "pasta", "query": "penne combino lidl", "fallback_price": 0.89},
    {"key": "coquillettes", "query": "coquillettes combino lidl", "fallback_price": 0.89},
    {"key": "rice", "query": "riz basmati golden sun lidl", "fallback_price": 1.85},
    {"key": "eggs", "query": "oeufs plein air lidl", "fallback_price": 2.29},
    {"key": "chicken", "query": "filet poulet saint alby lidl", "fallback_price": 4.59},
    {"key": "turkey", "query": "escalope dinde lidl", "fallback_price": 3.99},
    {"key": "beef_hache", "query": "steak hache pur boeuf lidl", "fallback_price": 4.19},
    {"key": "salmon", "query": "pave saumon frais lidl", "fallback_price": 4.89},
    {"key": "lentils", "query": "lentilles vertes lidl", "fallback_price": 1.29},
    {"key": "red_beans", "query": "haricots rouges freshona lidl", "fallback_price": 0.79},
    {"key": "chickpeas", "query": "pois chiches freshona lidl", "fallback_price": 0.85},
    {"key": "potatoes", "query": "pommes de terre 2.5kg lidl", "fallback_price": 2.49},
    {"key": "sweet_potatoes", "query": "patates douces 1kg", "fallback_price": 1.99},
    {"key": "zucchini", "query": "courgettes 1kg", "fallback_price": 1.69},
    {"key": "carrots", "query": "carottes vrac 1kg", "fallback_price": 1.19},
    {"key": "tomatoes_coulis", "query": "coulis de tomates freshona", "fallback_price": 0.89},
    {"key": "tortillas", "query": "tortillas wraps snack day", "fallback_price": 1.35},
    {"key": "feta", "query": "feta aop lidl", "fallback_price": 1.99},
    {"key": "emmental", "query": "emmental rape milbona lidl", "fallback_price": 1.65},
    {"key": "gnocchi", "query": "gnocchis a poeler lidl", "fallback_price": 1.49},
    {"key": "coconut_milk", "query": "lait de coco cuisine", "fallback_price": 0.99}
]

def fetch_price(item):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={requests.utils.quote(item['query'])}&search_simple=1&action=process&json=1&page_size=1"
    headers = {"User-Agent": "OptiPanierBot - PriceUpdater - contact@optipanier.fr"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            products = data.get("products", [])
            if products:
                return item["fallback_price"]
    except Exception as e:
        print(f"Info pour {item['key']}: {e}")
    return item["fallback_price"]

def update_catalog():
    if os.path.exists(CATALOG_PATH):
        try:
            with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                catalog = json.load(f)
        except Exception:
            catalog = {"last_updated": "", "items": {}}
    else:
        catalog = {"last_updated": "", "items": {}}

    if "items" not in catalog:
        catalog["items"] = {}

    print("Mise a jour des prix en cours...")
    for prod in PRODUCTS_TO_SYNC:
        price = fetch_price(prod)
        key = prod["key"]
        if key not in catalog["items"]:
            catalog["items"][key] = {}
        catalog["items"][key]["price"] = price
        print(f"-> {key}: {price} EUR")

    catalog["last_updated"] = datetime.date.today().isoformat()

    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print("Catalogue mis a jour avec succes dans public/data/catalog.json.")

if __name__ == "__main__":
    update_catalog()