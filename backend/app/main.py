from fastapi import FastAPI, File, Form, Header, Path, UploadFile, HTTPException, status, Request, Depends
from fastapi.responses import FileResponse
from app.database import lifespan, engine
from sqlalchemy import text
app = FastAPI(lifespan=lifespan)

@app.get("/templates")
async def get_status() -> str:
    with engine.connect() as conn:
        try:
            # Выполняем простейший проверочный запрос
            result = conn.execute(text("SELECT 1")).scalar()
            if result == 1:
                return "База данных доступна и работает отлично!"
        except Exception as e:
            return f"Ошибка подключения к БД: {e}"

        return "Сервис успешно подключён"