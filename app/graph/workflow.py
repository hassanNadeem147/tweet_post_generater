from langgraph.graph import StateGraph, START, END
from app.graph.state import TweetState
from app.graph.nodes import (
    improve_text,
    generate_text,
    review_text,
    reviewer_router
)
workflow = StateGraph(TweetState)
workflow.add_node("generate_tweet", generate_text)
workflow.add_node("review_tweet", review_text)
workflow.add_node("improve_tweet", improve_text)
workflow.add_edge(START, "generate_tweet")
workflow.add_edge("generate_tweet", "review_tweet")
workflow.add_conditional_edges(
    "review_tweet",
    reviewer_router,
    {
        "improve": "improve_tweet",
        "end": END
    }
)
workflow.add_edge("improve_tweet", "review_tweet")
app = workflow.compile()