import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '').strip()
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

def generate_explanation(prompt: str):
    if not OPENAI_API_KEY:
        return None
    try:
        r = httpx.post(
            f'{OPENAI_BASE_URL}/chat/completions',
            headers={'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'},
            json={'model': OPENAI_MODEL, 'messages': [
                {'role': 'system', 'content': 'You are a shopping assistant. Use only the supplied product evidence. Be concise and factual.'},
                {'role': 'user', 'content': prompt}
            ], 'temperature': 0.2},
            timeout=30
        )
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content'].strip()
    except Exception:
        return None
