from pydantic import BaseModel

class UserQuery(BaseModel):
    query: str
    
class ResearchQuery(BaseModel):
    queries: list[str]
