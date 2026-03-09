from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """
    summary
    add two numbers"""
    return a+b

@mcp.tool()
def multiple(a:int,b:int)->int:
    """
    summary
    multiply two numbers"""
    return a*b

#The transoprt ="stdio" argument tell the server to:
#use standerd input/output(stdin or stdout) to recive and responce the tool function call
#client run and directly get output in command prompt by stdout
##check locally so used the stdio 
if __name__=="__main__":
    mcp.run(transport="stdio") #it uses for the command prompt