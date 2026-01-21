from fastmcp import FastMCP, Context

mcp = FastMCP("Toto Integration Example")

def get_bearer_token(ctx: Context):
    request = ctx.request_context.request
    headers = request.headers
    # Check if 'Authorization' header is present
    authorization_header = headers.get('Authorization')
    
    if authorization_header:
        # Split the header into 'Bearer <token>'
        parts = authorization_header.split()
        
        if len(parts) == 2 and parts[0] == 'Bearer':
            return parts[1]
        else:
            raise ValueError("Invalid Authorization header format")
    else:
        raise ValueError("Authorization header missing")

@mcp.tool() 
async def greet(name: str, context: Context) -> str:
    """Greet a person by name."""
    token = get_bearer_token(context)
    
    await context.info(f"{token}")
    
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")