from fastapi import FastAPI
from app.api.routes_scraper import router as scraper_router
from app.api.routes_agents import router as agent_router
from app.api.routes_webpages import router as webpages_routes

app = FastAPI()

# Mount the scraping-related APIs
app.include_router(scraper_router, prefix="/scraper")
app.include_router(agent_router, prefix="/agents", tags=["Agents"])
app.include_router(webpages_routes, prefix="/webpages-queue")