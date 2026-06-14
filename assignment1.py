from typing import List
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ==========================================
# 1. DEFINING THE TOOLS
# ==========================================

@tool
def calculate_attendance(total_classes: int, attended_classes: int) -> dict:
    """
    Calculates the attendance percentage and exam eligibility status.
    Inputs: Total Classes, Attended Classes
    Outputs: Attendance Percentage, Exam Eligibility Status.
    """
    if total_classes <= 0:
        return {"error": "Total classes must be greater than 0."}
    percentage = (attended_classes / total_classes) * 100
    eligible = "Eligible for Exam" if percentage >= 75 else "Not Eligible for Exam"
    return {"attendance_percentage": f"{percentage:.2f}%", "status": eligible}

@tool
def calculate_result(marks: List[float]) -> dict:
    """
    Provided the list of marks of a student in 5 subjects, calculate the grade, average marks and pass/fail status.
    Inputs: Marks of 5 Subjects
    Outputs: Average Marks, Grade, Pass/Fail Status
    """
    if not marks:
        return {"error": "Marks list cannot be empty."}
    average = sum(marks) / len(marks)
    if average >= 90: grade = "A"
    elif average >= 75: grade = "B"
    elif average >= 60: grade = "C"
    else: grade = "D"
    status = "Pass" if average >= 50 else "Fail"
    return {"average_marks": round(average, 2), "grade": grade, "status": status}

@tool
def calculate_fee_balance(total_fee: float, amount_paid: float) -> dict:
    """Calculates the balance fee remaining from the Inputs given: Total Course Fee and Amount Paid.
    Inputs: Total Course Fee, Amount Paid
    Output: Pending Fee Amount"""
    return {"pending_fee_amount": total_fee - amount_paid}

@tool
def calculate_library_fine(delayed_days: int) -> dict:
    """Calculates the library fine based on the number of delayed days.
    based on the Rule 
    Rule: Fine = ₹5 * Delayed Days
    Input: Number of Delayed Days
    Output: Fine Amount"""
    return {"fine_amount": f"₹{5 * delayed_days}"}

@tool
def calculate_hostel_fee(monthly_fee: float, months_stayed: int) -> dict:
    """Calculates the total hostel fee based on the monthly fee and number of months stayed.
    Inputs: Monthly Hostel Fee, Number of Months
    Output: Total Hostel Fee"""
    return {"total_hostel_fee": monthly_fee * months_stayed}

@tool
def get_student_information(student_id: str) -> dict:
    """Retrieves student details using Student ID string, e.g., 'STU101'"""
    student_db = {
        "STU101": {"name": "Alice Smith", "major": "Computer Science", "year": "2nd Year"},
        "STU102": {"name": "Bob Jones", "major": "Mechanical Engineering", "year": "3rd Year"}
    }
    return student_db.get(student_id.upper(), {"error": "Student ID not found."})

# ==========================================
# 2. LOCAL OLLAMA AGENT CONFIGURATION 
# ==========================================

tools = [
    calculate_attendance,
    calculate_result,
    calculate_fee_balance,
    calculate_library_fine,
    calculate_hostel_fee,
    get_student_information
]


llm = ChatOllama(
    model="qwen2.5:3b",  
    temperature=0
)


prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a strict, logical assistant with access to calculator tools. "
        "CRITICAL RULES: "
        "1. If a user asks a multi-part question, you MUST execute ALL necessary tools one by one before providing any final response to the user. "
        "2. Do not attempt to calculate anything yourself. Always use the tools. "
        "3. Only write your final response AFTER you have gathered the observations from every required tool."
    )),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True
)


# ==========================================
# 3. RUN TESTING EXECUTIONS
# ==========================================

def run_query(query_text: str):
    print(f"\n{'='*50}\nUser Query: {query_text}\n{'='*50}")
    try:
        response = agent_executor.invoke({"input": query_text})
        print(f"\nFinal Response:\n{response['output']}\n")
    except Exception as e:
        print(f"\nExecution Failed: {e}\n")

if __name__ == "__main__":
    run_query("I attended 72 classes out of 90. Am I eligible for exams?")

    run_query("My marks are 95, 90, 88, 91 and 87. What is my grade?")

    run_query("My course fee is 50000 and I have paid 35000. How much fee is pending?")

    run_query("I returned a library book 8 days late. What is the fine amount?")

    run_query("Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.")

    run_query("""
    I attended 80 classes out of 100.
    My marks are 90, 85, 88, 92 and 95.
    My course fee is 60000 and I paid 45000.
    
    Provide:
    1. Attendance Status
    2. Grade
    3. Pending Fee
    """)