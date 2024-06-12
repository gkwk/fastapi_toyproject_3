import json
from typing import Any, Dict

from starlette.websockets import WebSocketState
from fastapi import WebSocket, WebSocketDisconnect, Path, Query
from jwt.exceptions import InvalidTokenError


from database.database import database_dependency
from models import Chat, ChatSession
from auth.jwt.access_token.get_user_access_token_payload import (
    get_user_access_token_payload_for_websocket,
)
from auth.jwt.websocket_access_token.get_user_websocket_access_token_payload import (
    get_user_websocket_access_token_payload_without_query,
)
from exception_message.http_exception_params import http_exception_params


class ConnectionManager:
    def __init__(self):
        # {
        #   chat_session_id: {
        #       websocket: {
        #           "user_id": user_id,
        #           "verified" : boolean,
        #       },
        # }
        self.active_connections: Dict[int, Dict["WebSocket", Dict[str, Any]]] = dict()

        # {
        #   user_id: {
        #       chat_session_id: websocket,
        #   }
        self.active_user_id: Dict[int, Dict[int, "WebSocket"]] = dict()

    async def connect(self, websocket: WebSocket, chat_session_id: int, user_id: int):
        if not chat_session_id in self.active_connections:
            self.active_connections[chat_session_id] = dict()

        if not user_id in self.active_user_id:
            self.active_user_id[user_id] = dict()

        if not chat_session_id in self.active_user_id[user_id]:
            self.active_connections[chat_session_id][websocket] = dict()
            self.active_connections[chat_session_id][websocket]["user_id"] = user_id
            self.active_connections[chat_session_id][websocket]["verified"] = False
            self.active_user_id[user_id][chat_session_id] = websocket
        else:
            previouse_websocket = self.active_user_id[user_id][chat_session_id]
            await self.active_user_id[user_id][chat_session_id].close()
            self.active_connections[chat_session_id].pop(previouse_websocket)

            self.active_connections[chat_session_id][websocket] = dict()
            self.active_connections[chat_session_id][websocket]["user_id"] = user_id
            self.active_connections[chat_session_id][websocket]["verified"] = False
            self.active_user_id[user_id][chat_session_id] = websocket

        await websocket.accept()

    async def disconnect(
        self, websocket: WebSocket, chat_session_id: int, user_id: int
    ):
        self.active_connections[chat_session_id].pop(websocket)
        self.active_user_id[user_id].pop(chat_session_id)
        
        if not websocket.state != WebSocketState.DISCONNECTED:
            await websocket.close()

    async def verify_user(
        self,
        websocket: WebSocket,
        data_base: database_dependency,
        chat_session_id: int,
        token: str,
    ):
        # 연속적으로 한 사용자로부터 들어온 메세지가 수백개있고, 우연히 절반이 처리 중 access token이 만료된다면 어떻게 처리해야 하는가?
        # 클라이언트 측에서 메세지 전송 시 토큰 만료를 검증하여 10초전 토큰만 보낸다.
        # 서버 처리가 느려서 10초전 토큰도 도착시 만료되었다면? 토큰 만료 시간을 1분 30초로 하고 클라이언트에서 50초마다 갱신? (하지만 access 토큰이 갱신되면 블랙리스트에 오른다.)
        # Celery등을 이용하여 토큰만 검증하고 토큰 검증이 끝난 메세지들을 순차적 처리?
        # 처리되었다는 메세지를 전송하고 클라이언트는 해당 메세지가 도착하지 않으면 전송하지 않도록 제어?
        try:
            get_user_access_token_payload_for_websocket(
                data_base=data_base, token=token
            )
            self.active_connections[chat_session_id][websocket]["verified"] = True
        except Exception:
            # if self.active_connections[chat_session_id][websocket]["verified"] == False:
            #     # 현재 처리 과정상 불필요하지만 차후를 대비해 삭제하지 않는다.
            #     raise InvalidTokenError
            # else:
            #     self.active_connections[chat_session_id][websocket]["verified"] = False
            self.active_connections[chat_session_id][websocket]["verified"] = False

        return self.active_connections[chat_session_id][websocket]["verified"]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, chatting_room_id: int):
        for connection in self.active_connections[chatting_room_id]:
            await connection.send_text(message)


manager = ConnectionManager()
json_encoder = json.JSONEncoder()
json_decoder = json.JSONDecoder()


def create_chat(
    data_base: database_dependency,
    token: dict,
    content: str,
    chat_session_id: int,
):
    chat = Chat(
        user_id=token.get("user_id"),
        chat_session_id=chat_session_id,
        content=content,
    )
    data_base.add(chat)
    data_base.commit()

    return chat.id


def get_chats(
    data_base: database_dependency,
    token: dict,
    chat_session_id: int,
    skip: int | None,
    limit: int | None,
):
    filter_kwargs = {"chat_session_id": chat_session_id}

    if skip == None:
        skip = 0
    if limit == None:
        limit = 10

    chats = (
        data_base.query(Chat)
        .filter_by(**filter_kwargs)
        .order_by(Chat.create_date.asc(), Chat.id.asc())
    )
    total = chats.count()
    chats = chats.offset(skip).limit(limit).all()
    return {"total": total, "chats": chats}


async def websocket_chat_session(
    websocket: WebSocket,
    data_base: database_dependency,
    chat_session_id: int = Path(ge=1),
    websocket_access_token: str = Query(""),
):
    t_bool = False
    try:
        websocket_access_token_payload = (
            get_user_websocket_access_token_payload_without_query(
                data_base=data_base, token=websocket_access_token
            )
        )
        if data_base.query(ChatSession).filter_by(id=chat_session_id).first():
            t_bool = True
    except Exception:
        return None

    if t_bool:
        await manager.connect(
            websocket, chat_session_id, websocket_access_token_payload.get("user_id")
        )
        try:
            for t_websocket in manager.active_connections[chat_session_id]:
                t_user_id = manager.active_connections[chat_session_id][t_websocket][
                    "user_id"
                ]
                if t_user_id != websocket_access_token_payload.get("user_id"):
                    await manager.send_personal_message(
                        json_encoder.encode(o={"user_join": f"{t_user_id}"}), websocket
                    )

            for chat_query in get_chats(
                data_base=data_base,
                token=websocket_access_token_payload,
                chat_session_id=chat_session_id,
                skip=0,
                limit=10,
            ).get("chats"):
                await manager.send_personal_message(
                    json_encoder.encode(o={"message": f"{chat_query.content}"}),
                    websocket,
                )

            await manager.broadcast(
                json_encoder.encode(
                    o={
                        "message": f'Client #{websocket_access_token_payload.get("user_id")} joined the chat'
                    }
                ),
                chat_session_id,
            )
            await manager.broadcast(
                json_encoder.encode(
                    o={"user_join": f'{websocket_access_token_payload.get("user_id")}'}
                ),
                chat_session_id,
            )
            while True:
                data = await websocket.receive_text()
                data = json_decoder.decode(data)
                access_token = data["access_token"]
                message = data["message"]

                is_user_verified_before_verification = manager.active_connections[
                    chat_session_id
                ][websocket]["verified"]
                is_user_verified_after_verification = await manager.verify_user(
                    websocket=websocket,
                    data_base=data_base,
                    chat_session_id=chat_session_id,
                    token=access_token,
                )

                if is_user_verified_after_verification:
                    create_chat(
                        data_base=data_base,
                        token=websocket_access_token_payload,
                        content=message,
                        chat_session_id=chat_session_id,
                    )
                    await manager.send_personal_message(
                        json_encoder.encode(o={"message": f"You wrote: {message}"}),
                        websocket,
                    )
                    await manager.broadcast(
                        json_encoder.encode(
                            o={
                                "message": f'Client #{websocket_access_token_payload.get("user_id")} says: {message}'
                            }
                        ),
                        chat_session_id,
                    )

                elif (
                    not is_user_verified_after_verification
                    and is_user_verified_before_verification
                ):
                    await manager.send_personal_message(
                        json_encoder.encode(
                            o={
                                "message": f"Your submitted access token is invalid",
                                "refresh_access_token": True,
                            }
                        ),
                        websocket,
                    )

                else:
                    await manager.send_personal_message(
                        json_encoder.encode(
                            o={
                                "message": f"You are kicked out",
                                "re_join": True,
                            }
                        ),
                        websocket,
                    )
                    raise InvalidTokenError
        except (WebSocketDisconnect, InvalidTokenError):
            if websocket in manager.active_connections[chat_session_id]:
                
                await manager.disconnect(
                    websocket,
                    chat_session_id,
                    websocket_access_token_payload.get("user_id"),
                )
            await manager.broadcast(
                json_encoder.encode(
                    o={"user_left": f'{websocket_access_token_payload.get("user_id")}'}
                ),
                chat_session_id,
            )
        except Exception:
            print("Error")
