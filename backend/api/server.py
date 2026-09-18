import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from langgraph.errors import GraphRecursionError

# Ensure the backend module is discoverable
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.main import app as graph_app
from backend.api.schemas import ChatRequest, ChatResponse

# Initialize FastAPI
app = FastAPI(
    title="UAE Legal Assistant API",
    description="A REST API serving a Multi-Agent RAG Pipeline for UAE Law",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """Simple endpoint to verify the API is running."""
    return {"status": "healthy", "service": "UAE Legal RAG Pipeline"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Executes the multi-agent graph (Retrieve -> Synthesize -> Fact-Check) 
    based on the user's query and returns a validated JSON response.
    """
    initial_state = {
        "query": request.query,
        "messages": [],
        "retrieved_documents": [],
        "synthesis": "",
        "is_factually_correct": False
    }
    
    try:
        # Cap execution to prevent infinite loops from the Fact-Checker
        final_state = graph_app.invoke(initial_state, config={"recursion_limit": 5})
        
        return ChatResponse(
            answer=final_state["synthesis"],
            sources=final_state.get("retrieved_documents", [])
        )
        
    except GraphRecursionError:
        return ChatResponse(
            answer="⚠️ Verification Failed: The AI models could not synthesize a strictly verified answer within the retry limit.",
            sources=[],
            error="RecursionLimitExceeded"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))