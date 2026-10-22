import os
import re
import httpx
from dotenv import load_dotenv

load_dotenv()

def _number(value, default=0):
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return value
    match = re.search(r"([0-9][0-9,]*)", str(value))
    return int(match.group(1).replace(",", "")) if match else default

def normalize_external_product(item, index=0):
    specs = item.get("specifications") or item.get("specs") or {}
    price = item.get("price") or item.get("current_price") or item.get("amount")

    retailer = item.get("retailer") or item.get("store") or item.get("source") or "External Store"

    return {
        "id": str(item.get("id") or f"external-{index}"),
        "name": item.get("name") or item.get("title") or "Unknown Product",
        "brand": item.get("brand") or "Unknown",
        "cpu": specs.get("cpu") or item.get("cpu") or "Not available",
        "ram_gb": _number(specs.get("ram") or item.get("ram"), 0),
        "storage_gb": _number(specs.get("storage") or item.get("storage"), 0),
        "gpu": specs.get("gpu") or item.get("gpu") or "Not available",
        "battery_wh": _number(specs.get("battery_wh") or item.get("battery_wh"), 0),
        "weight_kg": float(item.get("weight_kg") or 0),
        "prices": {retailer: _number(price, 0)},
        "rating": float(item.get("rating") or 0),
        "review_count": int(item.get("review_count") or 0),
        "reviews": item.get("reviews") or [],
        "image_url": item.get("image") or item.get("image_url"),
        "source": "external_api"
    }

async def search_products(query: str):
    url = os.getenv("PRODUCT_API_URL")
    key = os.getenv("PRODUCT_API_KEY")

    if not url:
        return None, {"mode": "demo_fallback", "reason": "PRODUCT_API_URL is not configured"}

    headers = {}
    if key:
        headers["Authorization"] = f"Bearer {key}"
        headers["X-API-Key"] = key

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params={"q": query}, headers=headers)
            response.raise_for_status()
            payload = response.json()

        items = payload.get("products") or payload.get("items") or payload.get("results") or []
        products = [normalize_external_product(item, i) for i, item in enumerate(items)]
        products = [p for p in products if p["name"] != "Unknown Product"]

        if not products:
            return None, {"mode": "demo_fallback", "reason": "API returned no usable products"}

        return products, {
            "mode": "external_api",
            "provider_url": url,
            "products_found": len(products)
        }

    except Exception as exc:
        return None, {
            "mode": "demo_fallback",
            "reason": f"External product API unavailable: {str(exc)[:120]}"
        }
