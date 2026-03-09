from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

async def main():
    client = MultiServerMCPClient({
        "math": {
           "command": "python3",
           "args": ["/home/ganesh/Analysis/mcp1/mathserver.py"],
           "transport": "stdio",
        },
        "weather": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        }
    })

    try:
        tools = await client.get_tools() ##get in in above tools connected
    except Exception as e:
        print(f"[ERROR] Failed to get tools: {e}")
        return

    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)

    # math_response = await agent.ainvoke({
    #     "messages": [{"role": "user", "content": "what's (3+5) x 12?"}]
    # })

    weather_response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "what is weather in california?"}]
    })

    print("Response:", weather_response["messages"][-1].content)

asyncio.run(main())