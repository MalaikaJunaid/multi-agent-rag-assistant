from dotenv import load_dotenv
from pathlib import Path
from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState
from backend.agents.retriever import retrieve_node
from backend.agents.synthesizer import synthesize_node
from backend.agents.fact_checker import fact_check_node

# Load environment variables
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

# 1. Initialize the LangGraph State
workflow = StateGraph(AgentState)

# 2. Add the Nodes (our three agent files)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("synthesize", synthesize_node)
workflow.add_node("fact_check", fact_check_node)

# 3. Define the standard flow (Edges)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "synthesize")
workflow.add_edge("synthesize", "fact_check")

# 4. Define the routing logic for the Fact-Checker (Conditional Edge)
def check_hallucinations(state: AgentState) -> str:
    """Routes the graph based on the fact-checker's boolean result."""
    if state.get("is_factually_correct"):
        return "end"
    else:
        print("\n[!] Hallucination detected. Re-routing back to Synthesizer...")
        return "synthesize"

workflow.add_conditional_edges(
    "fact_check",
    check_hallucinations,
    {
        "end": END,
        "synthesize": "synthesize" # Loops back if it fails
    }
)

# 5. Compile the application
app = workflow.compile()

# --- Testing Script ---
if __name__ == "__main__":
    print("Initializing the UAE Legal Assistant Pipeline...\n")
    
    # Let's ask a specific question based on the UAE Labor Law
    test_query = "What is the maximum probation period for an employee under UAE law?"
    print(f"User Query: {test_query}\n")
    
    initial_state = {
        "query": test_query,
        "messages": [],
        "retrieved_documents": [],
        "synthesis": "",
        "is_factually_correct": False
    }
    
    # Run the graph and stream the output so we can see the steps happen
    for event in app.stream(initial_state):
        for node_name, node_state in event.items():
            print(f"--- Finished Node: {node_name} ---")
            
    # Fetch the final resulting state
    final_state = app.invoke(initial_state)
    
    print("\n================ FINAL ANSWER ================")
    print(final_state["synthesis"])
    print("==============================================")