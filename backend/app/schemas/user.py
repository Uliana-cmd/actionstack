from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
     password: str = Field(
          ..., min_length=8, description='Пароль (минимум 8 символов)'
      )

class UserRead(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None