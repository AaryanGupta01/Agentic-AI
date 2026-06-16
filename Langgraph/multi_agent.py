from typing import TypedDict
from langgraph.graph import StateGraph, END
 
 
# ==================================================
# STATE
# ==================================================
 
class HRState(TypedDict):
 
    candidate_name: str
    resume_text: str
 
    screening_result: str
    next_agent: str
 
    skill_score: int
    interview_result: str
 
    final_decision: str
 
 
# ==================================================
# AGENT 1 : RESUME AGENT
# ==================================================
 
def resume_agent(state: HRState):
 
    text = state["resume_text"].lower()
 
    if "python" in text:
 
        result = "selected"
 
    elif "java" in text:
 
        result = "selected"
 
    elif "sql" in text:
 
        result = "hold"
 
    else:
 
        result = "rejected"
 
    print("\nResume Agent Executed")
 
    return {
        "screening_result": result
    }
 
 
# ==================================================
# AGENT 2 : SUPERVISOR AGENT
# ==================================================
 
def supervisor_agent(state: HRState):
 
    result = state["screening_result"]
 
    if result == "selected":
 
        next_agent = "skill_agent"
 
    elif result == "hold":
 
        next_agent = "interview_agent"
 
    else:
 
        next_agent = "end"
 
    print("\nSupervisor Agent Executed")
 
    return {
        "next_agent": next_agent
    }
 
 
# ==================================================
# AGENT 3 : SKILL AGENT
# ==================================================
 
def skill_agent(state: HRState):
 
    text = state["resume_text"].lower()
 
    if "python" in text:
 
        score = 90
 
    elif "java" in text:
 
        score = 85
 
    else:
 
        score = 75
 
    print("\nSkill Agent Executed")
 
    return {
        "skill_score": score
    }
 
 
# ==================================================
# AGENT 4 : INTERVIEW AGENT
# ==================================================
 
def interview_agent(state: HRState):
 
    print("\nInterview Agent Executed")
 
    return {
        "interview_result":
        "Strong Communication"
    }
 
 
# ==================================================
# AGENT 5 : DECISION AGENT
# ==================================================
 
def decision_agent(state: HRState):
 
    score = state.get("skill_score", 0)
 
    if score >= 90:
 
        decision = "Strong Hire"
 
    elif score >= 80:
 
        decision = "Hire"
 
    elif score >= 70:
 
        decision = "Consider"
 
    else:
 
        decision = "Reject"
 
    print("\nDecision Agent Executed")
 
    return {
        "final_decision": decision
    }
 
 
# ==================================================
# SUPERVISOR ROUTER
# ==================================================
 
def supervisor_router(state: HRState):
 
    next_agent = state["next_agent"]
 
    if next_agent == "skill_agent":
 
        return "skill_agent"
 
    elif next_agent == "interview_agent":
 
        return "interview_agent"
 
    else:
 
        return END
 
 
# ==================================================
# BUILD GRAPH
# ==================================================
 
builder = StateGraph(HRState)
 
 
# ==================================================
# REGISTER AGENTS
# ==================================================
 
builder.add_node(
    "resume_agent",
    resume_agent
)
 
builder.add_node(
    "supervisor_agent",
    supervisor_agent
)
 
builder.add_node(
    "skill_agent",
    skill_agent
)
 
builder.add_node(
    "interview_agent",
    interview_agent
)
 
builder.add_node(
    "decision_agent",
    decision_agent
)
 
 
# ==================================================
# ENTRY POINT
# ==================================================
 
builder.set_entry_point(
    "resume_agent"
)
 
 
# ==================================================
# FLOW
# ==================================================
 
builder.add_edge(
    "resume_agent",
    "supervisor_agent"
)
 
builder.add_conditional_edges(
    "supervisor_agent",
    supervisor_router
)
 
builder.add_edge(
    "skill_agent",
    "interview_agent"
)
 
builder.add_edge(
    "interview_agent",
    "decision_agent"
)
 
builder.add_edge(
    "decision_agent",
    END
)
 
 
# ==================================================
# COMPILE GRAPH
# ==================================================
 
graph = builder.compile()
 
 
# ==================================================
# TEST CASE 1
# ==================================================
 
print("\n==============================")
print("PYTHON CANDIDATE")
print("==============================")
 
result = graph.invoke(
    {
        "candidate_name": "John",
        "resume_text":
        "React Developer with 3 years experience"
    }
)
 
print("\nFinal Output")
print(result)