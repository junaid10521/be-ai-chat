from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_scraper import router as scraper_router
from app.api.routes_agents import router as agent_router
from app.api.routes_webpages import router as webpages_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the scraping-related APIs
app.include_router(scraper_router, prefix="/api/scraper")
app.include_router(agent_router, prefix="/api/agents", tags=["Agents"])
app.include_router(webpages_routes, prefix="/api/webpages-queue")
