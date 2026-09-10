FROM python:3.12

# Устанавливаем системный клиент postgres-client ради утилиты psql
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/* \
    && useradd -u 8888 -m appuser \
    && mkdir -p /app \
    && chown -R appuser:appuser /app

WORKDIR /app

# Шаг 1: Копируем только requirements.txt для кэширования слоев
COPY --chown=appuser:appuser backend/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Шаг 2: Создаем подпапку data (чтобы у appuser были на неё права)
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Шаг 3: Копируем локальную папку backend/app внутрь виртуальной папки /app/app
COPY --chown=appuser:appuser backend/app/ ./app

USER appuser
