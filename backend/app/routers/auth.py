from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Token
from app.dependencies import get_db, get_current_user
from app.crud import user as user_crud
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email уже занят")
    return user_crud.create(db, data)


# routers/auth.py
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # В form.username прилетит то, что пользователь ввел в поле Login/Email на фронтенде
    user = user_crud.authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Так как user теперь — это валидный объект UserRead, мы можем спокойно писать user.id
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token, token_type="bearer")



@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)):
    return current_user