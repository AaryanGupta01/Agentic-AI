# =============================================================
# HANDS-ON 4 — Smart E-Commerce Capstone (Qwen 2.5 via Ollama)
# =============================================================
 
import sqlite3
import random
import datetime
import os
from autogen import ConversableAgent, GroupChat, GroupChatManager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
 
console = Console()
 
DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")
 
 
# =============================================================
# SECTION 1: DATABASE SETUP
# =============================================================
 
def setup_database():
    """Create the orders table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id       TEXT NOT NULL,
            customer_name  TEXT NOT NULL,
            product        TEXT NOT NULL,
            original_price INTEGER,
            discount_pct   INTEGER,
            final_price    INTEGER,
            decision       TEXT,
            timestamp      TEXT
        )
    """)
    conn.commit()
    conn.close()
 
 
# =============================================================
# SECTION 2: PRODUCT CATALOG
# =============================================================
 
PRODUCT_CATALOG = {
    "Lenovo LOQ":     {"price": 68000, "stock": 5,  "rating": 4.6, "gpu": "RTX 4050", "ram": "16GB"},
    "ASUS TUF A15":   {"price": 72000, "stock": 3,  "rating": 4.5, "gpu": "RTX 4060", "ram": "16GB"},
    "HP Victus 15":   {"price": 58000, "stock": 8,  "rating": 4.3, "gpu": "GTX 1650", "ram": "8GB"},
    "Acer Nitro V":   {"price": 65000, "stock": 0,  "rating": 4.4, "gpu": "RTX 4050", "ram": "16GB"},
    "Dell G15":       {"price": 79000, "stock": 2,  "rating": 4.7, "gpu": "RTX 4060", "ram": "16GB"},
    "MSI Thin GF63":  {"price": 55000, "stock": 6,  "rating": 4.2, "gpu": "GTX 1650", "ram": "8GB"},
}
 
 
# =============================================================
# SECTION 3: TOOL FUNCTIONS (pure Python — no LLM)
# =============================================================
# Rule: Use Python for computation. Use LLM for reasoning.
# These functions are called BEFORE the GroupChat starts.
def find_best_product(need: str, budget: int) -> dict:
    """
    Find the best product based on user need and budget.
    Priority:
    1. Exact product/brand match
    2. Partial keyword match
    3. Best product within budget
    """
 
    need_lower = need.lower().strip()
 
    # Available products only
    available = {
        name: details
        for name, details in PRODUCT_CATALOG.items()
        if details["stock"] > 0
    }
 
    # -------------------------------------------------
    # 1. Exact match
    # -------------------------------------------------
    for name, details in available.items():
        if need_lower == name.lower():
            return {"product": name, **details}
 
    # -------------------------------------------------
    # 2. Partial keyword match
    # -------------------------------------------------
    for name, details in available.items():
        if need_lower in name.lower():
            return {"product": name, **details}
 
    # -------------------------------------------------
    # 3. Word-based matching
    # Example:
    # "Acer Nitro Gaming Laptop"
    # -------------------------------------------------
    words = need_lower.split()
 
    matches = []
 
    for name, details in available.items():
        score = 0
 
        for word in words:
            if word in name.lower():
                score += 10
 
        if score > 0:
            score += details["rating"]
 
            if details["price"] <= budget:
                score += 5
 
            matches.append((score, name, details))
 
    if matches:
        matches.sort(reverse=True)
        _, best_name, best_details = matches[0]
        return {"product": best_name, **best_details}
 
    # -------------------------------------------------
    # 4. No match found
    # Recommend best product within budget
    # -------------------------------------------------
    candidates = []
 
    for name, details in available.items():
 
        score = details["rating"] * 10
 
        if details["price"] <= budget:
            score += 20
 
        score -= abs(details["price"] - budget) / 5000
 
        candidates.append((score, name, details))
 
    candidates.sort(reverse=True)
 
    _, best_name, best_details = candidates[0]
 
    return {"product": best_name, **best_details}
 
def check_inventory(product_name: str) -> dict:
    """Check stock for a given product name."""
    for name, details in PRODUCT_CATALOG.items():
        if name.lower() in product_name.lower() or product_name.lower() in name.lower():
            return {
                "product":     name,
                "available":   details["stock"] > 0,
                "stock_count": details["stock"],
                "price":       details["price"],
                "rating":      details["rating"],
                "gpu":         details["gpu"],
                "ram":         details["ram"],
            }
    return {"product": product_name, "available": False, "stock_count": 0,
            "price": 0, "rating": 0, "gpu": "Unknown", "ram": "Unknown"}
 
 
def calculate_discount(price: int, budget: int) -> dict:
    """
    Calculate appropriate discount based on price vs budget.
    Within budget      -> 5% loyalty discount
    Up to 10% over     -> 8% to bring within budget
    Up to 15% over     -> 10% stretch discount
    Beyond 15% over    -> 0% (too far over budget)
    """
    if price <= budget:
        pct = 5
    elif price <= budget * 1.10:
        pct = 8
    elif price <= budget * 1.15:
        pct = 10
    else:
        pct = 0
 
    final = int(price * (1 - pct / 100))
    return {
        "original_price": price,
        "discount_pct":   pct,
        "final_price":    final,
        "within_budget":  final <= budget,
    }
 
 
def generate_order_id() -> str:
    """Generate unique order ID: ORD + 4 random digits."""
    return "ORD" + str(random.randint(1000, 9999))
 
 
def save_order(order_id, customer_name, product, original_price,
               discount_pct, final_price, decision) -> bool:
    """Save the completed order to SQLite. Returns True on success."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (order_id, customer_name, product, original_price, "
            "discount_pct, final_price, decision, timestamp) VALUES (?,?,?,?,?,?,?,?)",
            (order_id, customer_name, product, original_price, discount_pct,
             final_price, decision, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        console.print(f"[red]DB error: {e}[/red]")
        return False
 
 
def generate_invoice(order_id, customer_name, product, original_price,
                     discount_pct, final_price, decision) -> str:
    """Generate a formatted receipt string."""
    sep = "=" * 50
    row = [
        sep,
        "        SMART E-COMMERCE -- ORDER RECEIPT",
        sep,
        "Order ID       : " + str(order_id),
        "Date           : " + datetime.datetime.now().strftime("%d %b %Y  %H:%M"),
        sep,
        "Customer       : " + str(customer_name),
        "Product        : " + str(product),
        "Original Price : Rs " + "{:,}".format(original_price),
        "Discount       : " + str(discount_pct) + "%",
        "Final Price    : Rs " + "{:,}".format(final_price),
        sep,
        "Decision       : " + str(decision),
        sep,
        "Thank you for shopping with us!",
        sep,
    ]
    return "\n" + "\n".join(row) + "\n"
 
 
# =============================================================
# SECTION 4: LLM CONFIG
# =============================================================
 
config_list = [
    {
        "model":    "qwen2.5:3b",
        "base_url": "http://localhost:11434/v1",
        "api_key":  "ollama",
    }
]
 
llm_config = {"config_list": config_list, "temperature": 0.2}
 
 
# =============================================================
# SECTION 5: MAIN APPLICATION
# =============================================================
 
def run_ecommerce_system():
 
    setup_database()
 
    console.print("\n[bold magenta]=== SMART E-COMMERCE SYSTEM ===[/bold magenta]\n")
 
    customer_name = input("Customer Name  : ").strip() or "Shyni"
    budget_str    = input("Budget (Rs)    : ").strip()
    budget        = int(budget_str) if budget_str.isdigit() else 70000
    need          = input("What do you need? (e.g. gaming laptop): ").strip() or "gaming laptop"
 
    console.print("\n[cyan]Customer : " + customer_name + "[/cyan]")
    console.print("[cyan]Budget   : Rs " + "{:,}".format(budget) + "[/cyan]")
    console.print("[cyan]Need     : " + need + "[/cyan]\n")
 
    console.print("[bold yellow]Running tools...[/bold yellow]")
 
    product_data = find_best_product(need, budget)
    inv_data     = check_inventory(product_data["product"])
    disc_data    = calculate_discount(inv_data["price"], budget)
    order_id     = generate_order_id()
 
    table = Table(title="Tool Results", style="bold")
    table.add_column("Field",   style="cyan",  width=20)
    table.add_column("Value",   style="white", width=30)
    table.add_row("Product",        inv_data["product"])
    table.add_row("GPU",            inv_data["gpu"])
    table.add_row("RAM",            inv_data["ram"])
    table.add_row("Rating",         str(inv_data["rating"]) + " / 5.0")
    stock_str = str(inv_data["stock_count"]) + " units " + ("IN STOCK" if inv_data["available"] else "OUT OF STOCK")
    table.add_row("Stock",          stock_str)
    table.add_row("Original Price", "Rs " + "{:,}".format(inv_data["price"]))
    table.add_row("Discount",       str(disc_data["discount_pct"]) + "%")
    table.add_row("Final Price",    "Rs " + "{:,}".format(disc_data["final_price"]))
    table.add_row("Within Budget",  "Yes" if disc_data["within_budget"] else "No")
    table.add_row("Order ID",       order_id)
    console.print(table)
 
    status_str = "IN STOCK" if inv_data["available"] else "OUT OF STOCK"
 
    customer_agent = ConversableAgent(
        name="Customer",
        system_message=(
            "You are " + customer_name + ", a customer looking for a " + need + ". "
            "Your budget is Rs " + "{:,}".format(budget) + ". "
            "State your requirement. When StoreManager gives the final recommendation, "
            "say BUY if satisfied or PASS if not."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
 
    product_agent = ConversableAgent(
        name="ProductAgent",
        system_message=(
            "You are the Product Specialist. "
            "Recommended product: " + inv_data["product"] + ". "
            "GPU: " + inv_data["gpu"] + ", RAM: " + inv_data["ram"] + ", "
            "Rating: " + str(inv_data["rating"]) + "/5.0. "
            "Original price: Rs " + "{:,}".format(inv_data["price"]) + ". "
            "Explain in 2-3 sentences why this matches the customer need."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
 
    inventory_agent = ConversableAgent(
        name="InventoryAgent",
        system_message=(
            "You are the Inventory Manager. "
            + inv_data["product"] + " is " + status_str
            + " with " + str(inv_data["stock_count"]) + " units available. "
            "Report availability clearly. If stock is under 5 units, mention urgency."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
 
    pricing_agent = ConversableAgent(
        name="PricingAgent",
        system_message=(
            "You are the Pricing Analyst. "
            "Original price: Rs " + "{:,}".format(inv_data["price"]) + ". "
            "Customer budget: Rs " + "{:,}".format(budget) + ". "
            "Approved discount: " + str(disc_data["discount_pct"]) + "%. "
            "Final price after discount: Rs " + "{:,}".format(disc_data["final_price"]) + ". "
            "Within budget: " + str(disc_data["within_budget"]) + ". "
            "State these figures clearly in 2 sentences."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
 
    review_agent = ConversableAgent(
        name="ReviewAgent",
        system_message=(
            "You are the Customer Review Analyst. "
            + inv_data["product"] + " has a rating of "
            + str(inv_data["rating"]) + "/5.0. "
            "Classify as: Excellent (4.5+), Good (4.0-4.4), Average (3.5-3.9), or Poor. "
            "Give one sentence on what customers like or dislike."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
 
    manager_agent = ConversableAgent(
        name="StoreManager",
        system_message=(
            "You are the Store Manager. "
            "After hearing from ProductAgent, InventoryAgent, PricingAgent, and ReviewAgent, "
            "give ONE final recommendation to " + customer_name + ". "
            "Include: product name, final price Rs " + "{:,}".format(disc_data["final_price"]) + ", "
            "and order ID " + order_id + ". "
            "End your message with exactly one word on its own line: BUY or NEGOTIATE or PASS"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
 
    group_chat = GroupChat(
        agents=[customer_agent, product_agent, inventory_agent,
                pricing_agent, review_agent, manager_agent],
        messages=[],
        max_round=10,
        speaker_selection_method="auto"
    )
 
    gc_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
 
    console.print("\n[bold cyan]Starting 6-agent GroupChat...[/bold cyan]\n")
 
    customer_agent.initiate_chat(
        gc_manager,
        message=(
            "Hi everyone! I am " + customer_name + ". "
            "I am looking for a " + need + " with a budget of Rs "
            + "{:,}".format(budget) + ". "
            "Please help me make the best decision."
        )
    )
 
    final_decision = "BUY"
    for msg in reversed(group_chat.messages):
        if msg.get("name") == "StoreManager":
            content = msg.get("content", "").upper()
            if "PASS" in content:
                final_decision = "PASS"
            elif "NEGOTIATE" in content:
                final_decision = "NEGOTIATE"
            else:
                final_decision = "BUY"
            break
 
    save_order(order_id, customer_name, inv_data["product"],
               inv_data["price"], disc_data["discount_pct"],
               disc_data["final_price"], final_decision)
 
    invoice = generate_invoice(order_id, customer_name, inv_data["product"],
                               inv_data["price"], disc_data["discount_pct"],
                               disc_data["final_price"], final_decision)
 
    console.print(Panel(invoice, title="[bold green]ORDER RECEIPT[/bold green]", border_style="green"))
    console.print("[dim]Saved to: " + DB_PATH + "[/dim]")
 
    console.print("\n[bold yellow]=== ALL ORDERS IN DATABASE ===[/bold yellow]")
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, customer_name, product, final_price, decision, timestamp "
                   "FROM orders ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
 
    db_table = Table(style="bold")
    db_table.add_column("Order ID",  style="cyan")
    db_table.add_column("Customer",  style="white")
    db_table.add_column("Product",   style="white")
    db_table.add_column("Price",     style="green", justify="right")
    db_table.add_column("Decision",  style="yellow")
    db_table.add_column("Timestamp", style="dim")
    for row in rows:
        db_table.add_row(row[0], row[1], row[2], "Rs {:,}".format(row[3]), row[4], row[5])
    console.print(db_table)
    console.print("\nTotal orders: " + str(len(rows)))
 
    console.print("\n[bold yellow]=== SPEAKER STATS ===[/bold yellow]")
    counts = {}
    for msg in group_chat.messages:
        s = msg.get("name", msg.get("role", "?"))
        counts[s] = counts.get(s, 0) + 1
    for speaker, count in sorted(counts.items(), key=lambda x: -x[1]):
        console.print("  " + speaker.ljust(20) + " " + ("X" * count) + " (" + str(count) + ")")
 
 
# =============================================================
# ENTRY POINT
# =============================================================
 
if __name__ == "__main__":
    run_ecommerce_system()
 
 