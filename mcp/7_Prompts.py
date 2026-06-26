# FOR RUNNING npx @modelcontextprotocol/inspector python .py

# =============================================================
# HANDS-ON 7 — MCP Prompts
# =============================================================
 
 
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("Insurance Server")
 
 
# -------------------------------------------------------------
# TOOLS (from previous hands-on labs)
# -------------------------------------------------------------
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """Get insurance policy details by policy ID."""
    policies = {"P1001": "Health Insurance", "P1002": "Car Insurance", "P1003": "Life Insurance"}
    return policies.get(policy_id, "Not Found")
 
 
@mcp.tool()
def claim_status(claim_id: str) -> str:
    """Check the current status of an insurance claim."""
    claims = {"C1001": "Approved", "C1002": "Under Review", "C1003": "Rejected"}
    return claims.get(claim_id, "Claim Not Found")
 
 
# -------------------------------------------------------------
# RESOURCE (from Hands-on 7)
# -------------------------------------------------------------
 
@mcp.resource("policy://all")
def get_all_policies() -> str:
    """Provide the full list of available insurance policies."""
    return "P1001 - Health Insurance\nP1002 - Car Insurance\nP1003 - Life Insurance"
 
 
# -------------------------------------------------------------
# PROMPT 1: Claim Review Workflow
# -------------------------------------------------------------
 
 
@mcp.prompt()
def claim_review_prompt() -> str:
    """A structured workflow for reviewing an insurance claim."""
    return """
    Review the claim details carefully and follow these steps:
 
    1. Verify the claim_id exists and pull its current status
    2. Check the policy is active and covers the claimed incident
    3. Identify any fraud indicators:
       - Unusually high claim amount vs policy history
       - Claim filed very soon after policy purchase
       - Multiple claims from the same customer in a short period
    4. Summarise your findings in plain language
    5. Recommend: Approve / Investigate Further / Reject
    """
 
 
# -------------------------------------------------------------
# PROMPT 2: Customer Communication Template
# -------------------------------------------------------------
 
@mcp.prompt()
def customer_response_prompt() -> str:
    """A tone and structure guide for responding to customer queries."""
    return """
    When responding to insurance customers:
 
    1. Acknowledge their question warmly and clearly
    2. Provide the specific answer using available tools/resources
       (do not guess — always look up real claim/policy data)
    3. Explain any next steps in plain, non-technical language
    4. Avoid insurance jargon unless the customer used it first
    5. End with an offer to help further if needed
    """
 
 
# -------------------------------------------------------------
# PROMPT 3: Policy Renewal Reminder
# -------------------------------------------------------------
 
@mcp.prompt()
def renewal_reminder_prompt() -> str:
    """A template for generating policy renewal reminders."""
    return """
    When generating a renewal reminder for a customer:
 
    1. State the policy type and policy ID clearly
    2. State the exact renewal/expiry date
    3. State the premium amount due
    4. Mention any late renewal penalties if applicable
    5. Provide a clear call to action (how to renew)
    Keep the tone friendly but create appropriate urgency if
    the renewal date is within 7 days.
    """
 
 
# -------------------------------------------------------------
# Start the Server
# -------------------------------------------------------------
 
if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("\n2 Tools:")
    print("  1. get_policy(policy_id)")
    print("  2. claim_status(claim_id)")
    print("\n1 Resource:")
    print("  1. policy://all")
    print("\n3 Prompts:")
    print("  1. claim_review_prompt")
    print("  2. customer_response_prompt")
    print("  3. renewal_reminder_prompt")
    print("\nWaiting for MCP client connections (Ctrl+C to stop)...\n")
    mcp.run()