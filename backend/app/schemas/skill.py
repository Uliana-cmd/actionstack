from pydantic import BaseModel
from typing import Optional


class SkillBase(BaseModel):
    name: str
    direction: str


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    direction: Optional[str] = None


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True