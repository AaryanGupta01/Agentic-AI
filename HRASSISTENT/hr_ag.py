#==========================================================
# After running give input in this format: 
# You : name='Ravi' experience=4 skills=['python', 'git']
#==========================================================

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.vectorstores import FAISS
# ==================================
# MODEL
# ==================================
llm = ChatOllama(model="qwen2.5:3b")
# ==================================
# MEMORY
# ==================================
chat_history = InMemoryChatMessageHistory()
# ==================================
# LOAD VECTOR DB
# ==================================
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = FAISS.load_local(
 "hr_vector_db",
 embeddings,
 allow_dangerous_deserialization=True
)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})
#This returns 3 most relevant chunks from the vector database based on the input query.
# The retriever is used to fetch relevant information from the vector database, which can 
# then be used by the agent to generate informed responses to user queries.

# ==================================
# TOOLS
# ==================================

@tool
#tool decorator is used to define functions that can be called by the agent when processing user queries.
def experience_calculator(start_year: Optional[int] = None) -> str:
 """Calculate candidate experience""" # doc string provides a brief description of the function's purpose.
 if start_year is None:
     return "No start_year provided. Please provide a valid start year."
 return str(datetime.now().year - start_year)
 
@tool
def eligibility_checker(skills: str) -> str:
 """Check candidate eligibility"""
 required = {"python", "sql", "git"}
 candidate = {skill.strip().lower() for skill in skills.split(",")}
 missing = required - candidate
 if len(missing) == 0:
  return "Eligible"
 return "Not Eligible. Missing: " + ", ".join(missing)
 
@tool
def company_policy_search(question: str) -> str:
 """Use this for leave, notice period, holidays, handbook, work-from-home, dress code, and other company policy questions."""
 docs = retriever.invoke(question)
 context = "\n".join(doc.page_content for doc in docs)
 prompt = (
  "Use only the context provided below. "
  "If the answer is not in the context, say that the policy is not available in the documents.\n\n"
  f"Context:\n{context}\n\nQuestion:\n{question}"
 )
 return llm.invoke(prompt).content
 
@tool
def interview_questions(skills: str) -> str:
 """Generate interview questions"""
 prompt = f"Generate 5 interview questions for: {skills}"
 return llm.invoke(prompt).content
tools = [experience_calculator, eligibility_checker,
 company_policy_search, interview_questions]
 
# ==================================
# PROMPT
# ==================================
prompt = ChatPromptTemplate.from_messages([
 ("system", "You are an HR Recruitment Assistant. Use tools whenever required."),
 ("human", "{input}"),
 ("placeholder", "{agent_scratchpad}")
])
# ==================================
# AGENT
# ==================================
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# ==================================
# STRUCTURED OUTPUT
# ==================================
class Candidate(BaseModel):
 name: str
 experience: int
 skills: List[str]
structured_llm = llm.with_structured_output(Candidate)
# ==================================
# CHAT LOOP
# ==================================
POLICY_KEYWORDS = (
 "leave", "casual", "sick", "earned", "notice", "policy", "handbook",
 "holiday", "attendance", "work from home", "dress code", "working hours"
)
 
 
def is_policy_question(question: str) -> bool:
 question_lower = question.lower()
 return any(keyword in question_lower for keyword in POLICY_KEYWORDS)
 
 
print("=" * 60)
print("HR RECRUITMENT ASSISTANT")
print("=" * 60)
resume = ""
while True:
 user_input = input("\nYou : ").strip()
 if user_input.lower() == "exit":
   break
 
 if user_input.lower().startswith("resume:"):
   resume = user_input.split(":", 1)[1].strip()
   if not resume:
     print("\nPlease provide the resume text after 'resume:'")
     continue
 
   candidate = structured_llm.invoke(
     f"Extract Name, Experience, Skills\n\nResume:\n{resume}"
   )
   print("\nCandidate Details")
   print(candidate)
   continue
 
 if is_policy_question(user_input):
   answer = company_policy_search.invoke({"question": user_input})
   print("\nAssistant:", answer)
   continue
 
 response = agent_executor.invoke({"input": user_input})
 print("\nAssistant:", response["output"])