from datetime import date
from pydantic import BaseModel, ConfigDict

class PlanBase(BaseModel):
    title: str
    description: str | None = None
    start_date: date

class PlanCreate(PlanBase):
    pass

class PlanRead(PlanBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)