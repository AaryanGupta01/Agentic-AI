from autogen import ConversableAgent
 
# =============================================================
# LLM CONFIG
# =============================================================
 
config_list = [
    {
        "model": "qwen2.5:3b",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "price": [0, 0]
    }
]
 
llm_config = {
    "config_list": config_list,
    "temperature": 0.2,
    "cache_seed": None, # Disable disk cache to avoid sqlite3 I/O errors
}
 
# =============================================================
# RISK AGENT
# =============================================================
 
risk_agent = ConversableAgent(
    name="RiskAgent",
    system_message="""
    You are a banking risk analyst.
 
    Return:
    Risk Level: Low / Medium / High
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)
 
# =============================================================
# CREDIT AGENT
# =============================================================
 
credit_agent = ConversableAgent(
    name="CreditAgent",
    system_message="""
    Generate a credit score and recommendation.
 
    Format:
    Credit Score: <score>
 
    Recommendation:
    APPROVE / REVIEW / REJECT
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)
 
# =============================================================
# HUMAN BANK MANAGER
# =============================================================
 
bank_manager = ConversableAgent(
    name="BankManager",
    llm_config=False,
    human_input_mode="ALWAYS"
)
 
# =============================================================
# CUSTOMER DATA
# =============================================================
 
customer_name = "Ravi"
loan_amount = "500000"
monthly_income = "60000"
 
# =============================================================
# RISK ANALYSIS
# =============================================================
 
risk_result = risk_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content": f"""
            Customer: {customer_name}
            Loan Amount: {loan_amount}
            Monthly Income: {monthly_income}
            """
        }
    ]
)
 
print("\n=== Risk Analysis ===")
print(risk_result)
 
# =============================================================
# CREDIT ANALYSIS
# =============================================================
 
credit_result = credit_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content": f"""
            Customer: {customer_name}
 
            Loan Amount: {loan_amount}
 
            Monthly Income: {monthly_income}
 
            Risk Analysis:
            {risk_result}
            """
        }
    ]
)
 
print("\n=== Credit Analysis ===")
print(credit_result)
 
# =============================================================
# HUMAN-IN-THE-LOOP
# =============================================================
 
print("\n=== HUMAN APPROVAL REQUIRED ===\n")
 
credit_agent.initiate_chat(
    bank_manager,
    message=f"""
Loan Application Summary
 
Customer: {customer_name}
Loan Amount: Rs {loan_amount}
Monthly Income: Rs {monthly_income}
 
{risk_result}
 
{credit_result}
 
Should this loan be approved?
Type APPROVE or REJECT.
""",
    max_turns=1
)