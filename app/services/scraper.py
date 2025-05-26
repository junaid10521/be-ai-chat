from datetime import datetime
from bson import ObjectId
from app.db.collections import webpages_collection, scrapping_requests_collection
from app.utils.helpers import normalize_url

def handle_scraper_queue(agent_id, request_data):
    level = request_data["level"]
    websites = list(set(request_data["websites"]))
    has_specific_urls = request_data["has_specific_urls"]

    for website_url in websites:
        website_url = normalize_url(website_url)
        req_data = {
            "agent_id": ObjectId(agent_id),
            "base_url": website_url,
            "url": website_url,
            "status": "pending",
            "level": 0,
            "retries": 0,
            "sitemap": False,
            "request_id": str(ObjectId()),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        if has_specific_urls:
            req_data["level"] = level
        else:
            req_data["level"] = 2
            req_data["sitemap"] = True

        webpages_collection.insert_one(req_data)

        query = {
            "agent_id": req_data["agent_id"],
            "url": req_data["url"],
            "level": req_data["level"],
            "sitemap": req_data["sitemap"],
        }

        scrapping_req_data = {
            key: req_data[key]
            for key in req_data
            if key not in {"status", "retries", "base_url"}
        }

        existing_entry = scrapping_requests_collection.find_one(query)
        if existing_entry:
            scrapping_requests_collection.update_one(
                {"_id": existing_entry["_id"]},
                {
                    "$inc": {"attempts": 1},
                    "$set": {
                        "request_id": req_data["request_id"],
                        "updated_at": datetime.now(),
                    },
                },
            )
        else:
            scrapping_req_data["attempts"] = 1
            scrapping_requests_collection.insert_one(scrapping_req_data)
