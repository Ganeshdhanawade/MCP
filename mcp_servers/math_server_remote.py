import random
from fastmcp import FastMCP

##crate the mcp server instant
mcp = FastMCP(name='arith')

def _as_number(x):
    if isinstance(x,(int,float)):
        return float(x)
    if isinstance(x,str):
        return float(x.strip())
    raise TypeError("Expected a number (int/float or numeric string)")

@mcp.tool()
async def roll_dice(n_dice: int=1) -> list[int]:
    """ Roll n_dice 6-sided dice and return the result"""
    return [random.randint(1,6) for _ in range(n_dice)]

@mcp.tool()
async def add_number(a:float, b:float) ->float:
    """ add the two numbers"""
    return _as_number(a) + _as_number(b)

@mcp.tool
async def subtract_number(a:float, b:float) ->float:
    """ subtract the two numbers"""
    return _as_number(a) - _as_number(b)

@mcp.tool
async def multiply_number(a:float, b:float) ->float:
    """ multiply the two numbers"""
    return _as_number(a) * _as_number(b)

@mcp.tool
async def devide_number(a:float, b:float) ->float:
    """devide the two numbers"""
    return _as_number(a) / _as_number(b)


if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)