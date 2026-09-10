from pydantic import BaseModel
from typing import Optional


class SkillBase(BaseModel):
    name: str
    field_id: int


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    field_id: Optional[int] = None


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True