from os import environ
import databases
from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

# Конфигурация базы данных
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "q1w2e3")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = "test"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()  # it is used to create classes models!
app = FastAPI()


@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()



from REST_API.routers import users , entities

app.include_router(users.router)
app.include_router(entities.router)
