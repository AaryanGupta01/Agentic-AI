from typing import TypedDict
from langgraph.graph import StateGraph

#=====================================================
# STEP 1: Define the State
#=====================================================

class AgentState(TypedDict):
    name: str  # Input: who is being greeted
    greeting: str  # Output: filled in by the node below

#=====================================================
# STEP 2: Define a Node (a function that does work)
#=====================================================

def generate_greeting(state: AgentState) -> AgentState:
    """
    Node: Greeting Generator
    Reads 'name' from state, writes a greeting back.
    """
    name = state["name"]
    state["greeting"] = f"Welcome {name} to LangGraph Training!"
    return state

# Every Node must return the state, even if it doesn't modify it.
# AgentState is a TypedDict, so we can modify it in place and return it.
# TypedDicts are mutable dictionaries, so we can add new keys as needed.

#=====================================================
# STEP 3: Build the Graph
#=====================================================

builder = StateGraph(AgentState)

# Register the node - give it a name and a function
builder.add_node("greet", generate_greeting)

# Entry point = where execution starts
builder.set_entry_point("greet")

# Finish point = where execution ends
builder.set_finish_point("greet")

# Compile = lock in the graph structure, ready to run
graph = builder.compile()
# compile is a method that finalizes the graph structure.
# After this, you cannot add more nodes or change the graph.
#  It prepares the graph for execution.

#=====================================================
# STEP 4: Run the Graph
#=====================================================

if __name__ == "__main__":
    result = graph.invoke({"name": "Shyni"})
    print(result["greeting"])

    for name in ["Alice", "Bob", "VIT Student"]:
        output = graph.invoke({"name": name})
        print(output["greeting"])



