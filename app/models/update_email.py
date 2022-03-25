from pydantic import BaseModel
class Update_Email(BaseModel):
    id: str
    username: str
    newemail: str