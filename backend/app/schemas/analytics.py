from pydantic import BaseModel


class FieldStats(BaseModel):
    direction: str
    people_count: int
    avg_progress: float
    field_name: str 


class DepartmentAnalytics(BaseModel):
    department_id: int
    department_name: str
    people_count: int
    avg_progress: float
    by_direction: list[FieldStats] = []


class ConfirmedSkillItem(BaseModel):
    skill_id: int
    skill_name: str
    confirmed_at: str


class OverdueItem(BaseModel):
    skill_id: int
    skill_name: str
    planned_date: str
    days_overdue: int


class UserProgress(BaseModel):
    user_id: int
    full_name: str
    total_items: int
    done_items: int
    overdue_items: int
    progress_percent: float
    confirmed_skills: list[ConfirmedSkillItem] = []
    overdue_details: list[OverdueItem] = []


class UserAnalytics(BaseModel):
    user_id: int
    full_name: str
    total_items: int
    done_items: int
    overdue_items: int
    progress_percent: float
    confirmed_skills: list[ConfirmedSkillItem] = []
    overdue_details: list[OverdueItem] = []
    meetings_history: list[dict] = []