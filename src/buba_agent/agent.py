from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware
from .tools import *
from langgraph.types import Command
import os
from dotenv import load_dotenv
load_dotenv()

from buba_agent.prompt import SYSTEM_PROMPT

memory_saver = InMemorySaver() # checkpointer to save the agent's memory, can be used to maintain context across multiple interactions
config = {"configurable": {"thread_id": "user-session-123"}} # configurable thread_id for the agent's session, can be used to maintain context across multiple interactions

llm = init_chat_model(
    "openrouter:deepseek/deepseek-v4-flash-0731",
    api_key=os.getenv("DEEPSEEK-V4"),
    temperature=0,
    max_tokens=2048,
)

tools = [

    # Actions that require HITL
    send_email,
    get_current_datetime,
    schedule_event,

    # Read-only tools
    search_emails,
    find_contact,
    get_contacts,
    get_calendar_events,
    search_web,
]

agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    tools=tools,
    checkpointer=memory_saver
)

def chat_agent(user_input: str, thread_id: str):
    """
    Start a new agent interaction.

    The thread_id identifies the conversation/checkpoint
    that this request belongs to.
    """

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    human_message = HumanMessage(
        content=user_input
    )

    result = agent.invoke(
        {
            "messages": [human_message]
        },
        config=config,
    )

    return result

def resume_agent(thread_id: str, decision: str):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = agent.invoke(
        Command(resume=decision),
        config=config,
    )

    return result