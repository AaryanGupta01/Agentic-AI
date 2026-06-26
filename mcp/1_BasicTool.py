# Understanding MCP Basics

def get_policy_details(policy_id: str) -> str:
    """Look up policy type by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return policies.get(policy_id, "Policy Not Found")
 
 
print("Calling get_policy_details('P1002') directly:")
print(" ", get_policy_details("P1002"))
 
print("\nCalling get_policy_details('P9999') (unknown ID):")
print(" ", get_policy_details("P9999"))