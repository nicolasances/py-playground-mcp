# Python Playground - MCP Server

`This repo contains a simple implementation of MCP Server to demostrate possible integration with different ecosystems.` <br>
Mainly focuses on the following integrations: 
* [Toto Ecosystem](https://github.com/nicolasances/toto)

## Testing
To test the MCP Server, you can use [`mcp-inspector`](https://github.com/modelcontextprotocol/inspector). Run the following: 
```
npx @modelcontextprotocol/inspector
``` 

No need to install anything, it will start a local instance of the inspector that you can use to test the MCP Server. <br>
The server will start up and the UI will be accessible at `http://localhost:6274`.

## Authentication 
MCP Server support Bearer Token authentication. <br>
You can set the token in the UI in the Authentication left panel. <br>

## Different ways to run MCP Servers
### 1. Easiest Way: Generate it from OpenAPI Specifications

```python
client = httpx.AsyncClient(base_url="https://<endpoint>", verify=False)
openapi_spec = httpx.get("https://<endpoint>/jsondocs", verify=False).json() 

mcp = FastMCP.from_openapi(
    name="Integration Example",
    openapi_spec=openapi_spec,
    client=client,
)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")
```

### 2. More control: Use Tools
You can also define one tool for every endpoint you want to expose. <br>
That gives you more control, but requires more code. <br>
For example, to get a list of topics from Tome API:

```python

@mcp.tool()
async def get_tome_topics(context: Context) -> list[Topic]:
    """Get a list of topics from Tome API."""
    token = get_bearer_token(context)
    
    # Call the Tome API to get topics
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json", 
        "Accept": "application/json",
    }
    
    await context.info("Fetching topics from Tome API...")
    
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get("https://<your-endpoint>/topics", headers=headers)
        response.raise_for_status()
        topics_data = response.json()
        
        await context.info(topics_data)
        
        return [Topic(topic) for topic in topics_data.get('topics', [])]

```