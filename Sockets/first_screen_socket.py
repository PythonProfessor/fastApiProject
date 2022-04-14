

# ---------------------------------------- Ready socket ------------------------------------------------

# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID:s <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
#
# class ConnectionManager:
#     def __init__(self):
#         """Значит идея такая: создать список сокетов, которые будут добавляться в список"""
#         self.active_connections: List[WebSocket] = []
#         print(f"There are {self.active_connections}")
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         print("You have connected suc-ly")
#         self.active_connections.append(websocket)
#         print(f"Appended a new connection: {self.active_connections}")
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#         print(f"You've been disconnected there are {self.active_connections} left")
#
#
#     # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#     #async def send_personal_message(self, message: str, websocket: WebSocket):
#     #    await websocket.send_json(message)
#     #    print(f"The message is {message}")
#
#     async def send_water(self, websocket: WebSocket):
#         await websocket.send_text(f"The time is {datetime.utcnow()}")
#         with open('GameWorld/water.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
#             text = json.load(f)  # загнали все, что получилось в переменную
#         for i in range(1000):
#             await websocket.send_json(text)
#             await websocket.send_text(f"The time is {datetime.utcnow()}")
#
#     async def send_water(self):
#         pass
#
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_json(message)
#         # тут чекнуть кароч
#
#
# manager = ConnectionManager()
#
#
# @app.get("/")
# async def get():
#     return HTMLResponse(html)
#
#
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     await manager.send_water(websocket)
#     try:
#         while True:
#             # data = await websocket.receive_text()
#             data = await websocket.receive_json()
#             print(f"Type of data is: {type(data)}")
#             #await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
