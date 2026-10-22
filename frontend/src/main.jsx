import React,{useState} from 'react';
import {createRoot} from 'react-dom/client';
import './style.css';

const API=(import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
function App(){
 const [query,setQuery]=useState('Laptop for AI/ML and coding under ₹70000 with 16GB RAM');
 const [data,setData]=useState(null); const [loading,setLoading]=useState(false); const [error,setError]=useState('');
 async function search(){setLoading(true);setError('');try{const r=await fetch(API+'/api/shop',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query})});if(!r.ok)throw new Error(await r.text());setData(await r.json())}catch(e){setError('Backend not reachable. Start FastAPI on port 8000.')}finally{setLoading(false)}}
 async function alertFor(p){const target=prompt(`Target price for ${p.name}:`,String(Math.round(p.best_price*0.9)));if(!target)return;await fetch(API+'/api/alerts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({product_id:p.id,target_price:Number(target)})});alert('Price alert created.');}
 return <div className="app"><header><div><div className="eyebrow">GENERATIVE AI • AGENTIC AI</div><h1>Smart Shopping Assistant</h1><p>Research, compare, analyze reviews and explain the value of products.</p></div><span className="badge">V7</span></header>
 <section className="search"><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()}/><button onClick={search} disabled={loading}>{loading?'Researching…':'Find products'}</button></section>
 {error&&<div className="error">{error}</div>}
 {data&&<>
  <section className="profile"><h2>Requirement Analysis</h2><div className="chips"><span>Budget: ₹{data.user_profile.budget.toLocaleString('en-IN')}</span>{data.user_profile.use_cases.map(x=><span key={x}>{x}</span>)}{data.user_profile.mandatory_features.ram_gb&&<span>{data.user_profile.mandatory_features.ram_gb}GB RAM</span>}</div><small>Research mode: {data.research_metadata.mode}</small></section>
  <section><h2>Recommendations</h2><div className="grid">{data.products.map((p,i)=><article className={i===0?'card featured':'card'} key={p.id}><div className="rank">#{i+1}</div><h3>{p.name}</h3><div className="score">{p.agent_score}/100 match</div><p className="price">₹{Number(p.best_price).toLocaleString('en-IN')} <small>at {p.best_store}</small></p><dl><dt>CPU</dt><dd>{p.cpu}</dd><dt>RAM</dt><dd>{p.ram_gb}GB</dd><dt>Storage</dt><dd>{p.storage_gb}GB</dd><dt>GPU</dt><dd>{p.gpu}</dd><dt>Battery</dt><dd>{p.battery_wh}Wh</dd></dl><div className="review"><b>Reviews:</b> {p.rating}/5 • {p.review_count} reviews<br/>{p.review_analysis.pros.join(' • ')}</div><button className="secondary" onClick={()=>alertFor(p)}>Set price alert</button></article>)}</div></section>
  <section className="recommend"><h2>AI Recommendation</h2><h3>{data.recommendation.product_name}</h3><p>{data.recommendation.explanation}</p><small>LLM enhanced: {data.recommendation.llm_enhanced?'Yes':'No — rule-based fallback'}</small></section>
  <section className="pipeline"><h2>Agent Execution</h2>{data.agent_steps.map((s,i)=><div key={i}><b>{i+1}</b>{s}</div>)}</section>
 </>}
 </div>
}
createRoot(document.getElementById('root')).render(<App/>);
