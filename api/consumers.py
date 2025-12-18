import os
import json
import asyncio
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv
from .serializers import StockRequestSerializer, StockResponseSerializer
import websockets

# .env에서 키값 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

APP_KEY = os.getenv('g_appkey')
APP_SECRET = os.getenv('g_appsecret') or os.getenv('g_appsceret')
APPROVAL_KEY = None # 승인키는 연결 시 발급

# 설정 값
WS_BASE_URL = "ws://ops.koreainvestment.com:21000"
WS_PATH = ""  # 실제 투자 환경은 경로 없이 접속
TR_ID_HOGA = "H0UNASP0"  # 실시간 호가
TR_ID_EXEC = "H0STCNT0"  # 국내주식 실시간 체결 (H0UNCNT0 대신 사용)

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL에서 stock_code 추출
        self.stock_code = self.scope['url_route']['kwargs'].get('stock_code')
        await self.accept()
        # print(f"WebSocket connected for stock: {self.stock_code}")
        
        self.keep_running = True
        self.stock_task = asyncio.create_task(self.send_realtime_stock())

    async def disconnect(self, close_code):
        self.keep_running = False
        if hasattr(self, 'stock_task'):
            self.stock_task.cancel()

    async def get_approval_key(self):
        """실시간 접속키(Approval Key) 발급"""
        print("Requesting new Approval Key...")
        url = "https://openapi.koreainvestment.com:9443/oauth2/Approval"
        payload = {"grant_type": "client_credentials", "appkey": APP_KEY, "secretkey": APP_SECRET}
        try:
            r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
            if r.status_code == 200:
                body = r.json()
                key = body.get("approval_key") or body.get("approvalKey")
                if key:
                    print(f"Approval Key issued: {key[:10]}...")
                    return key
                else:
                    print(f"Approval Key missing in response: {body}")
            else:
                print(f"Approval Key request failed: {r.status_code} {r.text}")
        except Exception as e:
            print(f"Error requesting Approval Key: {e}")
        return None

    async def send_realtime_stock(self):
        """
            실시간 호가 데이터를 가져오는 메서드
        """
        print("실시간 호가 데이터를 가져오는 메서드")
        

        url = f"{WS_BASE_URL}{WS_PATH}"
        target_tr_id = TR_ID_HOGA

        # Approval Key 확인 및 발급
        global APPROVAL_KEY
        if not APPROVAL_KEY:
            APPROVAL_KEY = await self.get_approval_key()
            if not APPROVAL_KEY:
                await self.send(json.dumps({"error": "Failed to issue Approval Key"}))
                return

        try:
            async with websockets.connect(url) as ws:
                # 실시간 호가(H0UNASP0) 구독 요청
                senddata_hoga = StockRequestSerializer.build_payload(
                    approval_key=APPROVAL_KEY,
                    tr_id=TR_ID_HOGA,
                    stock_code=self.stock_code
                )
                await ws.send(json.dumps(senddata_hoga))
                print("Request sent (Hoga):", senddata_hoga)

                # 2. 실시간 체결가(H0UNCNT0) 구독 요청
                senddata_exec = StockRequestSerializer.build_payload(
                    approval_key=APPROVAL_KEY,
                    tr_id=TR_ID_EXEC,
                    stock_code=self.stock_code
                )
                await ws.send(json.dumps(senddata_exec))
                print("Request sent (Exec):", senddata_exec)
                
                # 초기 응답은 각각 올 수 있으므로 루프 진입 전 1개만 받지 않고, 루프 내에서 처리 권장
                # 하지만 여기서는 명시적으로 PINGPONG 등 처리를 위해 루프 바로 진입
                
                while self.keep_running:
                    data = await ws.recv()
                    # print(f"Raw Data ({len(data)}): {data[:50]}...") # 모든 데이터 로그 찍기

                    # raw string 데이터인지 확인 (Pipe | 포함 여부)
                    if isinstance(data, str) and '|' in data:
                        parts = data.split('|')
                        tr_id = parts[1] if len(parts) > 1 else ""
                        print(f"[BACKEND] Data received for TR_ID: {tr_id}")

                        from .serializers import StockAskingPriceResponseSerializer, StockResponseSerializer
                        
                        SerializerClass = None
                        if tr_id == "H0UNASP0":
                            SerializerClass = StockAskingPriceResponseSerializer
                        elif tr_id == "H0UNCNT0" or tr_id == "H0STCNT0":
                            SerializerClass = StockResponseSerializer

                        if SerializerClass:
                            parsed_dict = SerializerClass.parse_from_raw(data)
                            if parsed_dict:
                                # Serializer를 통해 검증 및 JSON 변환
                                serializer = SerializerClass(data=parsed_dict)
                                if serializer.is_valid():
                                    # 디버깅을 위해 예상 체결가 관련 필드 출력
                                    d = serializer.data
                                    # print(f"[DEBUG] Valid data parsed: {tr_id}")
                                    
                                    # 프론트엔드에 JSON으로 전송
                                    await self.send(text_data=json.dumps(serializer.data))
                                else:
                                    print(f"Validaton Error ({tr_id}):", serializer.errors)
                        else:
                             # 알 수 없는 TR_ID는 그냥 통과
                             pass
                    else:
                        print(f"Non-pipe data received: {data}")
                        # JSON 형태거나 다른 바이너리일 경우 그냥 바이패스
                        await self.send(text_data=data)
        except Exception as e:
            print("Error in send_realtime_stock:", str(e))
            await self.send(text_data=json.dumps({"error": str(e)}))
