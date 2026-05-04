from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    ticker: str
    messages: Annotated[List[str], operator.add]
    analysis: dict
    consensus: float

# Define the 7 agents as simple functions
def technical_agent(state: AgentState): return {"analysis": {"technical": "bullish"}}
def fundamental_agent(state: AgentState): return {"analysis": {"fundamental": "neutral"}}
def sentiment_agent(state: AgentState): return {"analysis": {"sentiment": "positive"}}
def news_agent(state: AgentState): return {"analysis": {"news": "macro-stable"}}
def bull_agent(state: AgentState): return {"messages": ["Bull case: strong momentum"]}
def bear_agent(state: AgentState): return {"messages": ["Bear case: overbought levels"]}
def portfolio_manager(state: AgentState): return {"consensus": 0.9}

# Orchestrator setup
workflow = StateGraph(AgentState)
workflow.add_node("technical", technical_agent)
workflow.add_node("fundamental", fundamental_agent)
workflow.add_node("sentiment", sentiment_agent)
workflow.add_node("news", news_agent)
workflow.add_node("bull", bull_agent)
workflow.add_node("bear", bear_agent)
workflow.add_node("pm", portfolio_manager)

workflow.set_entry_point("technical")
workflow.add_edge("technical", "fundamental")
workflow.add_edge("fundamental", "sentiment")
workflow.add_edge("sentiment", "news")
workflow.add_edge("news", "bull")
workflow.add_edge("news", "bear")
workflow.add_edge("bull", "pm")
workflow.add_edge("bear", "pm")
workflow.add_edge("pm", END)

app = workflow.compile()
