from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI


load_dotenv()
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "docx_template_converter").lower()
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL, pool_size=10, max_overflow=20, pool_timeout=5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Эта функция запускается ОДИН раз при старте FastAPI сервера.
    Здесь мы можем сделать первоначальные проверки или логирование.
    """
    print("=== [FastAPI] Сервер запускается, пул соединений готов. ===")

    # Слово yield — это разделитель:
    yield

    # Всё, что после yield, выполнится СТРОГО при выключении сервера
    print("=== [FastAPI] Сервер останавливается, закрываем ресурсы... ===")