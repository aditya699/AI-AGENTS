from pydantic import BaseModel

class UserQuery(BaseModel):
    query: str
    
