from langchain_ollama import ChatOllama

class Agent:
 
    def __init__(self,name):
        self.name=name
 
    def respond(self,message):
 
        return f"{self.name}: handled {message}"
 
planner=Agent("Planner")
executor=Agent("Executor")
monitor=Agent("Monitor")
 
history=[]
 
msg="Deploy Inventory Service"

llm = ChatOllama(
    model = "qwen2.5:3b",
    temperature = 0,
    token_limit = 200
)
 
response=planner.respond(msg)
llm_response = llm.invoke(response)
llm_summary = llm.invoke(f"Summarize the following: {llm_response}")
history.append(llm_summary)
 
response=executor.respond(llm_response)
llm_response = llm.invoke(response)
llm_summary = llm.invoke(f"Summarize the following: {llm_response}")
history.append(llm_summary)
 
response=monitor.respond(llm_response)
llm_response = llm.invoke(response)
llm_summary = llm.invoke(f"Summarize the following: {llm_response}")
history.append(llm_summary)
 
for h in history:
    print(h)