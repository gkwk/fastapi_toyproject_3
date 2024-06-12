from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)
from database.database import database_dependency
from models import ChatSession
from exception_message.http_exception_params import http_exception_params


def chat_test_html(user_id, chat_session_id):
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <h2>Your ID: <span id="ws-id"></span></h2>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='users'>
            </ul>
            
            <hr>
            
            <ul id='messages'>
            </ul>
            <script>
                var client_id = {user_id}
                document.querySelector("#ws-id").textContent = client_id;
                var wsk = "None"
                
                const fetchDataFromAPI = async (url, method = 'GET', headers = {{}}, body = null) => {{
                try {{
                    // 요청 옵션 설정
                    const options = {{
                        method: method,
                        headers: {{
                            'Content-Type': 'application/json',
                            ...headers
                        }},
                        body: body ? JSON.stringify(body) : null
                    }};

                    // Fetch API를 사용하여 요청 전송
                    const response = await fetch(url, options);

                    // 응답이 성공적인지 확인
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}

                    // JSON 데이터 파싱
                    const data = await response.json();
                    return data;
                    }} catch (error) {{
                        // 에러 처리
                        console.error('Error fetching data:', error);
                        return null;
                        }}
                    }};
                
                
                // WebSocket 연결 생성 함수
                const createWebSocketConnection = (chatSessionId, accessToken) => {{
                    const wsUrl = `ws://${{location.host}}/api/v1/chat-sessions/${{chatSessionId}}/ws?websocket_access_token=${{accessToken}}`;
                    const ws = new WebSocket(wsUrl);

                    ws.onopen = () => {{
                        console.log('WebSocket connection opened.');
                    }};

                    ws.onmessage = (event) => {{
                        var jsonData = JSON.parse(event.data)
                    
                        if (jsonData.hasOwnProperty('message')) {{
                            var messages = document.getElementById('messages')
                            var message = document.createElement('li')
                            var content = document.createTextNode(jsonData.message)
                            message.appendChild(content)
                            messages.appendChild(message)
                        }}
                        
                        if (jsonData.hasOwnProperty('user_join')) {{
                            var users = document.getElementById('users')
                            var user = document.createElement('li')
                            user.id = `${{jsonData.user_join}}`
                            var content = document.createTextNode(jsonData.user_join)
                            user.appendChild(content)
                            users.appendChild(user)
                        }}
                        
                        if (jsonData.hasOwnProperty('user_left')) {{
                            var user = document.getElementById(`${{jsonData.user_left}}`)
                            user.remove()
                        }}
                    }};

                    ws.onclose = () => {{
                        console.log('WebSocket connection closed.');
                    }};

                    ws.onerror = (error) => {{
                        console.error('WebSocket error:', error);
                    }};

                    return ws;
                }};
                // API 요청 및 WebSocket 연결 예시
                const apiUrl = `http://${{location.host}}/api/v1/auth/issue-websocket-access-token`;
                const method = 'GET'; // 또는 'POST', 'PUT', 'DELETE' 등
                const headers = {{ 'Authorization': 'Bearer '+localStorage.getItem("access_token") }};
                const body = {{ key1: 'value1', key2: 'value2' }}; // POST, PUT 요청 시 사용

                fetchDataFromAPI(apiUrl, method, headers)
                    .then(data => {{
                        if (data) {{
                            console.log('Received data:', data);

                            // 가정: data 객체에 accessToken이 포함되어 있음
                            const accessToken = data.websocket_access_token;

                            // WebSocket 연결 생성
                            wsk = createWebSocketConnection({chat_session_id}, accessToken);
                        }} else {{
                            console.log('Failed to fetch data.');
                        }}
                    }});
                
                function sendMessage(event) {{
                    var input = document.getElementById("messageText")
                    wsk.send(JSON.stringify({{"message": input.value, "access_token": localStorage.getItem("access_token")}}))
                    input.value = ''
                    event.preventDefault()
                }}
            </script>
        </body>
    </html>
    """
    return html


def http_get(
    data_base: database_dependency,
    chat_session_id: int,
    token: current_user_access_token_payload,
):
    """
    채팅 세션에 접속하여 웹소켓을 통한 실시간 채팅기능 테스트를 수행할 수 있다.
    """
    user_id: int = token.get("user_id")
    if data_base.query(ChatSession).filter_by(id=chat_session_id).first():
        return HTMLResponse(chat_test_html(user_id, chat_session_id))
    else:
        raise HTTPException(**http_exception_params["not_exist_resource"])
