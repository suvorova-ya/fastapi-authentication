import json
from pathlib import Path

from app.dependencies.password import pwd_context

# Пример пользователей: username, пароль и активность
raw_users = [
    {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "test123",
        "disabled": False
    },
    {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "password": "secret",
        "disabled": True
    },
]


def create_user_db(users: list[dict]) -> dict:
    db = {}
    for user in users:
        hashed_password = pwd_context.hash(user["password"])
        db[user["username"]] = {
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "hashed_password": hashed_password,
            "disabled": user["disabled"]
        }
    return db


if __name__ == "__main__":
    db = create_user_db(raw_users)
    # Сохраняем в JSON
    Path("app/core/fake_users.json").write_text(json.dumps(db, indent=2))
    print("✅ fake_users.json сгенерирован!")
