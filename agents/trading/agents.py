from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator
from .openmythos_client import reason_deeply
from .technical import get_technical_signal
from .portfolio_manager import decide_trade

class AgentState(TypedDict):
    ticker: str
    messages: Annotated[List[str], operator.add]
    analysis: dict
    consensus: Annotated[float, operator.add]

def technical_agent(state: AgentState):
    signal = get_technical_signal(state['ticker'])
    return {"analysis": {"technical": signal}}

def fundamental_agent(state: AgentState): return {"analysis": {"fundamental": "neutral"}}
def sentiment_agent(state: AgentState): return {"analysis": {"sentiment": "positive"}}
def news_agent(state: AgentState): return {"analysis": {"news": "macro-stable"}}

def bull_agent(state: AgentState): 
    verdict = reason_deeply("Analyze bull case for " + state['ticker'])
    return {"messages": [verdict], "consensus": 0.5}

def bear_agent(state: AgentState): 
    verdict = reason_deeply("Analyze bear case for " + state['ticker'])
    return {"messages": [verdict], "consensus": 0.5}

def portfolio_manager(state: AgentState): 
    # Aggregate consensus
    final_consensus = state.get('consensus', 0.5) 
    decision = decide_trade(final_consensus, "NORMAL")
    return {"analysis": {"decision": decision}}

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
