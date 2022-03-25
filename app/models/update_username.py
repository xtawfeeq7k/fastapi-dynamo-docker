from pydantic import BaseModel
class Update_Username(BaseModel):
    id: str
    username: str
    newusername: str