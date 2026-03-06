from fastmcp import FastMCP

mcp = FastMCP.as_proxy(
    "mcp clode url",
    name = "ganesh server proxy"
)

if __name__=="__main__":
    mcp.run()