from pydantic import BaseModel
from datetime import date


class VesselDataSchema(BaseModel):
    id: str
    name: str
    group: str
    date: date
    value: int

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True