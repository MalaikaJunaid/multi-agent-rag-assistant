import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from backend.agents.state import AgentState

# CHANGED: Match the new index name we used in ingestion
INDEX_NAME = "uae-legal-assistant-free"

def retrieve_node(state: AgentState) -> dict:
    """
    Retrieves relevant documents from Pinecone based on the user's query.
    """
    query = state["query"]
    
    # CHANGED: Use the same free local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME, 
        embedding=embeddings
    )
    
    docs = vectorstore.similarity_search(query, k=3)
    retrieved_content = [doc.page_content for doc in docs]
    
    return {"retrieved_documents": retrieved_content}