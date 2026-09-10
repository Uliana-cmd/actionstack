#!/bin/bash
set -e

# Путь к файлу-маркеру, который создается после успешной инициализации
FLAG_FILE="/app/data/.db_initialized"

# Экспортируем пароль, чтобы утилиты psql и pg_isready не запрашивали его в консоли
export PGPASSWORD="$DB_PASSWORD"

echo "=== Проверка доступности локального PostgreSQL ==="
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "PostgreSQL еще не готов, ожидание 2 секунды..."
  sleep 2
done

# Проверяем, выполнялась ли инициализация ранее
if [ ! -f "$FLAG_FILE" ]; then
  echo "=== Первый запуск: Инициализация базы данных ==="

  # 1. Проверяем, существует ли база данных. Если нет — создаем.
  # Подключаемся к системной базе 'postgres', так как она точно есть.
  DB_EXISTS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

  if [ "$DB_EXISTS" != "1" ]; then
    echo "Создание базы данных $DB_NAME..."
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"
  else
    echo "База данных $DB_NAME уже существует в Postgres."
  fi

  # 2. Накатываем структуру из template.sql в созданную БД
  echo "Развертывание шаблона template.sql в базу $DB_NAME..."
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f /app/models/action_stack.sql

  # 3. Создаем файл-маркер, чтобы в следующий раз пропустить этот блок
  mkdir -p /app/data
  touch "$FLAG_FILE"
  echo "=== Инициализация успешно завершена! ==="
else
  echo "=== База данных уже была инициализирована ранее. Пропуск настройки. ==="
fi

# Передаем управление основному приложению (запуск сервера)
echo "=== Запуск основного приложения ==="
exec "$@"
