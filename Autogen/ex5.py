# =============================================================
# HUMAN-IN-THE-LOOP LOAN APPROVAL SYSTEM
# =============================================================
 
from autogen import ConversableAgent
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
 
console = Console()
 
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
# HEADER
# =============================================================
 
console.print(
    Panel.fit(
        "[bold cyan]🏦 AI LOAN APPROVAL SYSTEM[/bold cyan]",
        border_style="green"
    )
)
 
# =============================================================
# CUSTOMER APPLICATION
# =============================================================
 
customer_name = input("Customer Name      : ")
loan_amount = input("Loan Amount (Rs)   : ")
monthly_income = input("Monthly Income (Rs): ")
 
console.print()
 
table = Table(title="Loan Application")
 
table.add_column("Field", style="cyan")
table.add_column("Value", style="green")
 
table.add_row("Customer", customer_name)
table.add_row("Loan Amount", f"Rs {loan_amount}")
table.add_row("Monthly Income", f"Rs {monthly_income}")
 
console.print(table)
 
# =============================================================
# RISK AGENT
# =============================================================
 
risk_agent = ConversableAgent(
    name="RiskAgent",
    system_message="""
    You are a banking risk analyst.
 
    Analyze the loan request.
 
    Return:
    Risk Level: Low / Medium / High
 
    Keep answer short.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)
 
# =============================================================
# CREDIT SCORE AGENT
# =============================================================
 
credit_agent = ConversableAgent(
    name="CreditScoreAgent",
    system_message="""
    You are a credit score specialist.
 
    Generate a realistic credit score between 650 and 850.
 
    Format:
 
    Credit Score: <score>
 
    Recommendation:
    APPROVE
    REVIEW
    REJECT
 
    Keep answer short.
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
# RISK ASSESSMENT
# =============================================================
 
console.print(
    Panel.fit(
        "[bold yellow]Running Risk Assessment...[/bold yellow]",
        border_style="yellow"
    )
)
 
risk_result = risk_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content":
            f"""
            Customer: {customer_name}
 
            Loan Amount: Rs {loan_amount}
 
            Monthly Income: Rs {monthly_income}
            """
        }
    ]
)
 
console.print(
    Panel(
        risk_result,
        title="Risk Agent",
        border_style="red"
    )
)
 
# =============================================================
# CREDIT SCORE
# =============================================================
 
credit_result = credit_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content":
            f"""
            Customer: {customer_name}
 
            Loan Amount: Rs {loan_amount}
 
            Monthly Income: Rs {monthly_income}
 
            Risk Analysis:
 
            {risk_result}
            """
        }
    ]
)
 
console.print(
    Panel(
        credit_result,
        title="Credit Score Agent",
        border_style="blue"
    )
)
 
# =============================================================
# HUMAN-IN-THE-LOOP
# =============================================================
 
console.print()
 
console.print(
    Panel.fit(
        "[bold magenta]HUMAN APPROVAL REQUIRED[/bold magenta]",
        border_style="magenta"
    )
)
 
console.print(
    f"""
[bold]Risk Agent:[/bold]
{risk_result}
 
[bold]Credit Agent:[/bold]
{credit_result}
"""
)
 
decision = input(
    "\nApprove loan of Rs "
    + loan_amount +
    "? (yes/no): "
).strip().lower()
 
# =============================================================
# FINAL DECISION
# =============================================================
 
if decision == "yes":
 
    console.print(
        Panel.fit(
            "[bold green]✅ LOAN APPROVED[/bold green]",
            border_style="green"
        )
    )
 
else:
 
    console.print(
        Panel.fit(
            "[bold red]❌ LOAN REJECTED[/bold red]",
            border_style="red"
        )
    )
 
console.print(
    Panel.fit(
        "[bold cyan]Workflow Completed[/bold cyan]",
        border_style="cyan"
    )
)