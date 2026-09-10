from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class MeetingSkillCreate(BaseModel):
    skill_id: int
    confirmed: bool = False


class MeetingSkillOut(BaseModel):
    id: int
    skill_id: int
    skill_name: Optional[str] = None
    confirmed: bool

    class Config:
        from_attributes = True


class MeetingCreate(BaseModel):
    user_id: int
    manager_id: int
    date: date
    summary: str = ""


class MeetingUpdate(BaseModel):
    meeting_date: Optional[date] = None
    summary: Optional[str] = None


class MeetingOut(BaseModel):
    id: int
    user_id: int
    manager_id: int
    date: date
    summary: str
    created_at: Optional[datetime] = None
    skills: list[MeetingSkillOut] = []

    class Config:
        from_attributes = True


class MeetingShort(BaseModel):
    id: int
    user_id: int
    manager_id: int
    date: date
    summary: str

    class Config:
        from_attributes = True