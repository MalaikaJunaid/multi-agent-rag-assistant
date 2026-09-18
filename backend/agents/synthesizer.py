import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.agents.state import AgentState

def synthesize_node(state: AgentState) -> dict:
    """
    Synthesizes an answer using the retrieved documents and the user's query.
    """
    query = state["query"]
    retrieved_documents = state.get("retrieved_documents", [])
    
    # Format the retrieved documents into a single readable string for the LLM
    context = "\n\n".join(retrieved_documents)
    
    # Define the system prompt restricting the AI to the provided context
    system_prompt = """You are a specialized UAE Legal Assistant.
    Answer the user's question based strictly on the following retrieved legal context.
    If the context does not contain the answer, explicitly state that you cannot answer based on the provided documents.
    
    Context:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])
    
    # Initialize the LLM with OpenRouter
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        model="openrouter/free", # This acts as a permanent fail-safe
        temperature=0
    )
    
    # Chain the prompt and the LLM together
    chain = prompt | llm
    
    # Execute the chain
    response = chain.invoke({
        "context": context,
        "query": query
    })
    
    # LangGraph automatically updates the 'synthesis' key in the global AgentState
    return {"synthesis": response.content}