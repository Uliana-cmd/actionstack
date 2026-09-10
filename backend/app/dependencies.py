from datetime import datetime
from app.schemas.user import UserRead

def get(db_cursor, user_id: int):
    # Выбираем строго определенные поля, чтобы индексы всегда были фиксированными
    query = """
        SELECT id, login, email, department_id, created_at, is_hired, field_id 
        FROM public.users 
        WHERE id = %s;
    """
    db_cursor.execute(query, (user_id,))
    row = db_cursor.fetchone()
    
    if not row:
        return None
        
    # Сопоставляем индексы кортежа (0, 1, 2...) со свойствами Pydantic схемы
    return UserRead(
        id=row[0],
        login=row[1],
        email=row[2],
        department_id=row[3],
        created_at=row[4],
        is_hired=row[5],
        field_id=row[6]
    )

def authenticate(db_cursor, login_from_form: str, password_raw: str):
    # Ищем пользователя по логину
    query = """
        SELECT id, login, email, department_id, created_at, is_hired, field_id, hash_password 
        FROM public.users 
        WHERE login = %s;
    """
    db_cursor.execute(query, (login_from_form,))
    row = db_cursor.fetchone()
    
    if not row:
        return None
        
    # Извлекаем хэш пароля (он идет 7-м элементом, индекс 6)
    # .strip() обязателен, так как тип character(100) забивает остаток строки пробелами
    stored_hash = row[7].strip() if row[7] else ""
    
    # --- ТУТ ВАША ПРОВЕРКА ПАРОЛЯ ---
    # Например: if not verify_password(password_raw, stored_hash): return None
    
    # Если пароль подошел, собираем схему без хэша пароля
    return UserRead(
        id=row[0],
        login=row[1],
        email=row[2],
        department_id=row[3],
        created_at=row[4],
        is_hired=row[5],
        field_id=row[6]
    )
