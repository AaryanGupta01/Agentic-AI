from pydantic import BaseModel
from typing import List
import json
 
# ==========================================================
# SKILL MODEL
# ==========================================================
 
class Skill(BaseModel):
    id: str
    description: str
    tags: List[str]
 
# ==========================================================
# AGENT CARD MODEL
# ==========================================================
 
class AgentCard(BaseModel):
 
    name: str
    description: str
    version: str
    endpoint: str
    provider: str
    capabilities: List[str]
    skills: List[Skill]
 
# ==========================================================
# CREATE AGENT CARD
# ==========================================================
 
infra_agent = AgentCard(
    name="InfrastructureAgent",
 
    description="Handles server, cloud and deployment operations",
 
    version="1.0.0",
 
    endpoint="http://localhost:8001",
 
    provider="A2A Training Lab",
 
    capabilities=[
        "Task Execution",
        "Monitoring",
        "Artifact Generation"
    ],
 
    skills=[
 
        Skill(
            id="server_health",
            description="Checks server health",
            tags=[
                "server",
                "health",
                "monitoring"
            ]
        ),
 
        Skill(
            id="docker",
            description="Docker container management",
            tags=[
                "docker",
                "container",
                "deployment"
            ]
        ),
 
        Skill(
            id="autoscaling",
            description="Scale infrastructure resources",
            tags=[
                "cloud",
                "scaling",
                "aws"
            ]
        )
    ]
)
 
# ==========================================================
# DISPLAY CARD
# ==========================================================
 
print("\nAGENT CARD")
print("=" * 50)
 
print(
    infra_agent.model_dump_json(
        indent=4
    )
)