from pydantic import BaseModel, EmailStr, Field, SecretStr

class LoginRequest(BaseModel):
        email : EmailStr
        password: str = Field(
      ..., min_length=8, description='Пароль (минимум 8 символов)'
  )

class Token(BaseModel):
  access_token: str
  token_type: str = 'bearer'

class TokenPayload(BaseModel):
  sub: str | None = None
  exp: int | None = None