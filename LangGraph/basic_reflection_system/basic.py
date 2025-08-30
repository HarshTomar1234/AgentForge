import os
from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain


# What is MessageGraph?

"""
 MessageGraph is a class that LangcGraph provides that we can use to orchestrate the flow of messages between different nodes in the graph.

 Example usecases :
 Simple routing decisions, simple chatbot conversation flow, etc..

 If you just want to pass messages along between nodes, then go for MessageGraph.

 If the app requires complex state management, then go for StateGraph.

 To put it simply, MessageGraph maintains a list of messages and decides the flow of those messages between nodes.

 Every node in MessageGraph receives the full list of previous messages as input.

 Each node can append new messages to the list and return it.

 The updated message list is then passed to the next node in the graph.

"""

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()

def generate_node(state):
    return generation_chain.invoke({
        "messages": state
    })


def reflect_node(messages):
    response = reflection_chain.invoke({
        "messages": messages
    })
    return [HumanMessage(content=response.content)]


graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)


def should_continue(state):
    if (len(state) > 6):
        return END 
    return REFLECT


graph.add_conditional_edges(
    GENERATE, should_continue,
    path_map={
        REFLECT: REFLECT,
        END: END
    }
)

graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

response = app.invoke(HumanMessage(content="AI Agents taking over content creation"))

for message in response:
    print(message.content)