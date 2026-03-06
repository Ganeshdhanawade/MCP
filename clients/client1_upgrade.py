#functionality for the multiple tool calling
import asyncio
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage,HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

#load the key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
fastmcp_key = os.getenv("FASTMCP_API_KEY")

SERVERS = {
    "maths": {
      "transport": "streamable_http",
      "url": "https://middle-orange-quail.fastmcp.app/mcp",
      "headers": {
                "Authorization": f"Bearer {fastmcp_key}"
            }
    },
    "ExpenseTracker": {
      "transport": "stdio",
      "command": "C:\\Users\\12353\\.conda\\envs\\manim\\Scripts\\uv.exe",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "C:\\Users\\12353\\Ganesh\\mcp\\expenses_server_remote\\main.py"
      ]
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm = ChatGroq(model="llama-3.3-70b-versatile")
    llm_with_tools = llm.bind_tools(tools)

    prompt = "add expenses on march 4 2026 by lunch 40 rs"
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())

