from fastapi import APIRouter
from app.db.collections import agents_collection
from app.models.agents import AgentCreateRequest
from app.utils.responses import response_success_handler, response_error_handler

from bson import ObjectId

router = APIRouter()


@router.post("/")
def create_agent(req_data: AgentCreateRequest):
    try:
        agent_data = {"title": req_data.title}
        inserted_id = agents_collection.insert_one(agent_data).inserted_id
        return response_success_handler("Agent created", {"id": str(inserted_id)})
    except Exception as e:
        return response_error_handler(500, f"Failed to create agent: {str(e)}")


@router.get("/")
def get_all_agents():
    try:
        agents = list(agents_collection.find({}, {"title": 1}))
        formatted_agents = [
            {"id": str(agent["_id"]), "title": agent["title"]}
            for agent in agents
        ]
        return response_success_handler("Agents fetched", formatted_agents)
    except Exception as e:
        return response_error_handler(500, f"Failed to fetch agents: {str(e)}")


@router.delete("/{agent_id}")
def delete_agent(agent_id: str):
    try:
        result = agents_collection.delete_one({"_id": ObjectId(agent_id)})
        if result.deleted_count == 0:
            return response_error_handler(404, "Agent not found")
        return response_success_handler("Agent deleted", {"id": agent_id})
    except Exception as e:
        return response_error_handler(500, f"Failed to delete agent: {str(e)}")
