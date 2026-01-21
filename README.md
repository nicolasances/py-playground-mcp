# Python Playground - MCP Server

This repo contains a simple implementation of MCP Server to demostrate possible integration with different ecosystems. <br>
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