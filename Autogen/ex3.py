# =============================================================
 
# HANDS-ON 3 — GroupChat Retail (ROUND ROBIN VERSION)
 
# =============================================================
 
 
from autogen import ConversableAgent, GroupChat, GroupChatManager
 
print("\n=== HANDS-ON 3: GROUPCHAT RETAIL (ROUND ROBIN) ===\n")
 
# -------------------------------------------------------------
 
# STEP 1: LLM CONFIGURATION
 
# -------------------------------------------------------------
 
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
 
print("LLM Ready: qwen2.5:3b via Ollama")
 
# -------------------------------------------------------------
 
# STEP 2: CUSTOMER AGENT
 
# -------------------------------------------------------------
 
customer = ConversableAgent(
name="Customer",
system_message=(
"You are a customer looking for a gaming laptop under Rs 70,000. "
"You need 16GB RAM, RGB keyboard and a good GPU. "
"When you are happy with the recommendation, say DEAL ACCEPTED."
),
llm_config=llm_config,
human_input_mode="NEVER"
)
 
# -------------------------------------------------------------
 
# STEP 3: PRODUCT EXPERT
 
# -------------------------------------------------------------
 
product_expert = ConversableAgent(
name="ProductExpert",
system_message=(
"You are a gaming laptop specialist. "
"Recommend ONE laptop from:\n"
"1. Lenovo LOQ - Rs 68,000 - RTX 4050 - 16GB RAM\n"
"2. ASUS TUF A15 - Rs 72,000 - RTX 4060 - 16GB RAM\n"
"3. HP Victus 15 - Rs 58,000 - GTX 1650 - 8GB RAM\n\n"
"Mention laptop name, GPU, RAM and price."
),
llm_config=llm_config,
human_input_mode="NEVER"
)
 
# -------------------------------------------------------------
 
# STEP 4: BUDGET EXPERT
 
# -------------------------------------------------------------
 
budget_expert = ConversableAgent(
name="BudgetExpert",
system_message=(
"You are a pricing analyst. "
"Check whether the recommendation fits within Rs 70,000. "
"Respond with:\n"
"Within Budget\n"
"Slightly Over Budget\n"
"Over Budget\n"
"Suggest discounts if needed."
),
llm_config=llm_config,
human_input_mode="NEVER"
)
 
# -------------------------------------------------------------
 
# STEP 5: STORE MANAGER
 
# -------------------------------------------------------------
 
store_manager = ConversableAgent(
name="StoreManager",
system_message=(
"You are the store manager. "
"Read all previous recommendations and provide ONE final decision. "
"Mention final price and one reason to buy."
),
llm_config=llm_config,
human_input_mode="NEVER"
)
 
print("\nAgents Created:")
print("  Customer")
print("  ProductExpert")
print("  BudgetExpert")
print("  StoreManager")
 
# -------------------------------------------------------------
 
# STEP 6: BUILD GROUPCHAT
 
# -------------------------------------------------------------
 
print("\n--- Building GroupChat (ROUND ROBIN) ---")
 
group_chat = GroupChat(
agents=[
customer,
product_expert,
budget_expert,
store_manager
],
messages=[],
max_round=8,
speaker_selection_method="round_robin"
)
 
manager = GroupChatManager(
groupchat=group_chat,
llm_config=llm_config
)
 
print(f"Agents in room : {[a.name for a in group_chat.agents]}")
print(f"Max rounds     : {group_chat.max_round}")
print(f"Speaker method : {group_chat.speaker_selection_method}")
 
# -------------------------------------------------------------
 
# STEP 7: START CONVERSATION
 
# -------------------------------------------------------------
 
print("\n=== RETAIL GROUP CHAT ===\n")
 
result = customer.initiate_chat(
manager,
message=(
"Hi team! I need a gaming laptop under Rs 70,000. "
"I want a good GPU, 16GB RAM and RGB keyboard. "
"Please suggest the best option."
)
)
 
# -------------------------------------------------------------
 
# STEP 8: ANALYSIS
 
# -------------------------------------------------------------
 
print("\n\n=== CONVERSATION ANALYSIS ===")
 
messages = group_chat.messages
 
print(f"Total Messages : {len(messages)}")
 
print("\nSpeaker Breakdown:")
 
counts = {}
 
for msg in messages:
 speaker = msg.get("name", msg.get("role", "?"))
counts[speaker] = counts.get(speaker, 0) + 1
 
for speaker, count in counts.items():
 print(f"  {speaker:<20} ({count})")
 
# -------------------------------------------------------------
 
# STEP 9: SPEAKING ORDER
 
# -------------------------------------------------------------
 
print("\nSpeaking Order:")
 
for i, msg in enumerate(messages):
 speaker = msg.get("name", msg.get("role", "?"))
print(f"  Turn {i+1:2d}: {speaker}")
 
 
 
 