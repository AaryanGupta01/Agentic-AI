# =============================================================
# HANDS-ON 5 — Multiple MCP Tools on One Server
# =============================================================
 
# FOR RUNNING npx @modelcontextprotocol/inspector python .py

#It is like a tool directory for agentic ai systems where each tool 
#is a function that can be called by the ai to perform specific actions,
 
# And resource will be like documentation for these tools which are for 
# reading for ai and not for performing any action.

#An analogy can be made with a library where each tool is a function and 
# resource is like the documentation for the library.
 
 
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("Insurance Server")
 
 
# -------------------------------------------------------------
# TOOL 1: Policy Lookup
# -------------------------------------------------------------
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """Get insurance policy details by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return f"Policy {policy_id}: {policies.get(policy_id, 'Not Found')}"
 
 
# -------------------------------------------------------------
# TOOL 2: Claim Status
# -------------------------------------------------------------
 
@mcp.tool()
def claim_status(claim_id: str) -> str:
    """Check the current status of an insurance claim."""
    claims = {
        "C1001": "Approved",
        "C1002": "Under Review",
        "C1003": "Rejected",
    }
    status = claims.get(claim_id, "Claim Not Found")
    return f"Claim {claim_id}: {status}"
 
 
# -------------------------------------------------------------
# TOOL 3: Premium Due
# -------------------------------------------------------------
 
@mcp.tool()
def premium_due(customer_id: str) -> str:
    """Get the premium amount due for a customer."""
    premiums = {
        "CUST001": 5000,
        "CUST002": 3200,
        "CUST003": 7800,
    }
    amount = premiums.get(customer_id)
    if amount is None:
        return f"No premium record found for {customer_id}"
    return f"Premium due for {customer_id}: Rs {amount:,}"
 
 
# -------------------------------------------------------------
# Start the Server
# -------------------------------------------------------------
 
if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("\n3 Tools available:")
    print("  1. get_policy(policy_id)")
    print("  2. claim_status(claim_id)")
    print("  3. premium_due(customer_id)")
    print("\nWaiting for MCP client connections (Ctrl+C to stop)...\n")
    mcp.run()