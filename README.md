# HacathonMax

Бот для MAX, который помогает школьникам находить подходящие олимпиады и отслеживать важные этапы.

## Требования

Перед запуском необходимо установить:

- Python
- PostgreSQL
- Git

## 1. Клонирование проекта

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd HacathonMax
```

## 2. Виртуальное окружение

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 4. Создание PostgreSQL баз

Необходимо создать две базы данных:

```sql
CREATE DATABASE hackathon_max;
CREATE DATABASE hackathon_max_test;
```

Например, это можно сделать через pgAdmin или psql.

## 5. Настройка .env

Скопируйте файл:

```text
.env.example
```

в новый файл:

```text
.env
```

Заполните настройки:

```env
MAX_TOKEN=your_max_token_here

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/hackathon_max
TEST_DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/hackathon_max_test
```

`your_password` необходимо заменить на пароль локального пользователя PostgreSQL.

`MAX_TOKEN` — токен бота MAX.

Файл `.env` содержит секретные данные и не должен добавляться в Git.

## 6. Создание таблиц

Запустите миграции Alembic:

```bash
alembic upgrade head
```

## 7. Начальное заполнение БД

```bash
python -m scripts.setup_database
```

Команда:

- добавит необходимые предметы;
- загрузит олимпиады из `data/OlimpiadData.xlsx`;
- создаст связи олимпиад с предметами, классами и этапами.

Скрипт можно запускать повторно: существующие олимпиады обновляются по `external_id`.

## 8. Запуск бота

```bash
python -m app.main
```

## Тесты

Для запуска всех тестов:

```bash
pytest -v
```

## Обновление структуры БД

После изменения SQLAlchemy-моделей создать новую миграцию:

```bash
alembic revision --autogenerate -m "описание изменения"
```

Проверить созданную миграцию, затем применить:

```bash
alembic upgrade head
```

Проверить наличие несохранённых изменений схемы:

```bash
alembic check
```

## Быстрый запуск после первой настройки

При последующих запусках обычно достаточно:

```bash
.venv\Scripts\activate
python app.main
```