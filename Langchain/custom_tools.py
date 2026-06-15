from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import ChatOllama
 
# ===================================================
# LOAD LOCAL LLM
# ===================================================
 
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)
 
# ===================================================
# CALCULATOR TOOL
# ===================================================
 
@tool
def calculator(expression: str) -> str:
    """
    Evaluates a safe math expression.
    Example Input: '2 + 2 * 3'
    """
 
    # -----------------------------------------------
    # Clean ReAct-style agent input
    # -----------------------------------------------
 
    expression = expression.replace("expression=", "")
    expression = expression.replace('"', "")
    expression = expression.replace("'", "")
    expression = expression.strip()
 
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )
 
        return str(result)
 
    except Exception as e:
        return f"Error: {e}"
 
# ===================================================
# STUDENT LOOKUP TOOL
# ===================================================
 
@tool
def student_lookup(name: str) -> str:
    """
    Look up a student by name.
    Returns department, CGPA, and risk level.
    """
 
    # -----------------------------------------------
    # Clean ReAct-style agent input
    # -----------------------------------------------
 
    name = name.replace("name=", "")
    name = name.replace('"', "")
    name = name.replace("'", "")
    name = name.strip()
 
    db = {
        "Priya": "Dept: Cyber Security | CGPA: 9.1 | Risk: Low",
        "Arjun": "Dept: AI & ML | CGPA: 6.8 | Risk: Medium",
        "Deepika": "Dept: Data Science | CGPA: 8.5 | Risk: Low",
    }
 
    return db.get(
        name,
        f"Student '{name}' not found."
    )
 
@tool
def grade_calculator(marks: str) -> str:
    """
    Computes the average and the grade for five marks.
    Input: A comma-separated string of 5 numbers (e.g., '88, 92, 76, 85, 90').
    Output: Returns a string containing both the calculated average and the letter grade.
    """
    try:
        # Convert string to list of floats
        marks_list = [float(m.strip()) for m in marks.split(",")]
        
        if len(marks_list) != 5:
            return "Error: Please provide exactly five marks."
        
        average = sum(marks_list) / len(marks_list)
        
        # Determine grade
        if average >= 90: grade = "A"
        elif average >= 75: grade = "B"
        elif average >= 60: grade = "C"
        else: grade = "F"
        
        # Explicitly label the output to ensure the LLM reports both parts
        return f"AVERAGE_MARK: {average:.2f}, FINAL_GRADE: {grade}"
    
    except Exception as e:
        return f"Error calculating grade: {e}"

# ===================================================
# TEST TOOLS DIRECTLY
# ===================================================
 
print("\n=== CALCULATOR TOOL TEST ===")
 
print(
    calculator.invoke({
        "expression": "(88+92+76+85+90)/5"
    })
)
 
print(
    calculator.invoke({
        "expression": "1/0"
    })
)
 
print("\n=== TOOL NAME ===")
print(calculator.name)
 
print("\n=== TOOL DESCRIPTION ===")
print(calculator.description)
 
print("\n=== STUDENT LOOKUP TOOL TEST ===")
 
print(
    student_lookup.invoke({
        "name": "Priya"
    })
)
 
print(
    student_lookup.invoke({
        "name": "Ravi"
    })
)
 
# ===================================================
# CREATE REACT AGENT
# ===================================================
 
tools = [
    calculator,
    student_lookup
]
 
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5
)
"""
1. agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION:

This is the "Reasoning Engine" and the most critical part of the configuration:

Zero-Shot: It means the agent does not need "few-shot" examples to learn how to use the tools; it relies on the descriptions you provided in the @tool docstrings.

ReAct (Reason + Act): This is the specific logic pattern the agent follows. It forces the LLM to think in a loop: Thought (Reasoning about the task) ---> Action (Choosing a tool) ---> Observation (The result from the tool).

Description: It requires that every tool in your tools list has a clear, accurate description. The agent uses these descriptions to decide which tool to pick.

2. verbose=True:

This is the "Transparency Flag." When set to True, it forces the agent to print its internal "chain of thought" to your console in real-time. This includes the "Thought," "Action," "Action Input," and "Observation" steps.

If you set this to False, the agent will perform all that work in the background and only return the final result.

3. max_iterations=5

This is the "Safety Valve." Because agents work in a loop (Reason --> Act --> Observe), there is a risk they could get stuck in an infinite loop if they are confused or if a tool keeps returning errors. 

This parameter tells the agent: "If you haven't arrived at a final answer in 5 attempts, stop and return an error." This prevents your script from running forever and consuming unnecessary tokens or system resources.
"""
 
# ===================================================
# RUN AGENT
# ===================================================
 
result = agent.invoke({
    "input": "What is Priya's CGPA and 15% of it?"
})
 
# ===================================================
# FINAL OUTPUT
# ===================================================
 
print("\n=== FINAL ANSWER ===")
print(result["output"])
 