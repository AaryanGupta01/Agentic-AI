# =============================================================
# HANDS-ON 4 — Your First Real MCP Server
# =============================================================
 
# FOR RUNNING npx @modelcontextprotocol/inspector python .py
 
from mcp.server.fastmcp import FastMCP
 
 
# -------------------------------------------------------------
# STEP 1: Create the MCP Server
# -------------------------------------------------------------
 
 
mcp = FastMCP("Insurance Server")
 
 
# -------------------------------------------------------------
# STEP 2: Define a Tool with @mcp.tool()
# -------------------------------------------------------------
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """Get insurance policy type by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return policies.get(policy_id, "Not Found")
 
 
# -------------------------------------------------------------
# STEP 3: Start the Server
# -------------------------------------------------------------
 
 
if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("Tool available: get_policy(policy_id)")
    print("Waiting for MCP client connections (Ctrl+C to stop)...\n")
    mcp.run()