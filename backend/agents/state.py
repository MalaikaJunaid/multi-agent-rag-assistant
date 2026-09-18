from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    query: str
    retrieved_documents: List[str]
    synthesis: str
    is_factually_correct: bool
    