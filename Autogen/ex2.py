# =============================================================
# HANDS-ON 2 — Retail Chat using Local LLM (Qwen 2.5 via Ollama)
# =============================================================
 
 
from autogen import ConversableAgent
 
print("\n=== HANDS-ON 2: RETAIL CHAT WITH LOCAL LLM ===\n")
 
 
# -------------------------------------------------------------
# STEP 1: LLM Configuration
# -------------------------------------------------------------
# AutoGen uses OpenAI-compatible API format.
# Ollama exposes this at http://localhost:11434/v1
 
config_list = [
    {
        "model":    "qwen2.5:3b",
        "base_url": "http://localhost:11434/v1",
        "api_key":  "ollama",
    }
]
 
llm_config = {
    "config_list": config_list,
    "temperature": 0,   # 0 = deterministic responses
    "cache_seed": None, # Disable disk cache to avoid sqlite3 I/O errors
}
 
print("LLM Config:")
print(f"  Model   : {config_list[0]['model']}")
print(f"  Endpoint: {config_list[0]['base_url']}")
 
 
# -------------------------------------------------------------
# STEP 2: Create Agents with system_message
# -------------------------------------------------------------
 
customer_agent = ConversableAgent(
    name="CustomerAgent",
    system_message=(
        "You are a college student in India looking for a smartphone.\n"
        "Your budget is Rs 20,000.\n"
        "You want: good camera for Instagram, long battery life (all-day use), "
        "and smooth performance for college apps.\n"
        "Ask at least 2 specific questions before deciding.\n"
        "When you are satisfied, say PURCHASE CONFIRMED on its own line."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=4
    # max_consecutive_auto_reply: how many times this agent replies in a row
    # without a break. Safety guard against looping.
)
 
retail_agent = ConversableAgent(
    name="RetailAdvisor",
    system_message=(
        "You are an expert smartphone retail advisor in India.\n"
        "You know every phone under Rs 20,000: Redmi Note series, Poco X series, "
        "Samsung M series, Realme Narzo, iQOO Z series.\n"
        "For every recommendation include: model name, price in Rs, "
        "camera megapixels, battery mAh, and one key strength.\n"
        "Be concise. When customer says PURCHASE CONFIRMED, "
        "reply with a one-line congratulation and purchase summary."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=4
)
 
print(f"\nAgent 1: {customer_agent.name} — budget Rs 20,000")
print(f"Agent 2: {retail_agent.name}   — smartphone expert")
 
 
# -------------------------------------------------------------
# STEP 3: Start the Conversation with initiate_chat()
# -------------------------------------------------------------
 
print("\n--- Starting retail conversation ---\n")
 
chat_result = customer_agent.initiate_chat(
    retail_agent,
    message="Hi! I need a smartphone under Rs 20,000 for college. "
            "I want a great camera and all-day battery. What do you suggest?",
    max_turns=5
)
 
 
# -------------------------------------------------------------
# STEP 4: Conversation Summary
# -------------------------------------------------------------
 
print("\n\n=== CONVERSATION SUMMARY ===")
print(f"Total messages exchanged: {len(chat_result.chat_history)}")
print("\nFull transcript:")
for i, msg in enumerate(chat_result.chat_history):
    name    = msg.get("name", msg.get("role", "?"))
    content = msg.get("content", "")
    short   = content[:200] + ("..." if len(content) > 200 else "")
    print(f"\n[{i+1}] {name}:\n  {short}")
 
 
# -------------------------------------------------------------
# STEP 5: Different Scenario — Laptop Purchase
# -------------------------------------------------------------
 
print("\n\n=== SCENARIO 2: LAPTOP PURCHASE ===\n")
 
student_buyer = ConversableAgent(
    name="VITStudent",
    system_message=(
        "You are a VIT University student buying a laptop for Python and Java coding "
        "and watching video lectures. Budget: Rs 55,000. "
        "You need at least 8GB RAM and 8+ hour battery. "
        "Ask 2 questions before deciding. Say LAPTOP CONFIRMED when ready to buy."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3
)
 
laptop_advisor = ConversableAgent(
    name="LaptopAdvisor",
    system_message=(
        "You are a laptop retail expert in India. "
        "Recommend models under Rs 55,000 for coding and study. "
        "Always mention: model name, price, RAM, storage, battery life, processor. "
        "Narrow to ONE best recommendation after the student asks questions. "
        "When student says LAPTOP CONFIRMED, give a short purchase summary."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3
)
 
laptop_chat = student_buyer.initiate_chat(
    laptop_advisor,
    message="Hi, I need a laptop under Rs 55,000 for college. "
            "I will use it for Python coding and online classes.",
    max_turns=5
)
 
 
 
 