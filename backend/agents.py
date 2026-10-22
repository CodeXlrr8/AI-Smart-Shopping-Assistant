import re
from copy import deepcopy
from data import DEMO_PRODUCTS
from adapters.product_api import search_products
from llm import generate_explanation
from fake_review_ml import predict_reviews


def steps(state, text):
    return state.get('agent_steps', []) + [text]


def requirement_agent(state):
    q = state['query'].lower()
    budget_match = re.search(r'(?:under|below|within|budget(?:\s+of)?|₹|rs\.?)[^0-9]{0,8}(\d[\d,]*)', q)
    budget = int(budget_match.group(1).replace(',', '')) if budget_match else 70000
    use_cases = []
    for key, label in [('coding','Coding'),('programming','Programming'),('ai/ml','AI/ML'),('machine learning','AI/ML'),('college','College'),('gaming','Gaming'),('editing','Content creation')]:
        if key in q and label not in use_cases:
            use_cases.append(label)
    ram = re.search(r'(\d+)\s*gb\s*ram', q)
    mandatory = {'ram_gb': int(ram.group(1))} if ram else {}
    if ('ai/ml' in q or 'machine learning' in q) and 'ram_gb' not in mandatory:
        mandatory['ram_gb'] = 16
    return {'user_profile': {'product_type':'Laptop','budget':budget,'use_cases':use_cases or ['General use'],'mandatory_features':mandatory}, 'agent_steps':steps(state,'Requirement Analysis Agent extracted budget, use cases and required specifications')}


def product_research_agent(state):
    products, metadata = search_products_sync(state['query'])
    if products is None:
        products = deepcopy(DEMO_PRODUCTS)
    return {'products':products,'research_metadata':metadata,'agent_steps':steps(state,f'Product Research Agent completed using {metadata["mode"]}')}


def search_products_sync(query):
    import os, httpx
    from dotenv import load_dotenv
    load_dotenv()
    url = os.getenv('PRODUCT_API_URL','').strip()
    key = os.getenv('PRODUCT_API_KEY','').strip()
    if not url:
        return None, {'mode':'demo fallback','reason':'PRODUCT_API_URL is not configured'}
    headers = {'Authorization':f'Bearer {key}'} if key else {}
    if key: headers['X-API-Key'] = key
    try:
        r = httpx.get(url, params={'q':query}, headers=headers, timeout=20)
        r.raise_for_status()
        payload = r.json()
        items = payload.get('products') or payload.get('items') or payload.get('results') or []
        if not items: return None, {'mode':'demo fallback','reason':'API returned no products'}
        normalized=[]
        for i,item in enumerate(items):
            normalized.append({
                'id':str(item.get('id') or item.get('sku') or f'api-{i}'), 'name':item.get('name') or item.get('title') or f'Product {i+1}',
                'brand':item.get('brand','Unknown'), 'cpu':item.get('cpu') or item.get('processor','Unknown'),
                'ram_gb':float(item.get('ram_gb') or item.get('ram') or 0), 'storage_gb':float(item.get('storage_gb') or item.get('storage') or 0),
                'gpu':item.get('gpu','Unknown'), 'battery_wh':float(item.get('battery_wh') or item.get('battery') or 0),
                'weight_kg':float(item.get('weight_kg') or item.get('weight') or 0), 'prices':item.get('prices') or ({item.get('store','API'):float(item.get('price',0))} if item.get('price') else {}),
                'rating':float(item.get('rating') or 0), 'review_count':int(item.get('review_count') or 0),
                'reviews':item.get('reviews') or [], 'source':item.get('source') or 'external-api'
            })
        return normalized, {'mode':'authorized external product API','count':len(normalized)}
    except Exception as exc:
        return None, {'mode':'demo fallback','reason':str(exc)[:160]}


def specification_agent(state):
    normalized=[]
    for p in state['products']:
        p=dict(p)
        p['normalized_specs']={'CPU':p.get('cpu') or 'Not available','RAM':f"{p.get('ram_gb',0):g}GB",'Storage':f"{p.get('storage_gb',0):g}GB",'GPU':p.get('gpu') or 'Not available','Battery':f"{p.get('battery_wh',0):g}Wh"}
        normalized.append(p)
    return {'normalized_products':normalized,'agent_steps':steps(state,'Specification Analysis Agent standardized product information')}


def review_agent(state):
    results={}
    for p in state['normalized_products']:
        reviews=p.get('reviews',[]) or []
        predictions=predict_reviews(reviews)
        suspicious=[x for x in predictions if x['suspicious']]
        clean=' '.join(x['text'] for x in predictions if not x['suspicious']).lower()
        pros=[]; cons=[]
        if any(x in clean for x in ['excellent','great','fast','powerful','solid']): pros.append('Positive user-reported performance')
        if 'battery' in clean and any(x in clean for x in ['good','excellent','lasts','stable']): pros.append('Positive battery feedback')
        if 'lightweight' in clean: pros.append('Positive portability feedback')
        if any(x in clean for x in ['average','could be better','bulky','heavy','loud']): cons.append('Some portability, battery or noise trade-offs')
        reliability=100 if not reviews else round((1-(len(suspicious)/len(reviews)))*100,1)
        results[p['id']]={'pros':pros or ['Insufficient review evidence'],'cons':cons or ['No major recurring issue identified'],'summary':'Review evidence analyzed using a TF-IDF + logistic-regression suspicious-review classifier.','reliability_score':reliability,'suspicious_reviews':len(suspicious),'review_count':len(reviews),'review_predictions':predictions}
    return {'review_results':results,'agent_steps':steps(state,'Review Analysis + ML Suspicious Review Detection Agents evaluated available review evidence')}

def price_agent(state):
    output={}
    for p in state['normalized_products']:
        valid={k:v for k,v in (p.get('prices') or {}).items() if isinstance(v,(int,float)) and v>0}
        store=min(valid,key=valid.get) if valid else 'Not available'
        output[p['id']]={'best_store':store,'best_price':valid.get(store,0),'price_count':len(valid)}
    return {'price_results':output,'agent_steps':steps(state,'Price Comparison Agent identified the lowest available price')}


def ranking_agent(state):
    profile=state['user_profile']; ranked=[]
    for p in state['normalized_products']:
        pd=state['price_results'][p['id']]; review=state['review_results'][p['id']]; price=pd['best_price']
        fit=100; required=profile['mandatory_features'].get('ram_gb',0)
        if required and p.get('ram_gb',0)<required: fit-=40
        if price and price>profile['budget']: fit-=min(30,((price-profile['budget'])/profile['budget'])*100)
        use=' '.join(profile['use_cases']).lower()
        if 'gaming' in use or 'ai/ml' in use:
            if 'RTX' in str(p.get('gpu','')): fit+=5
        if 'college' in use and p.get('weight_kg',0) and p['weight_kg']<=2.0: fit+=5
        fit=max(0,min(100,fit))
        spec=50 + (20 if p.get('ram_gb',0)>=16 else 0) + (20 if 'RTX' in str(p.get('gpu','')) else 0) + (10 if p.get('battery_wh',0)>=60 else 0)
        review_score=(p.get('rating',0)/5*100) if p.get('rating') else 50
        price_score=50 if not price else (100 if price<=profile['budget'] else max(20,100-(price-profile['budget'])/profile['budget']*100))
        score=fit*.30+spec*.25+review_score*.20+price_score*.15+review['reliability_score']*.10
        item=dict(p); item.update(pd); item['review_analysis']=review; item['agent_score']=round(score,1); ranked.append(item)
    ranked.sort(key=lambda x:x['agent_score'],reverse=True)
    return {'ranked_products':ranked,'agent_steps':steps(state,'Value-for-Money Agent ranked products using fit, specifications, reviews, reliability and price')}


def recommendation_agent(state):
    best=state['ranked_products'][0]
    evidence={'name':best['name'],'score':best['agent_score'],'price':best['best_price'],'store':best['best_store'],'rating':best.get('rating'),'use_cases':state['user_profile']['use_cases']}
    prompt=f"Explain in 3 concise sentences why this laptop matches the user's requirements. Evidence JSON: {evidence}. Do not invent specs or prices."
    llm_text=generate_explanation(prompt)
    explanation=llm_text or (f"{best['name']} achieved the highest match score based on your budget, required specifications, available price, review evidence and overall value.")
    return {'recommendation':{'product_id':best['id'],'product_name':best['name'],'score':best['agent_score'],'explanation':explanation,'llm_enhanced':bool(llm_text)},'agent_steps':steps(state,'Recommendation Agent produced the final explainable recommendation')}
