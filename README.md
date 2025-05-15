#  Сервис аутентификации и авторизации

##  Описание

Микросервис на FastAPI для регистрации пользователей, входа в систему и безопасного управления JWT-токенами.

Архитектура реализована по принципу BFF (Backend For Frontend): `refresh_token` хранится в **HttpOnly cookie**, а `access_token` возвращается клиенту для использования в заголовках.

---

##  Используемые технологии

- FastAPI — высокопроизводительный Python web-фреймворк
- JWT (JSON Web Tokens) — для авторизации и управления сессиями
- OAuth2 + Password flow — встроенная поддержка авторизации
- HttpOnly cookies — безопасное хранение `refresh_token`
- bcrypt (passlib) — хеширование паролей
- SQLAlchemy + AsyncSession — взаимодействие с БД
- Alembic — миграции схемы базы данных

---

## Доступные эндпоинты

| Метод | Путь               | Назначение                                      |
|-------|--------------------|--------------------------------------------------|
| POST  | `/register`        | Регистрация нового пользователя                 |
| POST  | `/login`           | Аутентификация и получение `access_token`       |
| POST  | `/refresh-token`   | Обновление `access_token` по `refresh_token`    |
| POST  | `/logout`          | Выход из системы (удаление `refresh_token`)     |
| GET   | `/users/me`        | Получение текущего авторизованного пользователя |

---

## Хранение пользователей

- Пользователи сохраняются в базе данных (PostgreSQL)
- Все пароли хранятся в виде хэшей (`bcrypt`)
- Миграции управляются через `Alembic`

---

##  Настройки

Используется `.env` файл с переменными:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

```
___
# Безопасность

- access_token выдаётся клиенту и используется в заголовках Authorization

- refresh_token хранится в HttpOnly, Secure, SameSite=Strict cookie

- Защита от XSS: токены недоступны из JavaScript

- Защита от CSRF за счёт строгой политики cookie

___

# Установка и запуск

```
git clone https://github.com/your-username/fastapi-auth-service.git
cd fastapi-auth-service

python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows

pip install -r requirements.txt

alembic upgrade head  # применить миграции

uvicorn app.main:app --reload

```

#TODO

- Интеграция с внешними OIDC-провайдерами (Google, GitHub)

- Поддержка ролей (admin/user)

- Black/flake8/ruff интеграция для линтинга

