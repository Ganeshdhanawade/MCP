import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
import os
from dotenv import load_dotenv

load_dotenv()

#load the key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

SERVERS = {
    "arith": {
      "command": "C:\\Users\\12353\\.conda\\envs\\manim\\python.exe",
      "args": [
        "C:\\Users\\12353\\Ganesh\\mcp\\mcp_servers\\math_server.py"
      ],
      "transport": "stdio",
    }
}
async def main():
    
    claint = MultiServerMCPClient(SERVERS)
    tools = await claint.get_tools()

    name_tools = {}
    for tool in tools:
        name_tools[tool.name] = tool

    print(name_tools)

    llm = ChatGroq(model="llama-3.3-70b-versatile")
    llm_with_tools = llm.bind_tools(tools)

    prompt = "what is india birth rate if nessesary that time only use tool otherwise not call"
    response =  await llm_with_tools.ainvoke(prompt)

    if not getattr(response,"tool_calls",None):
        print("\nLLM Reply:",response.content)
        return

    selected_tool = response.tool_calls[0]["name"]
    selected_tool_args = response.tool_calls[0]["args"]
    selected_tool_id = response.tool_calls[0]["id"]
    
    print(f"selectd tool: {selected_tool}")
    print(f"selected_tool_args: {selected_tool_args}")

    tool_result = await name_tools[selected_tool].ainvoke(selected_tool_args)
    print(f"tool_result: {tool_result}")

    tool_message = ToolMessage(content=tool_result,tool_call_id = selected_tool_id)

    final_result = await llm_with_tools.ainvoke([prompt,response,tool_message])
    print(f"final_response: {final_result.content}")


if __name__=='__main__':
    asyncio.run(main())