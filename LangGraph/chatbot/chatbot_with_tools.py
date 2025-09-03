from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

load_dotenv()

class BasicChatbot(TypedDict):
    messages: Annotated[list, add_messages]

tool = TavilySearchResults(max_results = 2)
tools = [tool]

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

llm_with_tools = llm.bind_tools(tools=tools)


def chatbot(state: BasicChatbot):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def tools_router(state: BasicChatbot):
    last_message = state["messages"][-1]

    if (hasattr(last_message, "tool_calls")) and (len(last_message.tool_calls) > 0):
        return "tool_node"
    else:
        return END
    

tool_node = ToolNode(tools=tools)

"""
ToolNode 

A node that runs the tools called in the last AIMessage.

It can be used either in StateGraph with a "messages" state key (or a custom key passed via ToolNode's 'messages_key'). If multiple tool calls are requested, they will be run in parallel. The output will be a list of ToolMessages, one for each tool call.

Tool calls can also be passed directly as a list of ToolCall dicts.

"""

chatbot_graph = StateGraph(BasicChatbot)

chatbot_graph.add_node("chatbot", chatbot)
chatbot_graph.add_node("tool_node", tool_node)
chatbot_graph.set_entry_point("chatbot")

chatbot_graph.add_conditional_edges("chatbot", tools_router)
chatbot_graph.add_edge("tool_node", "chatbot")

app = chatbot_graph.compile()

while True:
    user_input = input("User: ")
    if(user_input in ["quit", "exit", "bye", "goodbye"]):
        break
    else:
        result = app.invoke({"messages": [HumanMessage(content=user_input)]})
        print(result)
        print(result["messages"][-1].tool_calls)
