# app/crud/user.py
from sqlalchemy.orm import Session
from app.schemas.user import UserRead

def get(db: Session, user_id: int):
    # Пишем сырой SQL-запрос с точным указанием колонок из вашей БД
    query = """
        SELECT id, login, email, department_id, created_at, is_hired, field_id 
        FROM public.users 
        WHERE id = :id
    """
    result = db.execute(query, {"id": user_id}).fetchone()
    
    if not result:
        return None
        
    # Превращаем результат Row в словарь (в зависимости от версии SQLAlchemy: result._asdict() или dict(result))
    user_dict = result._asdict() 
    
    # Возвращаем Pydantic-модель, чтобы в роутерах работал автокомплит и валидация
    return UserRead.model_validate(user_dict)

def authenticate(db: Session, login_from_form: str, password_raw: str):
    # Ищем пользователя по логину (так как в форме OAuth2 это поле называется username)
    query = """
        SELECT id, login, email, hash_password, department_id, created_at, is_hired, field_id 
        FROM public.users 
        WHERE login = :login
    """
    result = db.execute(query, {"login": login_from_form}).fetchone()
    
    if not result:
        return None
        
    user_dict = result._asdict()
    
    # Хэш пароля в БД имеет тип character(100), PostgreSQL может дополнить его пробелами. 
    # Безопаснее сделать .strip(), если используете библиотеку вроде passlib/bcrypt
    stored_hash = user_dict["hash_password"].strip()
    
    # Здесь должна быть ваша проверка пароля (например, pwd_context.verify)
    # Если проверка прошла успешно:
    return UserRead.model_validate(user_dict)
