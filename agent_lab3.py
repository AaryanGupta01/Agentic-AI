from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain_ollama import ChatOllama
 
# Import tools from customtools.py
from custom_tools import calculator, student_lookup, grade_calculator
 
# ===================================================
# LLM
# ===================================================
 
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)
 
# ===================================================
# TOOLS
# ===================================================
 
tools = [
    calculator,
    student_lookup,
    grade_calculator
]
 
# ===================================================
# MEMORY
# ===================================================
 
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=0
)
"""
It keeps only the last k messages in memory. 
Setting k=0 means it will keep all messages.
"""
# ===================================================
# CONVERSATIONAL AGENT
# ===================================================
 
conv_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    max_iterations=5
)

"""
AgentType.CONVERSATIONAL_REACT_DESCRIPTION is a type of agent 
that uses a conversational approach to interact with the user.
It generates responses based on the conversation history and 
the tools available, allowing for a more dynamic and context-aware interaction.
"""
 
# ===================================================
# TURN 1
# ===================================================
 
r1 = conv_agent.invoke({
    "input": "Look up Priya"
})
 
print("\n=== TURN 1 ===")
print(r1["output"])
 
# ===================================================
# TURN 2
# ===================================================
 
r2 = conv_agent.invoke({
    "input": "What is 10% of her CGPA?"
})
 
print("\n=== TURN 2 ===")
print(r2["output"])

# ===================================================
# TURN 3
# ===================================================

r3 = conv_agent.invoke({
    "input": "Calculate the grade for marks 88, 92, 76, 85, 90"
})
 
print("\n=== TURN 3 ===")
print(r3["output"])
 
# ===================================================
# MEMORY CONTENT
# ===================================================
 
print("\n=== MEMORY ===")
 
msgs = memory.chat_memory.messages
 
for m in msgs:
    print(f"[{m.type.upper()}] {m.content}")
 
"""
Write a new @tool called grade_calculator that takes five marks as a comma-separated string,
computes the average, and returns the grade: A (>=90), B (>=75), C (>=60), F (<60). Add it to
agent_lab3.py tools list. Test: 'Calculate the grade for marks 88, 92, 76, 85, 90'
"""