from pydantic import BaseModel
from typing import Optional


class DepartmentBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    head_user_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    head_user_id: Optional[int] = None


class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class DepartmentTree(BaseModel):
    id: int
    name: str
    head_user_id: Optional[int] = None
    children: list["DepartmentTree"] = []

    class Config:
        from_attributes = True


DepartmentTree.model_rebuild()
