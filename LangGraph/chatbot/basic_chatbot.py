from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


class BasicChatbotState(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: BasicChatbotState):
    return {"messages": [llm.invoke(state["messages"])]}

basic_chatbot_graph = StateGraph(BasicChatbotState)

basic_chatbot_graph.add_node("chatbot", chatbot)
basic_chatbot_graph.set_entry_point("chatbot")
basic_chatbot_graph.add_edge("chatbot", END)

app = basic_chatbot_graph.compile()

while True:
    user_input = input("User: ")
    if(user_input in ["quit", "exit", "bye", "goodbye"]):
        break
    else:
        result = app.invoke({"messages": [HumanMessage(content=user_input)]})
        print(result["messages"][-1].content)