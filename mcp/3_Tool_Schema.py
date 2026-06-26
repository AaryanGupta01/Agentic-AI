# =============================================================
# HANDS-ON 3 — Design a Tool Schema
# =============================================================
 
 
import json
 
print("\n=== HANDS-ON 3: DESIGNING AN MCP TOOL SCHEMA ===\n")
 
 
# -------------------------------------------------------------
# STEP 1: Why Schemas Matter
# -------------------------------------------------------------
print("=" * 60)
print("WHY DOES A TOOL NEED A SCHEMA?")
print("=" * 60)
print("""
An AI model cannot read your Python source code to know:
  - What does this tool do?
  - What parameters does it need?
  - What TYPE should each parameter be?
 
The schema is a structured description the AI reads BEFORE
calling the tool. It's like a function's "API documentation"
but in a format machines can parse and reason over.
""")
 
 
# -------------------------------------------------------------
# STEP 2: Build a Tool Schema — claim_status
# -------------------------------------------------------------
 
claim_status_tool = {
    "name": "claim_status",
    "description": "Get insurance claim status",
    "parameters": {
        "claim_id": {
            "type": "string",
            "description": "Claim Identifier"
        }
    }
}
 
print("=" * 60)
print("SCHEMA: claim_status_tool")
print("=" * 60)
print(json.dumps(claim_status_tool, indent=2))
 
 
# -------------------------------------------------------------
# STEP 3: Build 2 More Schemas — Practice
# -------------------------------------------------------------
 
policy_lookup_tool = {
    "name": "get_policy",
    "description": "Retrieve policy details by policy ID",
    "parameters": {
        "policy_id": {
            "type": "string",
            "description": "Unique policy identifier, e.g. P1001"
        }
    }
}
 
premium_calculator_tool = {
    "name": "calculate_premium",
    "description": "Calculate insurance premium based on customer age and policy type",
    "parameters": {
        "age": {
            "type": "integer",
            "description": "Customer age in years"
        },
        "policy_type": {
            "type": "string",
            "description": "Type of policy: Health, Car, or Life"
        }
    }
}
 
print("\n" + "=" * 60)
print("SCHEMA: get_policy")
print("=" * 60)
print(json.dumps(policy_lookup_tool, indent=2))
 
print("\n" + "=" * 60)
print("SCHEMA: calculate_premium (multiple parameters)")
print("=" * 60)
print(json.dumps(premium_calculator_tool, indent=2))
 
 
# -------------------------------------------------------------
# STEP 4: Validate a Schema (basic structure check)
# -------------------------------------------------------------
 
 
def validate_tool_schema(schema: dict) -> bool:
    """Check that a tool schema has the minimum required structure."""
    required_top_level = ["name", "description", "parameters"]
 
    for field in required_top_level:
        if field not in schema:
            print(f"  INVALID: missing top-level field '{field}'")
            return False
 
    for param_name, param_def in schema["parameters"].items():
        if "type" not in param_def:
            print(f"  INVALID: parameter '{param_name}' missing 'type'")
            return False
 
    print(f"  VALID: '{schema['name']}' schema is well-formed")
    return True
 
 
print("\n" + "=" * 60)
print("VALIDATING ALL 3 SCHEMAS")
print("=" * 60)
validate_tool_schema(claim_status_tool)
validate_tool_schema(policy_lookup_tool)
validate_tool_schema(premium_calculator_tool)
 
# Test an invalid schema
broken_schema = {"name": "broken_tool", "parameters": {}}
print("\nTesting an intentionally broken schema (missing 'description'):")
validate_tool_schema(broken_schema)
 
 