import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.agents.state import AgentState

def fact_check_node(state: AgentState) -> dict:
    """
    Evaluates if the synthesized answer is factually supported by the retrieved documents.
    """
    retrieved_documents = state.get("retrieved_documents", [])
    synthesis = state.get("synthesis", "")
    
    context = "\n\n".join(retrieved_documents)
    
    # We explicitly instruct the model to output a single word to avoid JSON parsing errors
    system_prompt = """You are a strict legal fact-checker. 
    You must evaluate whether the provided Answer is completely supported by the provided Context.
    
    If the Answer is supported, respond with ONLY the word TRUE.
    If the Answer contains any hallucinations, assumptions, or contradictions, respond with ONLY the word FALSE.
    Do not add any other text, warnings, or explanations.
    
    Context:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Answer to check:\n{synthesis}")
    ])
    
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        model="openrouter/free", 
        temperature=0
    )
    
    chain = prompt | llm
    
    # Execute the chain and get the raw string content
    result = chain.invoke({
        "context": context,
        "synthesis": synthesis
    })
    
    # Clean the response text and check if it contains our target keyword
    response_text = result.content.strip().upper()
    is_correct = "TRUE" in response_text
    
    return {"is_factually_correct": is_correct}