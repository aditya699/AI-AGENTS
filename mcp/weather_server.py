from mcp.server.fastmcp import FastMCP

# Initialize MCP server with an ID
mcp = FastMCP("simple-mcp")

# Register a basic greeting tool
@mcp.tool()
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny."

# Run the server using stdio (works with Claude Desktop or any MCP host)
if __name__ == "__main__":
    mcp.run(transport="stdio")
