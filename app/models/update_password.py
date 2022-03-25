from pydantic import BaseModel
class Update_Password(BaseModel):
    id: str
    username:str
    password: str