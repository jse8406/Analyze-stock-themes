# Django REST Framework 프로젝트

Django REST Framework를 사용한 REST API 백엔드 프로젝트입니다.

## 프로젝트 구조

```
web-project/
├── config/              # Django 프로젝트 설정
│   ├── settings.py     # 프로젝트 설정 파일
│   ├── urls.py         # 메인 URL 라우팅
│   └── wsgi.py         # WSGI 설정
├── api/                # API 앱
│   ├── models.py       # 데이터 모델
│   ├── serializers.py  # DRF 시리얼라이저
│   ├── views.py        # API 뷰
│   ├── urls.py         # API URL 라우팅
│   └── tests.py        # 테스트 코드
├── manage.py           # Django 관리 명령어
└── requirements.txt    # 패키지 의존성
```

## 설치 및 실행

### 1. 가상환경 활성화
```bash
.venv\Scripts\activate  # Windows
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 슈퍼유저 생성 (선택사항)
```bash
python manage.py createsuperuser
```

### 5. 개발 서버 실행
```bash
python manage.py runserver
```

서버가 시작되면 http://localhost:8000 에서 접속할 수 있습니다.

## 주요 페이지 및 API 엔드포인트

### 웹 페이지 (Frontend)
- `GET /stock_price/stock/`: **실시간 호가 페이지**
  - 실시간 주식 시세를 WebSocket을 통해 조회할 수 있는 페이지입니다.
  - 예: `/stock_price/stock/?code=005930&name=삼성전자`
- `GET /stock_price/stock/detail/<stock_code>/`: **종목 상세 정보 페이지**
  - 특정 종목의 현재가 등 상세 정보를 조회합니다.
  - 예: `/stock_price/stock/detail/005930/`

### API 엔드포인트
- `GET /stock_price/hello/`: 테스트용 Hello World API

### 웹소켓 (WebSocket)
- `ws://<host>/ws/stock/<stock_code>/`: 실시간 주식 시세 스트림
  - `stock_code`: 6자리 종목 코드 (예: 005930)

## 프로젝트 구조

### 주요 앱 (Apps)
- `auth`: KIS API 토큰 발급 및 인증 관리 (`kis_auth.py`)
- `stock_price`: 주식 시세 조회, 랭킹 서비스, 웹 페이지 제공 (`services.py`, `views.py`)

## 설정된 기능

- **실시간 주세 조회**: KIS WebSocket API 연동
- **랭킹 서비스**: 등락률 상위, 거래량 상위 종목 조회 (`services.py`)
- **자동완성**: 종목 검색 시 자동완성 기능 적용 (`stock_utils.js`)
- **Redis 연동**: Django Channels와 Redis를 활용한 실시간 데이터 브로드캐스팅

## 테스트 실행

```bash
# 전체 테스트
python manage.py test

# 특정 앱 테스트
python manage.py test stock_price
python manage.py test auth
```

## 참고 사항
- SK하이닉스 등 일부 종목의 호가 데이터 수신 문제 연구 중.


