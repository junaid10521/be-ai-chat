import asyncio
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from bson import ObjectId

from app.db.collections import webpages_collection
from app.utils.helpers import normalize_url

shutdown_event = asyncio.Event()

async def process_webpages(shutdown_event):
    while not shutdown_event.is_set():
        # Find the next pending webpage to scrape
        record = webpages_collection.find_one_and_update(
            {"status": "pending"},
            {"$set": {"status": "processing", "updated_at": datetime.now()}},
        )

        if not record:
            await asyncio.sleep(5)  # No pending task found, wait and try again
            continue

        try:
            url = record["url"]
            print(f"[Scraper] Processing URL: {url}")

            # Perform scraping
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "lxml")

            title = soup.title.string.strip() if soup.title else "No title found"
            text = soup.get_text(separator=' ', strip=True)[:1000]  # first 1000 chars

            print(f"[Scraper] Title: {title}")

            # Update result
            webpages_collection.update_one(
                {"_id": record["_id"]},
                {
                    "$set": {
                        "status": "done",
                        "scraped_title": title,
                        "scraped_snippet": text,
                        "updated_at": datetime.now(),
                    }
                },
            )

        except Exception as e:
            print(f"[Scraper] Error scraping {record['url']}: {e}")
            webpages_collection.update_one(
                {"_id": record["_id"]},
                {
                    "$set": {
                        "status": "error",
                        "error_message": str(e),
                        "updated_at": datetime.now(),
                    },
                    "$inc": {"retries": 1},
                },
            )

        await asyncio.sleep(1)  # small delay between tasks
