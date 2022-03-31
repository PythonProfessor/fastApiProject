from pydantic import BaseModel, EmailStr

"""
Этот модуль используется для создания, валидации схем и для дальнейшего взаимодействия с REST API
"""


# тут можно создавать Response and Creation models


class UserCreate(BaseModel):
    """ Проверяет login запрос """
    # email: EmailStr
    username: str
    password: str


class UserCreateResponse(BaseModel):
    """ Проверяет sign-up запрос """
    # email: EmailStr
    username: str
    # hashed_password: str
    hard_token: str
    soft_token: str


class UserLogin(BaseModel):
    """Used for input login data"""
    username: str
    password: str


class UserSelectIsland(BaseModel):
    hard_token: str
    island_id: int
