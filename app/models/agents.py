from pydantic import BaseModel


class AgentCreateRequest(BaseModel):
    title: str
