from fastapi import FastAPI
from src.buba_agent.agent import chat_agent, resume_agent
from fastapi.middleware.cors import CORSMiddleware

from src.buba_agent.schemas import (
    ChatRequest,
    ApprovalRequest,
)


app = FastAPI(
    title="Buba Agent API",
    description="Personal AI Agent API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HOME

@app.get("/")
async def home():

    return {
        "message": "Agent API is running"
    }


# HEALTH CHECK
@app.get("/health")
async def health():

    return {
        "status": "ok"
    }


# CHAT
@app.post("/chat")
async def chat(request: ChatRequest):

    result = chat_agent(
        user_input=request.message,
        thread_id=request.thread_id
    )

    # Agent needs human approval
    if "__interrupt__" in result:

        interrupt = result["__interrupt__"][0]

        return {
            "status": "approval_required",
            "thread_id": request.thread_id,
            "approval": interrupt.value,
        }

    # Agent completed normally
    return {
        "status": "completed",
        "message": result["messages"][-1].content,
    }

# APPROVE / REJECT
@app.post("/approval")
async def approval(request: ApprovalRequest):

    result = resume_agent(
        thread_id=request.thread_id,
        decision=request.decision,
    )

    # AGENT NEEDS ANOTHER APPROVAL
    if "__interrupt__" in result:

        interrupt = result["__interrupt__"][0]

        return {
            "status": "approval_required",
            "thread_id": request.thread_id,
            "approval": interrupt.value,
        }

    # AGENT FINISHED
    return {
        "status": "completed",
        "message": result["messages"][-1].content,
    }