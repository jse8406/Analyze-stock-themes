import os
import json
import asyncio
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv
import websockets

# .env에서 키값 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

APP_KEY = os.getenv('g_appkey')
APP_SECRET = os.getenv('g_appsecret') or os.getenv('g_appsceret')
APPROVAL_KEY = os.getenv('g_approval_key')
TR_ID = "H0STCNT0"
STOCK_CODE = "005930"  # 예시: 삼성전자

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stock_code = self.scope['url_route']['kwargs']['stock_code']
        await self.accept()
        self.keep_running = True
        self.stock_task = asyncio.create_task(self.send_realtime_stock())

    async def disconnect(self, close_code):
        self.keep_running = False
        if hasattr(self, 'stock_task'):
            self.stock_task.cancel()

    async def send_realtime_stock(self):
        print("send_realtime_stock() started")  # 실행 여부 확인
        url = "ws://ops.koreainvestment.com:21000/tryitout/H0STCNT0"
        try:
            # 서버가 핸드쉐이크에서 헤더(또는 approval_key)를 요구하는 경우가 많습니다.
            # approval_key가 없으면 자동으로 발급 요청을 시도합니다.
            global APPROVAL_KEY
            if not APPROVAL_KEY:
                try:
                    print("approval_key not found in env — requesting Approval API...")
                    apr_url = "https://openapi.koreainvestment.com:9443/oauth2/Approval"
                    payload = {"grant_type": "client_credentials", "appkey": APP_KEY, "secretkey": APP_SECRET}
                    r = requests.post(apr_url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
                    if r.status_code == 200:
                        body = r.json()
                        # 응답 구조에 따라 키 이름이 다를 수 있으니 여러 키 확인
                        APPROVAL_KEY = body.get("approval_key") or body.get("approvalKey") or body.get("approvalKey")
                        if APPROVAL_KEY:
                            print("Obtained approval_key from API")
                        else:
                            msg = f"Approval API returned 200 but no approval_key field: {body}"
                            print(msg)
                            await self.send(text_data=json.dumps({"error": msg}))
                            return
                    else:
                        msg = f"Approval API failed: {r.status_code} {r.text}"
                        print(msg)
                        await self.send(text_data=json.dumps({"error": msg}))
                        return
                except Exception as e:
                    msg = f"Failed to request approval_key: {e}"
                    print(msg)
                    await self.send(text_data=json.dumps({"error": msg}))
                    return

            # extra_headers 파라미터는 현재 이벤트루프/라이브러리 조합에서 에러를 발생시킵니다.
            # 서버에 전달할 승인키는 WebSocket 바디의 header 필드에 포함해서 전송합니다.
            async with websockets.connect(url) as ws:
                senddata = {
                    "header": {
                        "appkey": APP_KEY,
                        "appsecret": APP_SECRET,
                        "approval_key": APPROVAL_KEY,
                        "custtype": "P",
                        "tr_type": "1",
                        "content-type": "utf-8"
                    },
                    "body": {
                        "input": {
                            "tr_id": TR_ID,
                            "tr_key": self.stock_code
                        }
                    }
                }
                # 일부 서버는 핸드쉐이크 헤더만으로 인증을 처리하므로,
                # 기존 바디 전송은 유지하되 중복되지 않도록 합니다.
                await ws.send(json.dumps(senddata))
                print("Request sent to server:", senddata)  # 요청 데이터 출력
                
                # 초기 응답 확인
                initial_response = await ws.recv()
                print("Initial response from server:", initial_response)  # 초기 응답 출력
                
                while self.keep_running:
                    data = await ws.recv()
                    print("Response from server:", data)  # 서버 응답 출력
                    await self.send(text_data=data)
        except Exception as e:
            print("Error in send_realtime_stock:", str(e))  # 예외 출력
            await self.send(text_data=json.dumps({"error": str(e)}))
