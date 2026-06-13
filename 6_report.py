import json
from langchain.memory import ConversationBufferWindowMemory
 
# ---------------------------------------------------
# Create memory
# ---------------------------------------------------
 
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5
)
 
# ---------------------------------------------------
# Add sample conversation manually
# ---------------------------------------------------
 
memory.chat_memory.add_user_message("Look up Priya")
 
memory.chat_memory.add_ai_message(
    "Priya is in Cyber Security. CGPA: 9.1. Risk: Low."
)
 
memory.chat_memory.add_user_message(
    "What is 10% of her CGPA?"
)
 
memory.chat_memory.add_ai_message(
    "10% of Priya's CGPA (9.1) is 0.91."
)
 
# ---------------------------------------------------
# Convert memory messages into JSON format
# ---------------------------------------------------
 
msgs = memory.chat_memory.messages
 
report = [
    {
        "role": m.type,
        "content": m.content
    }
    for m in msgs
]
 
# ---------------------------------------------------
# Save JSON file
# ---------------------------------------------------
 
with open("session_report.json", "w") as f:
    json.dump(report, f, indent=2)
 
print(f"Saved {len(report)} messages to session_report.json")
 
# ---------------------------------------------------
# Print JSON contents to terminal
# ---------------------------------------------------
 
print("\nsession_report.json contents\n")
 
print(
    json.dumps(
        report,
        indent=2
    )
)