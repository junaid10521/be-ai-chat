from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from app.db.collections import webpages_collection
from bson import ObjectId
from datetime import datetime
from app.utils.responses import response_success_handler, response_error_handler

router = APIRouter(prefix="/webpages/{agent_id}", tags=["Webpages Queue"])


@router.get("/")
async def webpages_queue(agent_id: str):
    try:
        records = webpages_collection.find(
            {
                "agent_id": ObjectId(agent_id),
            }
        )

        results = []

        for record in records:
            record["_id"] = str(record["_id"])
            record["agent_id"] = str(record["agent_id"])
            record["created_at"] = record["created_at"].isoformat()
            record["updated_at"] = record["updated_at"].isoformat()
            results.append(record)

        # Check if all records have status "done"
        if all(record["status"] == "done" for record in results):
            # Perform bulk delete operation if all records are "done"
            delete_result = webpages_collection.delete_many(
                {"agent_id": ObjectId(agent_id)}
            )

            print(f"Deleted {delete_result.deleted_count} records.")

        return response_success_handler("Success", results)
    except Exception as e:
        print(f"Error fetching records: {str(e)}")
        return response_error_handler(500, f"Error fetching records: {str(e)}")
