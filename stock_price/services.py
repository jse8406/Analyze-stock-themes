import requests
import os
from auth.kis_auth import get_access_token
from dotenv import load_dotenv

# Load env
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

APP_KEY = os.getenv('g_appkey')
APP_SECRET = os.getenv('g_appsecret')
DOMAIN = "https://openapi.koreainvestment.com:9443"

def get_fluctuation_rank(limit=30):
    """
    등락률 순위를 가져옵니다. (상위 30개 상승)
    TR_ID: FHPST01700000
    """
    token_data = get_access_token()
    if not token_data or 'access_token' not in token_data:
        print("[Stock Service] Token is missing")
        return None
    
    access_token = token_data['access_token']
    
    url = f"{DOMAIN}/uapi/domestic-stock/v1/ranking/fluctuation"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01700000",
        "custtype": "P",
    }
    
    params = {
        "fid_rsfl_rate2": "",
        "fid_cond_mrkt_div_code": "J",
        "fid_cond_scr_div_code": "20170",   # 화면번호
        "fid_input_iscd": "0000",           # 전체 종목
        "fid_rank_sort_cls_code": "0",      # 0: 상승률순
        "fid_input_cnt_1": "0",             # 누적일 수  
        "fid_prc_cls_code": "1",            # 1: 종가대비
        "fid_input_price_1": "",
        "fid_input_price_2": "",
        "fid_vol_cnt": "",
        "fid_trgt_cls_code": "0",
        "fid_trgt_exls_cls_code": "0",
        "fid_div_cls_code": "0",
        "fid_rsfl_rate1": "",
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        
        if data.get('rt_cd') != '0':
            print(f"[Stock Service] Fluctuation Rank Error: {data.get('msg1')} (Code: {data.get('msg_cd')})")
            return None
            
        output = data.get('output', [])
        return output

    except Exception as e:
        print(f"[Stock Service] Fluctuation Rank Request Error: {e}")
        return None
def get_volume_rank():
    """
    거래량 순위를 가져옵니다. (상위 30개)
    URL: /uapi/domestic-stock/v1/quotations/volume-rank
    TR_ID: FHPST01710000 (실전투자 전용)
    """
    token_data = get_access_token()
    if not token_data or 'access_token' not in token_data:
        return None
        
    access_token = token_data['access_token']
    
    url = f"{DOMAIN}/uapi/domestic-stock/v1/quotations/volume-rank" 
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01710000",  # [수정 1] 명세서에 명시된 실전 TR_ID 사용
        "custtype": "P",
    }

    params = {
       "FID_COND_MRKT_DIV_CODE": "J",       # 조건 시장 분류 코드 (J: 전체)
       "FID_COND_SCR_DIV_CODE": "20171",    # 조건 화면 분류 코드
       "FID_INPUT_ISCD": "0000",            # 입력 종목코드 (전체)
       "FID_DIV_CLS_CODE": "0",             # 분류 구분 코드 (0: 전체)
       "FID_BLNG_CLS_CODE": "0",            # 소속 구분 코드 (0: 평균거래량 - 보통 당일 거래량순)
       "FID_TRGT_CLS_CODE": "111111111",    # 대상 구분 코드 (9자리 - 전체 대상)
       
       # [수정 2] 명세서에 '10자리'라고 명시됨. (000000 -> 0000000000)
       "FID_TRGT_EXLS_CLS_CODE": "0000000000", 
       
       "FID_INPUT_PRICE_1": "",             # 입력 가격1 (공란)
       "FID_INPUT_PRICE_2": "",             # 입력 가격2 (공란)
       "FID_VOL_CNT": "",                   # 거래량 수 (공란)
       "FID_INPUT_DATE_1": ""               # 입력 날짜1 (공란)
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        
        # [디버깅] 응답 확인
        # print(f"[DEBUG] Volume Rank Raw Data: {data}")

        if data.get('rt_cd') == '0':
            output = data.get('output', [])
            # 템플릿 호환성을 위해 키를 소문자로 변환
            output = [{k.lower(): v for k, v in item.items()} for item in output]
            return output
        else:
            print(f"[Stock Service] Volume Rank Error: {data.get('msg1')} (Code: {data.get('msg_cd')})")
            return None
    except Exception as e:
        print(f"[Stock Service] Volume Rank Request Error: {e}")
        return None

def get_current_price(iscd):
    """
    특정 종목의 현재가를 조회합니다.
    TR_ID: FHKST01010100
    """
    token_data = get_access_token()
    if not token_data or 'access_token' not in token_data:
        return None
        
    access_token = token_data['access_token']
    url = f"{DOMAIN}/uapi/domestic-stock/v1/quotations/inquire-price"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST01010100",
        "custtype": "P",
    }
    
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": iscd
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        data = r.json()
        
        if data.get('rt_cd') == '0':
            return data.get('output', {})
        return None
    except Exception as e:
        print(f"[Stock Service] Get Price Error ({iscd}): {e}")
        return None

def get_theme_rank():
    """
    주요 테마별 등락률을 계산하여 순위를 반환합니다.
    """
    # 대한민국 대표 테마 정의
    themes = {
        "반도체 (Semiconductor)": ["005930", "000660", "042700"], # 삼성전자, SK하이닉스, 한미반도체
        "2차전지 (Battery)": ["373220", "006400", "003670", "247540"], # LG엔솔, 삼성SDI, 포스코퓨처엠, 에코프로비엠
        "자동차 (Auto)": ["005380", "000270", "012330"], # 현대차, 기아, 현대모비스
        "인터넷/플랫폼 (Platform)": ["035420", "035720"], # NAVER, 카카오
        "바이오 (Bio)": ["207940", "068270", "019170"], # 삼성바이오, 셀트리온, 신풍제약
        "엔터/콘텐츠 (K-Content)": ["352820", "041510", "122870"], # 하이브, 에스엠, 와이지엔터
        "금융 (Finance)": ["105560", "055550", "086790"], # KB금융, 신한지주, 하나금융지주
        "방산 (Defense)": ["012450", "042660"], # 한화에어로, 한화오션
    }
    
    # 테마별 등락률 계산
    theme_results = []
    
    # 성능을 위해 ThreadPool 사용 고려 가능하지만, 일단 순차 처리 (종목 수 적음)
    for theme_name, codes in themes.items():
        total_rate = 0
        count = 0
        
        # 대표 종목들의 등락률 평균 계산
        for code in codes:
            data = get_current_price(code)
            if data and 'prdy_ctrt' in data:
                try:
                    # prdy_ctrt: 전일대비율 (문자열)
                    rate = float(data['prdy_ctrt'])
                    total_rate += rate
                    count += 1
                except:
                    continue
        
        if count > 0:
            avg_rate = total_rate / count
            # 테마 평균 데이터 구성
            theme_results.append({
                'name': theme_name,
                'rate': round(avg_rate, 2),
                'is_rising': avg_rate > 0
            })
            
    # 등락률 순으로 정렬 (내림차순)
    theme_results.sort(key=lambda x: x['rate'], reverse=True)
    
    return theme_results