from fastapi import APIRouter, HTTPException
from REST_API.schemas import users
from REST_API.views import users as users_views
from REST_API.utils import users as users_utils

"""
Этот модуль используется для настройки end пойнтов Юзера и обрабатываем конечные запросы взаимодействуя с БД
"""

router = APIRouter()


@router.post("/register", response_model=users.UserCreateResponse)
async def create_user(user: users.UserCreate):
    """
    The handling of the register route
    :param user: value for creation of the user
    :return: the user view
    """
    db_user = await users_utils.User.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    return await users_views.create_user(user=user)


@router.post('/login', response_model=users.UserCreateResponse)
async def user_login(user: users.UserLogin):
    """
    The handling of the login route
    :param user: values for creation of the user
    :return: the user view
    """
    return await users_views.login(user=user)


@router.post('/select_island')
async def select_island(model: users.UserSelectIsland):
    return await users_views.select_island(model=model)
