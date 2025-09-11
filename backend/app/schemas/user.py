from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    class Config:
        from_attributes = True
