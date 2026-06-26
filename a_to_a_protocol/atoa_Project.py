#This file demonstrates a simple incident management system using a multi-agent architecture.
# includes classes for AgentCard, AgentRegistry, Message, Task, and various agents 
# (MonitoringAgent, InfrastructureAgent, SecurityAgent, ResolutionAgent, PlannerAgent).
import uuid
import json
from datetime import datetime
 
# ==========================================================
# AGENT CARD
# ==========================================================
 
class AgentCard:
 
    def __init__(self, name, skills):
 
        self.name = name
        self.skills = skills
 
# ==========================================================
# AGENT REGISTRY
# ==========================================================
 
class AgentRegistry:
 
    def __init__(self):
 
        self.agents = {}
 
    def register(self, agent_card):
 
        self.agents[agent_card.name] = agent_card
 
    def list_agents(self):
 
        print("\nREGISTERED AGENTS")
 
        for name, card in self.agents.items():
 
            print(f"{name} -> {card.skills}")
 
# ==========================================================
# MESSAGE
# ==========================================================
 
class Message:
 
    def __init__(self, sender, receiver, content):
 
        self.sender = sender
        self.receiver = receiver
        self.content = content
 
# ==========================================================
# TASK
# ==========================================================
 
class Task:
 
    def __init__(self, description):
 
        self.task_id = str(uuid.uuid4())
 
        self.description = description
 
        self.status = "submitted"
 
        self.artifacts = []
 
    def update_status(self, status):
 
        self.status = status
 
        print(f"[TASK] {self.task_id[:8]} -> {status}")
 
# ==========================================================
# MONITORING AGENT
# ==========================================================
 
class MonitoringAgent:
 
    def handle(self, task):
 
        print("\n[Monitoring Agent]")
 
        metrics = {
            "cpu": "98%",
            "memory": "72%",
            "traffic": "High Traffic Spike"
        }
 
        return metrics
 
# ==========================================================
# INFRASTRUCTURE AGENT
# ==========================================================
 
class InfrastructureAgent:
 
    def handle(self, task):
 
        print("\n[Infrastructure Agent]")
 
        health = {
            "server": "Healthy",
            "database": "Healthy",
            "instances": 2
        }
 
        return health
 
# ==========================================================
# SECURITY AGENT
# ==========================================================
 
class SecurityAgent:
 
    def handle(self, task):
 
        print("\n[Security Agent]")
 
        security = {
            "threats": "None",
            "ddos": "No",
            "intrusion": "No"
        }
 
        return security
 
# ==========================================================
# RESOLUTION AGENT
# ==========================================================
 
class ResolutionAgent:
 
    def handle(self, monitoring, infra, security):
 
        print("\n[Resolution Agent]")
 
        if monitoring["cpu"] == "98%":
 
            return {
                "root_cause": "Traffic Spike",
                "resolution": "Scale instances from 2 to 5",
                "status": "Resolved"
            }
 
        return {
            "root_cause": "Unknown",
            "resolution": "Manual Investigation",
            "status": "Pending"
        }
 
# ==========================================================
# PLANNER AGENT
# ==========================================================
 
class PlannerAgent:
 
    def __init__(self):
 
        self.monitor = MonitoringAgent()
 
        self.infra = InfrastructureAgent()
 
        self.security = SecurityAgent()
 
        self.resolution = ResolutionAgent()
 
    def execute(self, task):
 
        task.update_status("working")
 
        monitor_result = self.monitor.handle(task)
 
        infra_result = self.infra.handle(task)
 
        security_result = self.security.handle(task)
 
        resolution_result = self.resolution.handle(
            monitor_result,
            infra_result,
            security_result
        )
 
        task.artifacts.extend([
            "metrics.json",
            "infra_report.json",
            "security_report.json"
        ])
 
        task.update_status("completed")
 
        report = {
 
            "incident": task.description,
 
            "monitoring": monitor_result,
 
            "infrastructure": infra_result,
 
            "security": security_result,
 
            "resolution": resolution_result,
 
            "artifacts": task.artifacts,
 
            "generated_at": str(datetime.now())
        }
 
        return report
 
# ==========================================================
# MAIN
# ==========================================================
 
registry = AgentRegistry()
 
registry.register(
    AgentCard(
        "MonitoringAgent",
        ["metrics", "cpu", "memory"]
    )
)
 
registry.register(
    AgentCard(
        "InfrastructureAgent",
        ["server", "database"]
    )
)
 
registry.register(
    AgentCard(
        "SecurityAgent",
        ["threat", "attack"]
    )
)
 
registry.register(
    AgentCard(
        "ResolutionAgent",
        ["analysis", "resolution"]
    )
)
 
registry.list_agents()
 
print("\n===================================")
print("INCIDENT MANAGEMENT SYSTEM")
print("===================================")
 
incident = input("\nEnter Incident: ")
 
task = Task(incident)
 
planner = PlannerAgent()
 
final_report = planner.execute(task)
 
print("\n===================================")
print("FINAL INCIDENT REPORT")
print("===================================")
 
print(
    json.dumps(
        final_report,
        indent=4
    )
)