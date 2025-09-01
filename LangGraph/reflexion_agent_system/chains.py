"""

Reflection Agent System consists of a generator and a reflector component

Although, iteratively making a post better is significantly better than just prompting ChatGPT, the content generated is still not grounded in live data and may even become increasingly off-topic.

It could be hallucination or outdated content and we have no way of knowing unless we actually check the content against the live data.

"""

"""
What is Reflexion Agent System?

The reflexion agent, similaar to reflection agent, not only critiques it's own responses but also facct checks it with external data by making API calls (Internet Search)

In the Reflection agent pattern, we had to rely on the training data of LLMs but in this case, we're not limited to that.

The main component of Reflexion Agent System is the "actor" 

The "actor" is the main agent that drives everything-it reflects on it's responses and re-executes.

It can do this with or without tools to improve based on the self critiques that is grounded in external data.

It's main sub-components include:
1. Tools/tool execution
2. Initial responder: generate an initial response & self-reflection
3. Revisor: re-respond & reflect based on previous reflections


Episodic Memory:

In the context of Reflexion agents, episodic memory refers to an agent's ability to recall specific past interactions, events, or experiences, rather than just generalized knowledge.

This is crucial for making agents feel more context-aware , personalized, and human-like over time.


"""
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion, ReviseAnswer
from langchain_core.output_parsers.openai_tools import PydanticToolsParser, JsonOutputToolsParser
from langchain_core.messages import HumanMessage

load_dotenv()

pydantic_parser = PydanticToolsParser(tools=[AnswerQuestion])

# parser = JsonOutputToolsParser(return_id=True)

# Actor Agent Prompt 
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') 

validator = PydanticToolsParser(tools=[AnswerQuestion])

# Revisor section

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

revisor_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")

# response = first_responder_chain.invoke({
#     "messages": [HumanMessage("Write me a blog post on how small business can leverage AI to improve their operations and grow their business")]
# })

# print(response)


"""
LLM Response Parser System

The system converts unstructured LLM outputs into well-defined Python objects through a series of structured parsing steps, ensuring data validation and consistent formatting.

What are the key components of LLM Response Parser System?

1. ChatPromptTemplate: Defines the prompt for the LLM

2. Function Calling with Pydantic Schema : Similar to how we make tools available to the LLM,
we can also send a schema to the LLM and force it to structure it's JSON output according to the schema.
Pydantic: A python library that defines data structures using classes
It provides automatic data validation and documentation.

3. Pydantic Parser: Takes the JSON output from the LLM's function call abd validates it against the defined Pydantic schema(class definition).
It creates instances of Pydantic classes with the validated data.
If the LLMs output does not match with the defined schema, it will throw an error.


"""