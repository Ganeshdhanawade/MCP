from fastmcp import FastMCP
from main import app #application ofr the fastapi created

#convert fastapi to fastmcp server
mcp = FastMCP.from_fastapi(
    app=app,
    name="expense traker server",
)

if __name__=="__main__":
    mcp.run()