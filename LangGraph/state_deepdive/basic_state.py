"""
What is State in LangGraph?

State in LangGraph is a way to maintain and tarck information as an AI system processes data.

Think of it as the system's memory, allowing it to remember and update information as it moves through different stages of a workflow, or graph.

"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class SimpleState(TypedDict):
    count: int


def increment(state: SimpleState) -> SimpleState:
    return {"count": state["count"] + 1}

def should_continue(state: SimpleState):
    if state["count"] < 10:
        return "continue"
    
    else: 
        return "stop"
    
graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.set_entry_point("increment")

graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue": "increment",
        "stop": END
    }
)



app = graph.compile()

state = {
    "count": 0
}

result = app.invoke(state)
print(result)


