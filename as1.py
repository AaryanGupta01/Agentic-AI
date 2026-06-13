from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

@tool
def calculate_attendance(total_classes: int,attended_classes: int) -> dict:
    """
    Calculates the attendance percentage and exam eligibility status.
    Inputs: Total Classes, Attended Classes
    Outputs: Attendance Percentage, Exam Eligibility Status.
    """
    attendance_percentage = (attended_classes / total_classes) * 100 
    if attendance_percentage >= 75:
        eligible = "Eligible"
    else:
        eligible = "Not Eligible"
    return {"attendance_percentage": f"{attendance_percentage:.2f}%", "status": eligible}

@tool
def result_calculator(marks: list)-> dict:
    """
    Provided the list of marks of a student in 5 subjects, calculate the grade, average marks and pass/fail status.
    Inputs: Marks of 5 Subjects
    Outputs: Average Marks, Grade, Pass/Fail Status
    """
    avg_marks = sum(marks) / len(marks)
    if avg_marks >= 90:
        grade = "A"
    elif avg_marks >= 75 and avg_marks <= 89:
        grade = "B"
    elif avg_marks >= 60 and avg_marks <= 74:
        grade = "C"
    elif avg_marks < 60:
        grade = "D"
    if avg_marks >= 50:
        status = "Pass"
    else:       
        status = "Fail"
    return {
        "average_marks": round(avg_marks,2),
        "grade": grade,
        "status": status 
    }

@tool
def fee_balance_calculator(course_fee: int, amount_paid: int) -> int:
    """
    Calculates the balance fee remaining from the Inputs given: Total Course Fee and Amount Paid.
    Inputs: Total Course Fee, Amount Paid
    Output: Pending Fee Amount
    """
    return course_fee - amount_paid

@tool
def library_fine(delayed_days: int) -> int:
    """
    Calculates the library fine based on the number of delayed days.
    based on the Rule 
    Rule: Fine = ₹5 * Delayed Days
    Input: Number of Delayed Days
    Output: Fine Amount
    """
    return 5*delayed_days

@tool
def hostel_fee_calculator(monthly_hostel_fee: int, number_of_months: int) -> int:
    """
    Calculates the total hostel fee based on the monthly fee and number of months stayed.
    Inputs: Monthly Hostel Fee, Number of Months
    Output: Total Hostel Fee
    """
    return monthly_hostel_fee * number_of_months

@tool
def 
