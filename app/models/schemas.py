from typing import List
from pydantic import BaseModel

class AgentWebsiteCreateRequest(BaseModel):
    websites: List[str]
    level: int
    has_specific_urls: bool
