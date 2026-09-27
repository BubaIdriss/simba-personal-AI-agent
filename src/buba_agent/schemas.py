from pydantic import BaseModel
from typing import Literal

class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ApprovalRequest(BaseModel):
    thread_id: str
    decision: Literal["approve", "reject"]