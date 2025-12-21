import os
from dotenv import load_dotenv
import asyncio
import websockets
import json

# .env 파일에서 환경변수 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

APP_KEY = os.getenv('g_appkey')
APP_SECRET = os.getenv('g_appsceret')
TR_ID = "H0STCNT0"  # 주식체결가 TR
STOCK_CODE = "005930"  # 예시: 삼성전자

async def get_realtime_stock_price():
    url = "wss://openapi.koreainvestment.com:9443/websocket"
    async with websockets.connect(url) as ws:
        senddata = {
            "header": {
                "appkey": APP_KEY,
                "appsecret": APP_SECRET,
                "custtype": "P",
                "tr_type": "1",
                "content-type": "utf-8"
            },
            "body": {
                "input": {
                    "tr_id": TR_ID,
                    "tr_key": STOCK_CODE
                }
            }
        }
        await ws.send(json.dumps(senddata))
        while True:
            data = await ws.recv()
            print(data)  # 실시간 체결가 데이터 출력

# 테스트용: python manage.py shell에서 아래 실행
# import asyncio; from api.views import get_realtime_stock_price; asyncio.run(get_realtime_stock_price())
from rest_framework import viewsets, status

# 실시간 주가 웹페이지 렌더링용 View
from django.views.generic import TemplateView

class StockRealtimeView(TemplateView):
    template_name = "stock_realtime.html"
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['GET'])
def hello_world(request):
    """
    간단한 테스트용 API 엔드포인트
    """
    return Response({
        'message': 'Hello, World!',
        'status': 'success'
    })


# 예시: 커스텀 모델 ViewSet
# from .models import Item
# from .serializers import ItemSerializer
#
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
