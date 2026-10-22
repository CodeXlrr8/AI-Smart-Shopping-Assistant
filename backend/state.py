from typing import TypedDict, List, Dict, Any

class ShoppingState(TypedDict, total=False):
    query: str
    user_profile: Dict[str, Any]
    products: List[Dict[str, Any]]
    normalized_products: List[Dict[str, Any]]
    review_results: Dict[str, Any]
    price_results: Dict[str, Any]
    ranked_products: List[Dict[str, Any]]
    recommendation: Dict[str, Any]
    agent_steps: List[str]
    research_metadata: Dict[str, Any]
