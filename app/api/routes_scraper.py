from fastapi import APIRouter
from bson import ObjectId
from datetime import datetime
import asyncio
from app.models.schemas import AgentWebsiteCreateRequest
from app.services.tasks import process_webpages, shutdown_event
from app.services import scraper
from app.utils.responses import response_success_handler, response_error_handler
from app.db.collections import webpages_collection
from app.db.collections import agents_collection

router = APIRouter()
background_task = None

@router.post("/websites/{agent_id}/")
async def create_agent_websites(agent_id: str, req_data: AgentWebsiteCreateRequest):
    try:
        request_data = req_data.model_dump()

        if not request_data:
            return response_error_handler(400, "No data provided")

        scraper.handle_scraper_queue(agent_id, request_data)

        global background_task
        if not background_task or background_task.done():
            shutdown_event.clear()
            background_task = asyncio.create_task(process_webpages(shutdown_event))

        return response_success_handler("Scraping processing started successfully")
    except Exception as e:
        return response_error_handler(500, f"Error starting background task: {str(e)}")


@router.get("/websites/{agent_id}/")
async def webpages_queue(agent_id: str):
    try:
        # ✅ Use PyMongo without `await`
        agent = agents_collection.find_one({"_id": ObjectId(agent_id)})
        agent_name = agent.get("title", "") if agent else ""

        records = webpages_collection.find({"agent_id": ObjectId(agent_id)})

        results = []
        for record in records:
            record["_id"] = str(record["_id"])
            record["agent_id"] = str(record["agent_id"])
            record["created_at"] = record["created_at"].isoformat()
            record["updated_at"] = record["updated_at"].isoformat()
            record["agent_name"] = agent_name  # ✅ Inject agent name
            results.append(record)

        return response_success_handler("Success", results)

    except Exception as e:
        return response_error_handler(500, f"Error fetching records: {str(e)}")

