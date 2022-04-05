import asyncio
import logging

import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket

from REST_API.utils.users import User

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class Homepage(HTTPEndpoint):
    async def get(self, request):
        return HTMLResponse(html)

# class Echo(WebSocketEndpoint):
#     encoding = "text"
#
#     async def on_receive(self, websocket, data):
#         await websocket.send_text(f"Message text was: {data}")
#
#     async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
#         await websocket.send_text('CLOSED')
#         print("CLOSED")
#         return '<h1> Closed </h1>'


class WebSocketHandler(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

    # await websocket.send_text(f"Message text was: {data}")
    async def on_connect(self, websocket):
        #await websocket.accept()
        while True:
            logging.info("Connected")
            await websocket.send_json({"hello": "world"})
            await asyncio.sleep(10)

    # async def on_receive(self, websocket, data):
    #     print(f"websocket received: {data}")

    async def on_disconnect(self, websocket, close_code):
        print(f"websocket client disconnected, code={close_code}")


routes = [
    Route("/", Homepage),
    WebSocketRoute("/ws", WebSocketHandler)
]

app = Starlette(routes=routes)

# ======================================================================================================================#
# class MoneysAndNotificationsConsumer(WebsocketConsumer):
#     """
#     Не привязан к конкретному экрану
#     Обработка и отправка обновлений баланса и уведомлений о новых событиях
#     """
#     user: User = None
#
#     def connect(self):
#         self.accept()
#
#     def send(self, text_data=None, bytes_data=None, close=False):
#         """
#         переопределение метода для добавления логирования
#         :param text_data:
#         :param bytes_data:
#         :param close:
#         :return:
#         """
#         super().send(text_data, bytes_data, close)
#         logging.info(f'SEND ->> {json.loads(text_data)}')
#
#     @auth
#     def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         # logging.info(data)
#         _type = data.get('type')
#         if _type == SockTypes.auth.value:
#             async_to_sync(self.channel_layer.group_add)("notifications",
#                                                         self.channel_name)  # добавляем текущего пользователя в группу
#             self.user.notifications_channel_name = self.channel_name
#             # записываем в модель пользователя имя его канала
#             # для возможности отправки данных ему из любой части кода
#             self.send_user_balance()
#             self.send_events()
#         self.user.save()
#
#     def send_events(self) -> None:
#         """
#         Отправка уведомлений о событиях пользователю
#         """
#         events_count = Event.objects.filter(owner_id=self.user.pk, sent=False).count()
#         if not events_count:
#             self.send(json.dumps({'type': SockTypes.last_notifications.value,
#                                   'events': []}))
#             return
#         events = Event.objects.filter(owner_id=self.user.pk, sent=False).order_by('pk').reverse()[:10]
#         self.send(json.dumps({'type': SockTypes.last_notifications.value,
#                               'events': [event.event for event in events]}))
#         Event.objects.filter(owner_id=self.user.pk, sent__exact=False).update(sent=True)
#         if events_count > 10:
#             event_count_notification = Event.event_for_unread_count(self.user, events_count)
#             event_count_notification.save()
#
#     def send_user_balance(self) -> None:
#         """
#         Отправка текущего баланса пользователю
#         :return:
#         """
#         wallet = Wallet.objects.get(owner__pk=self.user.pk)
#         self.send(json.dumps({'type': SockTypes.moneys.value,
#                               **wallet.balance}))
#
#     def disconnect(self, _):
#         """
#         действия в случае закрытия соединения
#         :return:
#         """
#         async_to_sync(self.channel_layer.group_discard)("notifications", self.channel_name)
#         self.user.notifications_channel_name = None
#         self.user.save(update_fields=['notifications_channel_name'])
#         self.clear_user()
#
#     def chat_message(self, event):
#         """
#         метод, необходимый для django channels
#         :param event:
#         :return:
#         """
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps(message))
#
#     def clear_user(self):
#         def __clear_user():
#             time.sleep(30)
#             self.user.refresh_from_db()
#             if not any([self.user.notifications_channel_name,
#                         self.user.worlds_info_channel_name,
#                         self.user.pets_data_channel_name,
#                         self.user.terrain_channel_name]):
#                 self.user.selected_island = None
#                 self.user.center_point = None
#                 self.user.radius = None
#                 self.user.save(update_fields=['selected_island', 'center_point', 'radius'])
#
#         t = Thread(target=__clear_user)
#         t.start()
