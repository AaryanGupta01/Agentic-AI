# # =============================================================
# HANDS-ON 2 — MCP TOOL REGISTRY & DISCOVERY
# =============================================================
 
# This hands-on exercise demonstrates how an MCP client can discover and 
# interact with tools registered on an MCP server.

# FOR RUNNING npx @modelcontextprotocol/inspector python .py

print("\n=== MCP TOOL DISCOVERY ===\n")
 
# -------------------------------------------------------------
# STEP 1: Define MCP Tools
# -------------------------------------------------------------
 
def get_policy(policy_id):
    return f"Policy Details for {policy_id}"
 
def claim_status(claim_id):
    return f"Claim Status for {claim_id}"
 
def calculate_premium(age):
    if age < 30:
        return 5000
    elif age < 50:
        return 8000
    else:
        return 12000
 
 
# -------------------------------------------------------------
# STEP 2: Simulate MCP Server Tool Registry
# -------------------------------------------------------------
 
tool_registry = {
    "get_policy": get_policy,
    "claim_status": claim_status,
    "calculate_premium": calculate_premium
}
 
# -------------------------------------------------------------
# STEP 3: MCP Client Discovers Available Tools
# -------------------------------------------------------------
 
print("Tools discovered from MCP Server:\n")
 
for tool_name in tool_registry:
    print("•", tool_name)
 
# -------------------------------------------------------------
# STEP 4: MCP Client Calls a Tool
# -------------------------------------------------------------
 
selected_tool = "claim_status"
 
print("\nClient selected tool:", selected_tool)
 
result = tool_registry[selected_tool]("C1001")
#here, we call the selected tool with a sample claim ID "C1001" and print the result.
#if we don't use sample input, the tool will not have any data to process and will return a generic message.
 
print("Tool Result:", result)
 
# -------------------------------------------------------------
# STEP 5: Call Another Tool
# -------------------------------------------------------------
 
selected_tool = "calculate_premium"
 
print("\nClient selected tool:", selected_tool)
 
result = tool_registry[selected_tool](35)
 
print("Tool Result:", result)
 