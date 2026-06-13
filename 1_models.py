from langchain_ollama import ChatOllama

#temperature = 0 --> deterministic output, best for agents
#temperature = 1 --> more creative output for content generation

llm = ChatOllama(
    model="tinyllama:latest",
    temperature=0,
    num_predict=512  # max tokens per response
)

response = llm.invoke("What is ReAct in Agentic AI?")
print(response.content)

