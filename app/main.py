from fastapi import FastAPI
from app.routers.routes import router

app = FastAPI(title="Auth_service",
              description="API для регистрации, входа пользователей и управления JWT-токенами.",
              version="1.0.0"
              )

app.include_router(router)

