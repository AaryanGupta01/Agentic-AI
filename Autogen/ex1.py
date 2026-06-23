# =============================================================
# HANDS-ON 1 — Basic AutoGen Agents (No LLM)
# =============================================================
 
from autogen import ConversableAgent
 
# -------------------------------------------------------------
# STEP 1: Create Two Agents with NO LLM
# -------------------------------------------------------------
 
 
 
teacher = ConversableAgent(
    name="TeacherAgent",
    llm_config=False,
    human_input_mode="NEVER"
)
 
student = ConversableAgent(
    name="StudentAgent",
    llm_config=False,
    human_input_mode="NEVER"
)
 
print(f"Agent 1 created: {teacher.name}")
print(f"Agent 2 created: {student.name}")
 
 
# -------------------------------------------------------------
# STEP 2: Send Messages Between Agents
# -------------------------------------------------------------
 
print("\n--- Teacher sends a question ---")
teacher.send(
    message="What is Python?",
    recipient=student,
    request_reply=False
)
 
print("--- Student sends an answer ---")
student.send(
    message="Python is a high-level programming language used for AI, web, and data science.",
    recipient=teacher,
    request_reply=False
)
 
print("\nMessages exchanged!")
 
 
# -------------------------------------------------------------
# STEP 3: Read Message History
# -------------------------------------------------------------
# chat_messages = {partner_agent: [{"role": ..., "content": ...}]}
# -------------------------------------------------------------
 
print("\n=== TeacherAgent Message History ===")
for msg in teacher.chat_messages.get(student, []):
    print(f"  [{msg['role'].upper()}] {msg['content']}")
 
print("\n=== StudentAgent Message History ===")
for msg in student.chat_messages.get(teacher, []):
    print(f"  [{msg['role'].upper()}] {msg['content']}")
 
 
# -------------------------------------------------------------
# STEP 4: Three-Agent Classroom
# -------------------------------------------------------------
 
print("\n\n=== THREE-AGENT CLASSROOM ===\n")
 
teacher2  = ConversableAgent(name="Teacher",  llm_config=False, human_input_mode="NEVER")
student_a = ConversableAgent(name="StudentA", llm_config=False, human_input_mode="NEVER")
student_b = ConversableAgent(name="StudentB", llm_config=False, human_input_mode="NEVER")
 
question = "What is the difference between AI and Machine Learning?"
 
teacher2.send(message=question, recipient=student_a, request_reply=False)
teacher2.send(message=question, recipient=student_b, request_reply=False)
 
student_a.send(
    message="AI is the broad concept of machines being smart. ML is a subset where machines learn from data.",
    recipient=teacher2, request_reply=False
)
student_b.send(
    message="AI makes machines intelligent. ML lets machines improve through experience without being explicitly programmed.",
    recipient=teacher2, request_reply=False
)
 
print(f"Teacher asked: {question}")
print("\nAnswers received by Teacher:")
for partner in [student_a, student_b]:
    for msg in teacher2.chat_messages.get(partner, []):
        if msg["role"] == "user":
            print(f"  {partner.name}: {msg['content']}")
 
 
# -------------------------------------------------------------
# STEP 5: HR Department Example
# -------------------------------------------------------------
 
print("\n\n=== HR DEPARTMENT EXAMPLE ===\n")
 
hr        = ConversableAgent(name="HR",        llm_config=False, human_input_mode="NEVER")
developer = ConversableAgent(name="Developer", llm_config=False, human_input_mode="NEVER")
designer  = ConversableAgent(name="Designer",  llm_config=False, human_input_mode="NEVER")
 
hr.send(message="Please submit your weekly report by 5 PM today.",
        recipient=developer, request_reply=False)
hr.send(message="Please submit your weekly report by 5 PM today.",
        recipient=designer,  request_reply=False)
 
developer.send(message="Report submitted: Completed authentication module, fixed 3 API bugs.",
               recipient=hr, request_reply=False)
designer.send(message="Report submitted: Completed landing page redesign, delivered 5 new UI components.",
              recipient=hr, request_reply=False)
 
print("HR broadcast the weekly report request.")
print("\nHR received:")
for partner in [developer, designer]:
    for msg in hr.chat_messages.get(partner, []):
        if msg["role"] == "user":
            print(f"  {partner.name}: {msg['content']}")
 
print("\n=== Hands-on 1 Complete ===")
print("Next step: Hands-on 2 — Replace llm_config=False with Qwen 2.5 via Ollama")