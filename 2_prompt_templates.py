from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {domain} engineer. Be concise"),
    ("human", "Explain {topic} with a real-world example")
])

formatted = prompt.format_messages(
    domain = "AI",
    topic = "ReAct agent pattern"
)

print(formatted)