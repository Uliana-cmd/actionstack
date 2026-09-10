# schemas/user.py
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr | None = None  # В БД может быть NULL
    login: str                     # Вместо username

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description='Пароль (минимум 8 символов)')
    department_id: int             # Обязательно для INSERT в БД
    field_id: int                  # Обязательно для INSERT в БД

class UserRead(UserBase):
    id: int
    is_hired: bool                 # Вместо is_active
    department_id: int
    field_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    login: str | None = None
    department_id: int | None = None
    field_id: int | None = None
