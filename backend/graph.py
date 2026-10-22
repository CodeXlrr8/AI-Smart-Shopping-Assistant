from langgraph.graph import StateGraph, START, END
from state import ShoppingState
from agents import (
    requirement_agent, product_research_agent, specification_agent,
    review_agent, price_agent, ranking_agent, recommendation_agent
)

def build_graph():
    g = StateGraph(ShoppingState)

    g.add_node("requirements", requirement_agent)
    g.add_node("research", product_research_agent)
    g.add_node("specifications", specification_agent)
    g.add_node("reviews", review_agent)
    g.add_node("prices", price_agent)
    g.add_node("ranking", ranking_agent)
    g.add_node("recommendation", recommendation_agent)

    g.add_edge(START, "requirements")
    g.add_edge("requirements", "research")
    g.add_edge("research", "specifications")
    g.add_edge("specifications", "reviews")
    g.add_edge("reviews", "prices")
    g.add_edge("prices", "ranking")
    g.add_edge("ranking", "recommendation")
    g.add_edge("recommendation", END)

    return g.compile()

shopping_graph = build_graph()
