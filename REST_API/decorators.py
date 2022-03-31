from functools import wraps

from REST_API.utils.tokens import Token
# def auth(func):
#     def wrapper(obj, request, *args, **kwargs):
#         data = request.data
#         try:
#             user = Token.objects.get(hard_token=data.get('hard_token'), created__gte=(time.time() - 43200)).user
#
#         except:
#             return Response({'error': 'token has expired'}, status=401)
#         else:
#             request.user = user
#         response = func(obj, request, *args, **kwargs)
#         return response
#
#     return wrapper
from REST_API.utils.users import User

"""
  @staticmethod
    async def get_user_by_token(hard_token: str):
        Возвращает информацию о владельце указанного токена
        query = token_table.join(users_table).select().where(
            and_(
                token_table.c.hard_token == hard_token,  # тут надо уточнить хард или софт ..
                # token_table.c.expires > datetime.now()
            )
        )
        return await database.fetch_one(query)
"""


def auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        data = dict(args[0])    # *  ('hard_token', 'hard??1648728241.4256487') ('pet_type', 'rabbit') ('pet_id', 10)
        print(data)
        if not await User.get_user_by_token(data['hard_token']):      # without await!
            return {'error': 'token has expired'}
        return await func(*args, **kwargs)

    return wrapper


# def auth(func):
#     def wrapper(**kwargs):
#         try:
#             print(user)
#         except:
#
#         response = func(**kwargs)
#         return response
#
#     return wrapper
