from dataclasses import dataclass
from fastmcp import FastMCP, Context
import httpx

mcp = FastMCP("Toto Integration Example")

@dataclass
class Topic: 
    name: str
    id: str
    
    def __init__(self, data: dict):
        self.name = data.get('name', '')
        self.id = data.get('id', '')
    
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

# @mcp.tool() 
# async def greet(name: str, context: Context) -> str:
#     """Greet a person by name."""
#     token = get_bearer_token(context)
    
#     return f"Hello, {name}!"

# @mcp.tool()
# async def get_tome_topics(context: Context) -> list[Topic]:
#     """Get a list of topics from Tome API."""
#     token = get_bearer_token(context)
    
#     # Call the Tome API to get topics
#     headers = {
#         "Authorization": f"Bearer {token}", 
#         "Content-Type": "application/json", 
#         "Accept": "application/json",
#     }
    
#     await context.info("Fetching topics from Tome API...")
    
#     async with httpx.AsyncClient(verify=False) as client:
#         response = await client.get("https://api.dev.toto.nimoto.eu/tometopics/topics", headers=headers)
#         response.raise_for_status()
#         topics_data = response.json()
        
#         await context.info(topics_data)
        
#         return [Topic(topic) for topic in topics_data.get('topics', [])]


# client = httpx.AsyncClient(base_url="https://api.dev.toto.nimoto.eu/tometopics", verify=False)
# openapi_spec = httpx.get("https://api.dev.toto.nimoto.eu/tometopics/jsondocs", verify=False).json() 
client = httpx.AsyncClient(base_url="https://dnd-services-test.de-prod.dk/orstedlabs/event/v1/data/api/prod", verify=False)
openapi_spec = httpx.get("https://dnd-services-test.de-prod.dk/orstedlabs/event/v1/data/api/prod/static/swagger/openapi.json", verify=False).json() 

mcp = FastMCP.from_openapi(
    name="Integration Example",
    openapi_spec=openapi_spec,
    client=client,
    #auth_header_getter=get_bearer_token,
)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")