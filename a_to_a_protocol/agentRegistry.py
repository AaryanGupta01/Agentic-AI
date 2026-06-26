# This file tells how to register agents and discover them based on their skills.
# It defines the Skill and AgentCard classes, as well as the AgentRegistry class 
# that manages the registration and discovery of agents. 
# The code demonstrates registering two agents with different skills 
# and searching for an agent with a specific skill tag.
from pydantic import BaseModel
from typing import List
 
print("Program Started")
 
class Skill(BaseModel):
    id: str
    description: str
    tags: List[str]
 
class AgentCard(BaseModel):
    name: str
    endpoint: str
    skills: List[Skill]
 
class AgentRegistry:
 
    def __init__(self):
        self.agents = []
 
    def register(self, agent):
        self.agents.append(agent)
 
    def discover(self, tag):
 
        matches = []
 
        for agent in self.agents:
            for skill in agent.skills:
                if tag in skill.tags:
                    matches.append(agent.name)
 
        return matches
 
infra = AgentCard(
    name="InfrastructureAgent",
    endpoint="http://localhost:8001",
    skills=[
        Skill(
            id="docker",
            description="Docker Operations",
            tags=["docker", "container"]
        )
    ]
)
 
cloud = AgentCard(
    name="CloudAgent",
    endpoint="http://localhost:8002",
    skills=[
        Skill(
            id="aws",
            description="AWS Operations",
            tags=["aws", "cloud"]
        )
    ]
)
 
registry = AgentRegistry()
 
registry.register(infra)
registry.register(cloud)
 
print("\nRegistered Agents")
 
for agent in registry.agents:
    print("-", agent.name)
 
print("\nSearching for 'cloud' skill")
 
result = registry.discover("cloud")
 
print("Found:", result)