from fastmcp import FastMCP

mcp = FastMCP("Toto Integration Example")

@mcp.tool() 
def greet(name: str, __context__=None) -> str:
    """Greet a person by name."""
    if __context__ is not None:
        auth_header = __context__.headers.get("authorization")
        
        print(f"Authorization header: {auth_header}")

    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")