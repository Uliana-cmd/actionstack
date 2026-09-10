FROM python:3.12

# Устанавливаем системный клиент postgres-client ради утилиты psql
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/* \
    && useradd -u 8888 -m appuser \
    && mkdir -p /app \
    && chown -R appuser:appuser /app

WORKDIR /app

# ставим библиотеки языка
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY --chown=appuser:appuser . .

USER appuser