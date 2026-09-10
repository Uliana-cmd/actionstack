from pydantic import BaseModel
from typing import Optional


class DepartmentBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    manager_id: int


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    manager_id: Optional[int] = None


class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class DepartmentTree(BaseModel):
    id: int
    name: str
    manager_id: int
    children: list["DepartmentTree"] = []

    class Config:
        from_attributes = True


DepartmentTree.model_rebuild()
