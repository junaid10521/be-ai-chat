from fastapi import APIRouter
from bson import ObjectId
from datetime import datetime
import asyncio

from app.models.schemas import AgentWebsiteCreateRequest
from app.services.tasks import process_webpages, shutdown_event
from app.services import scraper
from app.utils.responses import response_success_handler, response_error_handler
from app.db.collections import webpages_collection

router = APIRouter()
background_task = None

@router.post("/websites/")
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


@router.get("/")
async def webpages_queue(agent_id: str):
    try:
        records = webpages_collection.find({"agent_id": ObjectId(agent_id)})

        results = []
        for record in records:
            record["_id"] = str(record["_id"])
            record["agent_id"] = str(record["agent_id"])
            record["created_at"] = record["created_at"].isoformat()
            record["updated_at"] = record["updated_at"].isoformat()
            results.append(record)

        if all(record["status"] == "done" for record in results):
            delete_result = webpages_collection.delete_many({"agent_id": ObjectId(agent_id)})
            print(f"Deleted {delete_result.deleted_count} records.")

        return response_success_handler("Success", results)
    except Exception as e:
        return response_error_handler(500, f"Error fetching records: {str(e)}")
