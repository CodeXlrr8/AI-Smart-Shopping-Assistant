from __future__ import annotations
import os
from datetime import datetime
from typing import Any

import httpx
from dotenv import load_dotenv
from sqlalchemy import update

from db import SessionLocal, PriceAlert, PriceSnapshot
from data import DEMO_PRODUCTS

load_dotenv()


def _authorized_api_prices(product_id: str) -> dict[str, float]:
    url = os.getenv('PRODUCT_API_URL', '').strip()
    key = os.getenv('PRODUCT_API_KEY', '').strip()
    if not url:
        return {}
    headers = {'Authorization': f'Bearer {key}'} if key else {}
    if key:
        headers['X-API-Key'] = key
    try:
        r = httpx.get(url, params={'product_id': product_id}, headers=headers, timeout=15)
        r.raise_for_status()
        payload = r.json()
        items = payload.get('products') or payload.get('items') or payload.get('results') or []
        prices: dict[str, float] = {}
        for item in items:
            pid = str(item.get('id') or item.get('sku') or '')
            if pid != product_id:
                continue
            if item.get('prices'):
                prices = {str(k): float(v) for k, v in item['prices'].items() if float(v) > 0}
            elif item.get('price'):
                prices[str(item.get('store') or 'API')] = float(item['price'])
        return prices
    except Exception:
        return {}


def current_prices(product_id: str) -> dict[str, float]:
    prices = _authorized_api_prices(product_id)
    if prices:
        return prices
    for product in DEMO_PRODUCTS:
        if product['id'] == product_id:
            return {k: float(v) for k, v in product.get('prices', {}).items() if v > 0}
    return {}


def check_price_alerts() -> dict[str, Any]:
    db = SessionLocal()
    checked = triggered = 0
    try:
        alerts = db.query(PriceAlert).filter(PriceAlert.active.is_(True), PriceAlert.triggered.is_(False)).all()
        for alert in alerts:
            prices = current_prices(alert.product_id)
            checked += 1
            if not prices:
                continue
            now = datetime.utcnow()
            for store, price in prices.items():
                db.add(PriceSnapshot(product_id=alert.product_id, store=store, price=price, captured_at=now))
            if min(prices.values()) <= alert.target_price:
                alert.triggered = True
                triggered += 1
        db.commit()
        return {'checked': checked, 'triggered': triggered}
    finally:
        db.close()
