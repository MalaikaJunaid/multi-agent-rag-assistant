from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's legal question.")

class ChatResponse(BaseModel):
    answer: str = Field(description="The synthesized and fact-checked answer.")
    sources: List[str] = Field(default_factory=list, description="The retrieved context chunks used.")
    error: Optional[str] = Field(default=None, description="Error message if the graph fails.")