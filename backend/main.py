from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy import desc
from apscheduler.schedulers.background import BackgroundScheduler

from graph import shopping_graph
from fake_review_ml import MODEL_SOURCE
from api_models import ShoppingRequest, AlertRequest
from db import SessionLocal, init_db, PriceSnapshot, PriceAlert, SearchLog
from price_worker import check_price_alerts

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    interval = 0
    try:
        import os
        interval = max(0, int(os.getenv('PRICE_CHECK_INTERVAL_MINUTES', '0')))
    except ValueError:
        interval = 0
    if interval > 0:
        scheduler.add_job(check_price_alerts, 'interval', minutes=interval, id='price-check', replace_existing=True)
        scheduler.start()
    yield
    if scheduler.running:
        scheduler.shutdown(wait=False)

app = FastAPI(title='AI Smart Shopping Assistant', version='7.0', lifespan=lifespan)
origins = [x.strip() for x in os.getenv('FRONTEND_URLS', '*').split(',') if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
def health():
    return {'status':'ok','version':'V7','features':['multi-agent research','ML suspicious-review detection','LLM explanations','price history','scheduled price checks','alerts','accessory recommendations']}

@app.get('/api/research-status')
def research_status():
    import os
    return {'supported_modes':['authorized external product API','demo fallback'],'llm_optional':True,'ml_review_detector':'TF-IDF + Logistic Regression', 'ml_model_source': MODEL_SOURCE,'scheduled_price_checks':bool(os.getenv('PRICE_CHECK_INTERVAL_MINUTES'))}

@app.post('/api/shop')
def shop(request: ShoppingRequest):
    if not request.query.strip(): raise HTTPException(status_code=400, detail='Query cannot be empty')
    result=shopping_graph.invoke({'query':request.query,'agent_steps':[]})
    db=SessionLocal()
    try:
        db.add(SearchLog(query=request.query,mode=result['research_metadata']['mode']))
        for p in result['ranked_products']:
            for store,price in (p.get('prices') or {}).items():
                if price>0: db.add(PriceSnapshot(product_id=p['id'],store=store,price=price))
        db.commit()
    finally: db.close()
    return {'user_profile':result['user_profile'],'research_metadata':result['research_metadata'],'agent_steps':result['agent_steps'],'products':result['ranked_products'],'recommendation':result['recommendation']}

@app.get('/api/products/{product_id}/price-history')
def price_history(product_id:str):
    db=SessionLocal()
    try:
        rows=db.query(PriceSnapshot).filter(PriceSnapshot.product_id==product_id).order_by(PriceSnapshot.captured_at.asc()).all()
        return {'product_id':product_id,'history':[{'store':r.store,'price':r.price,'captured_at':r.captured_at.isoformat()} for r in rows]}
    finally: db.close()

@app.post('/api/alerts')
def create_alert(req:AlertRequest):
    db=SessionLocal()
    try:
        alert=PriceAlert(product_id=req.product_id,target_price=req.target_price,email=req.email)
        db.add(alert); db.commit(); db.refresh(alert)
        return {'id':alert.id,'product_id':alert.product_id,'target_price':alert.target_price,'active':alert.active}
    finally: db.close()

@app.get('/api/alerts')
def list_alerts():
    db=SessionLocal()
    try:
        rows=db.query(PriceAlert).order_by(desc(PriceAlert.created_at)).all()
        return {'alerts':[{'id':r.id,'product_id':r.product_id,'target_price':r.target_price,'email':r.email,'active':r.active,'triggered':r.triggered,'created_at':r.created_at.isoformat()} for r in rows]}
    finally: db.close()

@app.post('/api/price-check')
def manual_price_check():
    return check_price_alerts()

@app.get('/api/products/{product_id}/accessories')
def accessories(product_id:str):
    catalog={'lenovo-loq':['Laptop cooling pad','USB-C hub','Wireless gaming mouse','Laptop sleeve'],'asus-vivobook':['USB-C hub','Wireless mouse','Laptop sleeve','External SSD'],'hp-victus':['Cooling pad','Gaming mouse','Laptop stand','External SSD']}
    return {'product_id':product_id,'accessories':catalog.get(product_id,['USB-C hub','Wireless mouse','Laptop sleeve','External SSD'])}
