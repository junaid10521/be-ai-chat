from fastapi import APIRouter
from app.db.collections import agents_collection  # ✅ correct import
from app.models.agents import AgentCreateRequest  # Your Pydantic model
from app.utils.responses import response_success_handler, response_error_handler  # Assuming these exist

router = APIRouter()


@router.post("/")
def create_agent(req_data: AgentCreateRequest):
    try:
        # Only use the `title` field
        agent_data = {"title": req_data.title}

        inserted_id = agents_collection.insert_one(agent_data).inserted_id
        return response_success_handler("Agent created", {"id": str(inserted_id)})

    except Exception as e:
        return response_error_handler(500, f"Failed to create agent: {str(e)}")
