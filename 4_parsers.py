#partial prefills the placeholder variables in the
#prompt template, so you only need to provide the 
#remaining variables when invoking the chain.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
 
# ---------------------------------------------------
# Load Local LLM from Ollama
# ---------------------------------------------------
 
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0,
    num_predict=512
)
 
# ---------------------------------------------------
# Define Structured Output Schema
# ---------------------------------------------------
 
class StudentProfile(BaseModel):
    name: str = Field(description="Student full name")
    department: str = Field(description="Department name")
    cgpa: float = Field(description="CGPA out of 10")
    risk_level: str = Field(description="low / medium / high")
 
# ---------------------------------------------------
# Create JSON Parser
# ---------------------------------------------------
 
parser = JsonOutputParser(
    pydantic_object=StudentProfile
)
 
# ---------------------------------------------------
# Prompt Template
# ---------------------------------------------------
 
profile_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extract student info as JSON.\n{format_instructions}"
    ),
    (
        "human",
        "{student_text}"
    )
]).partial(
    format_instructions=parser.get_format_instructions()
)
 
# ---------------------------------------------------
# Create LCEL Chain
# ---------------------------------------------------
 
profile_chain = profile_prompt | llm | parser
 
# ---------------------------------------------------
# Invoke Chain
# ---------------------------------------------------
 
result = profile_chain.invoke({
    "student_text": "Aaryan from Database dept, CGPA nine point three, thriving"
})
 
# ---------------------------------------------------
# Output
# ---------------------------------------------------
 
print("\n=== PARSED OUTPUT ===")
print(result)
 
print("\n=== OUTPUT TYPE ===")
print(type(result))