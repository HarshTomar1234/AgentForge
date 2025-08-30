from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv
from langchain.agents import initialize_agent, tool
from langchain_community.tools import TavilySearchResults
import datetime


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in the specified format"""

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

tools = [search_tool, get_system_time]
    

agent = initialize_agent(
    llm=llm,
    agent="zero-shot-react-description",
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

#  agent.invoke("Tell me about LRM model which is basically in building process by Fractal Analytics company?")

agent.invoke("When was SpaceX's last launch and what was the name of the rocket also how many days ago was that from this instant?")
  