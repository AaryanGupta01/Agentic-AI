# =============================================================
# MCP CAPSTONE — Part 1: Insurance MCP Server
# =============================================================
 
 
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("Insurance MCP Server")
 
 
# =============================================================
# DATA LAYER — the actual business data behind each tool
# =============================================================
 
CUSTOMER_DB = {
    "C001": {"name": "John",  "policy_id": "P1001", "since": "2021", "email": "john@example.com"},
    "C002": {"name": "Priya", "policy_id": "P1002", "since": "2023", "email": "priya@example.com"},
    "C003": {"name": "Ravi",  "policy_id": "P1003", "since": "2020", "email": "ravi@example.com"},
}
 
POLICY_DB = {
    "P1001": {"type": "Health Insurance", "premium": 5000,  "active": True,  "coverage": 200000},
    "P1002": {"type": "Car Insurance",    "premium": 3200,  "active": True,  "coverage": 100000},
    "P1003": {"type": "Life Insurance",   "premium": 7800,  "active": False, "coverage": 500000},
}
 
CLAIM_DB = {
    "CL001": {"customer_id": "C001", "policy_id": "P1001", "status": "Approved",     "amount": 25000},
    "CL002": {"customer_id": "C002", "policy_id": "P1002", "status": "Under Review", "amount": 80000},
    "CL003": {"customer_id": "C001", "policy_id": "P1001", "status": "Rejected",     "amount": 150000},
    "CL004": {"customer_id": "C003", "policy_id": "P1003", "status": "Submitted",    "amount": 35000},
}
 
 
# =============================================================
# THE 6 MCP TOOLS
# =============================================================
 
@mcp.tool()
def get_customer(customer_id: str) -> str:
    """
    Get full customer profile by customer ID.
 
    Args:
        customer_id: Customer identifier, e.g. C001, C002, C003
    """
    record = CUSTOMER_DB.get(customer_id)
    if not record:
        return f"ERROR: Customer {customer_id} not found."
    return (
        f"Customer {customer_id}: Name={record['name']}, "
        f"Policy={record['policy_id']}, "
        f"Member since {record['since']}, "
        f"Email={record['email']}"
    )
 
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """
    Get insurance policy details by policy ID.
 
    Args:
        policy_id: Policy identifier, e.g. P1001, P1002, P1003
    """
    record = POLICY_DB.get(policy_id)
    if not record:
        return f"ERROR: Policy {policy_id} not found."
    status = "Active" if record["active"] else "Inactive"
    return (
        f"Policy {policy_id}: Type={record['type']}, "
        f"Status={status}, "
        f"Annual Premium=Rs {record['premium']:,}, "
        f"Coverage=Rs {record['coverage']:,}"
    )
 
 
@mcp.tool()
def get_claim_status(claim_id: str) -> str:
    """
    Get the current status of an insurance claim.
 
    Args:
        claim_id: Claim identifier, e.g. CL001, CL002, CL003, CL004
    """
    record = CLAIM_DB.get(claim_id)
    if not record:
        return f"ERROR: Claim {claim_id} not found."
    return (
        f"Claim {claim_id}: Status={record['status']}, "
        f"Amount=Rs {record['amount']:,}, "
        f"Customer={record['customer_id']}, "
        f"Policy={record['policy_id']}"
    )
 
 
@mcp.tool()
def get_premium_due(customer_id: str) -> str:
    """
    Get the annual premium amount due for a customer.
 
    Args:
        customer_id: Customer identifier, e.g. C001, C002, C003
    """
    customer = CUSTOMER_DB.get(customer_id)
    if not customer:
        return f"ERROR: Customer {customer_id} not found."
    policy = POLICY_DB.get(customer["policy_id"])
    if not policy:
        return f"ERROR: No policy found for {customer_id}."
    return (
        f"Premium due for {customer_id} ({customer['name']}): "
        f"Rs {policy['premium']:,} per year "
        f"for {policy['type']}"
    )
 
 
@mcp.tool()
def run_fraud_check(claim_id: str) -> str:
    """
    Run a fraud risk assessment on an insurance claim.
 
    Args:
        claim_id: Claim identifier, e.g. CL001, CL002, CL003, CL004
    """
    claim = CLAIM_DB.get(claim_id)
    if not claim:
        return f"ERROR: Claim {claim_id} not found."
 
    amount = claim["amount"]
 
    if amount > 100000:
        risk      = "HIGH RISK"
        action    = "Manual review required before processing"
        score     = 85
    elif amount > 50000:
        risk      = "MEDIUM RISK"
        action    = "Standard verification recommended"
        score     = 55
    else:
        risk      = "LOW RISK"
        action    = "Proceed with normal processing"
        score     = 15
 
    return (
        f"Fraud check for {claim_id}: "
        f"Risk={risk}, Score={score}/100, "
        f"Amount=Rs {amount:,}, "
        f"Action={action}"
    )
 
 
@mcp.tool()
def renew_policy(policy_id: str) -> str:
    """
    Renew an inactive insurance policy.
 
    Args:
        policy_id: Policy identifier to renew, e.g. P1001, P1002, P1003
    """
    policy = POLICY_DB.get(policy_id)
    if not policy:
        return f"ERROR: Policy {policy_id} not found."
    if policy["active"]:
        return f"Policy {policy_id} is already active — no renewal needed."
 
    policy["active"] = True
    return (
        f"Policy {policy_id} renewed successfully. "
        f"Type={policy['type']}, "
        f"Premium=Rs {policy['premium']:,}, "
        f"Coverage=Rs {policy['coverage']:,}"
    )
 
 
# =============================================================
# RUN THE SERVER
# =============================================================
 
if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("6 tools available:")
    print("  1. get_customer(customer_id)")
    print("  2. get_policy(policy_id)")
    print("  3. get_claim_status(claim_id)")
    print("  4. get_premium_due(customer_id)")
    print("  5. run_fraud_check(claim_id)")
    print("  6. renew_policy(policy_id)")
    print("\nWaiting for MCP client connections (Ctrl+C to stop)...\n")
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
 