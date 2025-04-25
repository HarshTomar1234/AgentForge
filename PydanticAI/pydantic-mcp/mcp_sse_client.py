import os
import asyncio
import logfire
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

logfire.configure()
logfire.instrument_pydantic_ai()

os.environ["GROQ_API_KEY"] = "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"

server = MCPServerHTTP(url='http://localhost:3001/sse')  
agent = Agent('groq:llama-3.3-70b-versatile', mcp_servers=[server])  


async def main():
    async with agent.run_mcp_servers():  
        result = await agent.run('What are the top 10 popular places for destination wedding?')
    print(result.output)
    

asyncio.run(main())