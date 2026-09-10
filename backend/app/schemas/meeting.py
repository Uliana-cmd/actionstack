from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class MeetingSkillCreate(BaseModel):
    skill_id: int
    is_defended: bool = False
    mark: int = 0
    problems_comm: Optional[str] = None


class MeetingSkillOut(BaseModel):
    id: int
    skill_id: int
    skill_name: Optional[str] = None
    mark: int
    problems_comm: Optional[str] = None
    is_defended: bool

    class Config:
        from_attributes = True


class MeetingCreate(BaseModel):
    user_id: int
    inspector_id: int
    meeting_date: datetime
    totals: str = ""


class MeetingUpdate(BaseModel):
    meeting_date: Optional[datetime] = None
    totals: Optional[str] = None


class MeetingOut(BaseModel):
    id: int
    user_id: int
    inspector_id: int
    meeting_date: datetime
    totals: str
    skills: list[MeetingSkillOut] = []

    class Config:
        from_attributes = True


class MeetingShort(BaseModel):
    id: int
    user_id: int
    inspector_id: int
    meeting_date: datetime
    totals: str

    class Config:
        from_attributes = True