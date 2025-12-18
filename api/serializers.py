from rest_framework import serializers
from django.contrib.auth.models import User


class StockRequestSerializer(serializers.Serializer):
    """
    외부 API 전송용 Serializer (DTO 역할)
    """
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    @classmethod
    def build_payload(cls, approval_key, tr_id, stock_code, custtype="P", tr_type="1"):
        return {
            "header": {
                "approval_key": approval_key,
                "custtype": custtype,
                "tr_type": tr_type,
                "content-type": "utf-8"
            },
            "body": {
                "input": {
                    "tr_id": tr_id,
                    "tr_key": stock_code
                }
            }
        }


class StockResponseSerializer(serializers.Serializer):
    """
    실시간 주식 체결가 응답용 Serializer
    """
    MKSC_SHRN_ISCD = serializers.CharField(help_text="유가증권 단축 종목코드", required=False, allow_blank=True, allow_null=True)
    STCK_CNTG_HOUR = serializers.CharField(help_text="주식 체결 시간", required=False, allow_blank=True, allow_null=True)
    STCK_PRPR = serializers.FloatField(help_text="주식 현재가", required=False, allow_null=True)
    PRDY_VRSS_SIGN = serializers.CharField(help_text="전일 대비 부호", required=False, allow_blank=True, allow_null=True)
    PRDY_VRSS = serializers.FloatField(help_text="전일 대비", required=False, allow_null=True)
    PRDY_CTRT = serializers.FloatField(help_text="전일 대비율", required=False, allow_null=True)
    WGHN_AVRG_STCK_PRC = serializers.FloatField(help_text="가중 평균 주식 가격", required=False, allow_null=True)
    STCK_OPRC = serializers.FloatField(help_text="주식 시가", required=False, allow_null=True)
    STCK_HGPR = serializers.FloatField(help_text="주식 최고가", required=False, allow_null=True)
    STCK_LWPR = serializers.FloatField(help_text="주식 최저가", required=False, allow_null=True)
    ASKP1 = serializers.FloatField(help_text="매도호가1", required=False, allow_null=True)
    BIDP1 = serializers.FloatField(help_text="매수호가1", required=False, allow_null=True)
    CNTG_VOL = serializers.FloatField(help_text="체결 거래량", required=False, allow_null=True)
    ACML_VOL = serializers.FloatField(help_text="누적 거래량", required=False, allow_null=True)
    ACML_TR_PBMN = serializers.FloatField(help_text="누적 거래 대금", required=False, allow_null=True)
    SELN_CNTG_CSNU = serializers.FloatField(help_text="매도 체결 건수", required=False, allow_null=True)
    SHNU_CNTG_CSNU = serializers.FloatField(help_text="매수 체결 건수", required=False, allow_null=True)
    NTBY_CNTG_CSNU = serializers.FloatField(help_text="순매수 체결 건수", required=False, allow_null=True)
    CTTR = serializers.FloatField(help_text="체결강도", required=False, allow_null=True)
    SELN_CNTG_SMTN = serializers.FloatField(help_text="총 매도 수량", required=False, allow_null=True)
    SHNU_CNTG_SMTN = serializers.FloatField(help_text="총 매수 수량", required=False, allow_null=True)
    CCLD_DVSN = serializers.CharField(help_text="체결구분", required=False, allow_blank=True, allow_null=True)
    SHNU_RATE = serializers.FloatField(help_text="매수비율", required=False, allow_null=True)
    PRDY_VOL_VRSS_ACML_VOL_RATE = serializers.FloatField(help_text="전일 거래량 대비 등락율", required=False, allow_null=True)
    OPRC_HOUR = serializers.CharField(help_text="시가 시간", required=False, allow_blank=True, allow_null=True)
    OPRC_VRSS_PRPR_SIGN = serializers.CharField(help_text="시가대비구분", required=False, allow_blank=True, allow_null=True)
    OPRC_VRSS_PRPR = serializers.FloatField(help_text="시가대비", required=False, allow_null=True)
    HGPR_HOUR = serializers.CharField(help_text="최고가 시간", required=False, allow_blank=True, allow_null=True)
    HGPR_VRSS_PRPR_SIGN = serializers.CharField(help_text="고가대비구분", required=False, allow_blank=True, allow_null=True)
    HGPR_VRSS_PRPR = serializers.FloatField(help_text="고가대비", required=False, allow_null=True)
    LWPR_HOUR = serializers.CharField(help_text="최저가 시간", required=False, allow_blank=True, allow_null=True)
    LWPR_VRSS_PRPR_SIGN = serializers.CharField(help_text="저가대비구분", required=False, allow_blank=True, allow_null=True)
    LWPR_VRSS_PRPR = serializers.FloatField(help_text="저가대비", required=False, allow_null=True)
    BSOP_DATE = serializers.CharField(help_text="영업 일자", required=False, allow_blank=True, allow_null=True)
    NEW_MKOP_CLS_CODE = serializers.CharField(help_text="신 장운영 구분 코드", required=False, allow_blank=True, allow_null=True)
    TRHT_YN = serializers.CharField(help_text="거래정지 여부", required=False, allow_blank=True, allow_null=True)
    ASKP_RSQN1 = serializers.FloatField(help_text="매도호가 잔량1", required=False, allow_null=True)
    BIDP_RSQN1 = serializers.FloatField(help_text="매수호가 잔량1", required=False, allow_null=True)
    TOTAL_ASKP_RSQN = serializers.FloatField(help_text="총 매도호가 잔량", required=False, allow_null=True)
    TOTAL_BIDP_RSQN = serializers.FloatField(help_text="총 매수호가 잔량", required=False, allow_null=True)
    VOL_TNRT = serializers.FloatField(help_text="거래량 회전율", required=False, allow_null=True)
    PRDY_SMNS_HOUR_ACML_VOL = serializers.FloatField(help_text="전일 동시간 누적 거래량", required=False, allow_null=True)
    PRDY_SMNS_HOUR_ACML_VOL_RATE = serializers.FloatField(help_text="전일 동시간 누적 거래량 비율", required=False, allow_null=True)
    HOUR_CLS_CODE = serializers.CharField(help_text="시간 구분 코드", required=False, allow_blank=True, allow_null=True)
    MRKT_TRTM_CLS_CODE = serializers.CharField(help_text="임의종료구분코드", required=False, allow_blank=True, allow_null=True)
    VI_STND_PRC = serializers.FloatField(help_text="정적VI발동기준가", required=False, allow_null=True)

    @classmethod
    def parse_from_raw(cls, raw_data):
        """
        0|H0STCNT0|001|005930^... 형태의 로우 데이터를 파싱하여 딕셔너리로 반환
        """
        try:
            # 1. 메타 데이터 분리 (Pipe | 구분)
            parts = raw_data.split('|')
            if len(parts) < 4:
                return None  # 올바르지 않은 형식
            
            # parts[0]: 암호화여부, parts[1]: TR_ID, parts[2]: 개수, parts[3]: 실제데이터(들)
            # 여기서는 편의상 첫 번째 데이터 블록만 처리하거나 ^로 전체를 나눔
            
            # 실제 데이터 부분 (마지막 요소)
            content = parts[3]
            
            # 2. 데이터 필드 분리 (Caret ^ 구분)
            fields = content.split('^')
            
            # 필드 개수가 부족하면 처리 불가 (API 스펙에 따라 46개 내외)
            # 안전하게 매핑 (인덱스 에러 방지)
            def get_val(idx, type_func=str):
                try:
                    val = fields[idx]
                    return type_func(val)
                except (IndexError, ValueError):
                    return None

            data = {
                "MKSC_SHRN_ISCD": get_val(0),
                "STCK_CNTG_HOUR": get_val(1),
                "STCK_PRPR": get_val(2, float),
                "PRDY_VRSS_SIGN": get_val(3),
                "PRDY_VRSS": get_val(4, float),
                "PRDY_CTRT": get_val(5, float),
                "WGHN_AVRG_STCK_PRC": get_val(6, float),
                "STCK_OPRC": get_val(7, float),
                "STCK_HGPR": get_val(8, float),
                "STCK_LWPR": get_val(9, float),
                "ASKP1": get_val(10, float),
                "BIDP1": get_val(11, float),
                "CNTG_VOL": get_val(12, float),
                "ACML_VOL": get_val(13, float),
                "ACML_TR_PBMN": get_val(14, float),
                "SELN_CNTG_CSNU": get_val(15, float),
                "SHNU_CNTG_CSNU": get_val(16, float),
                "NTBY_CNTG_CSNU": get_val(17, float),
                "CTTR": get_val(18, float),
                "SELN_CNTG_SMTN": get_val(19, float),
                "SHNU_CNTG_SMTN": get_val(20, float),
                "CCLD_DVSN": get_val(21),
                "SHNU_RATE": get_val(22, float),
                "PRDY_VOL_VRSS_ACML_VOL_RATE": get_val(23, float),
                "OPRC_HOUR": get_val(24),
                "OPRC_VRSS_PRPR_SIGN": get_val(25),
                "OPRC_VRSS_PRPR": get_val(26, float),
                "HGPR_HOUR": get_val(27),
                "HGPR_VRSS_PRPR_SIGN": get_val(28),
                "HGPR_VRSS_PRPR": get_val(29, float),
                "LWPR_HOUR": get_val(30),
                "LWPR_VRSS_PRPR_SIGN": get_val(31),
                "LWPR_VRSS_PRPR": get_val(32, float),
                "BSOP_DATE": get_val(33),
                "NEW_MKOP_CLS_CODE": get_val(34),
                "TRHT_YN": get_val(35),
                "ASKP_RSQN1": get_val(36, float),
                "BIDP_RSQN1": get_val(37, float),
                "TOTAL_ASKP_RSQN": get_val(38, float),
                "TOTAL_BIDP_RSQN": get_val(39, float),
                "VOL_TNRT": get_val(40, float),
                "PRDY_SMNS_HOUR_ACML_VOL": get_val(41, float),
                "PRDY_SMNS_HOUR_ACML_VOL_RATE": get_val(42, float),
                "HOUR_CLS_CODE": get_val(43),
                "MRKT_TRTM_CLS_CODE": get_val(44),
                "VI_STND_PRC": get_val(45, float),
            }
            return data
        except Exception:
            return None

class StockAskingPriceResponseSerializer(serializers.Serializer):
    """
    실시간 주식 호가(H0UNASP0) 응답용 Serializer
    """
    MKSC_SHRN_ISCD = serializers.CharField(help_text="유가증권 단축 종목코드", required=False, allow_blank=True, allow_null=True)
    BSOP_HOUR = serializers.CharField(help_text="영업 시간", required=False, allow_blank=True, allow_null=True)
    HOUR_CLS_CODE = serializers.CharField(help_text="시간 구분 코드", required=False, allow_blank=True, allow_null=True)
    ASKP1 = serializers.FloatField(help_text="매도호가1", required=False, allow_null=True)
    ASKP2 = serializers.FloatField(help_text="매도호가2", required=False, allow_null=True)
    ASKP3 = serializers.FloatField(help_text="매도호가3", required=False, allow_null=True)
    ASKP4 = serializers.FloatField(help_text="매도호가4", required=False, allow_null=True)
    ASKP5 = serializers.FloatField(help_text="매도호가5", required=False, allow_null=True)
    ASKP6 = serializers.FloatField(help_text="매도호가6", required=False, allow_null=True)
    ASKP7 = serializers.FloatField(help_text="매도호가7", required=False, allow_null=True)
    ASKP8 = serializers.FloatField(help_text="매도호가8", required=False, allow_null=True)
    ASKP9 = serializers.FloatField(help_text="매도호가9", required=False, allow_null=True)
    ASKP10=serializers.FloatField(help_text="매도호가10", required=False, allow_null=True)
    BIDP1 = serializers.FloatField(help_text="매수호가1", required=False, allow_null=True)
    BIDP2 = serializers.FloatField(help_text="매수호가2", required=False, allow_null=True)
    BIDP3 = serializers.FloatField(help_text="매수호가3", required=False, allow_null=True)
    BIDP4 = serializers.FloatField(help_text="매수호가4", required=False, allow_null=True)
    BIDP5 = serializers.FloatField(help_text="매수호가5", required=False, allow_null=True)
    BIDP6 = serializers.FloatField(help_text="매수호가6", required=False, allow_null=True)
    BIDP7 = serializers.FloatField(help_text="매수호가7", required=False, allow_null=True)
    BIDP8 = serializers.FloatField(help_text="매수호가8", required=False, allow_null=True)
    BIDP9 = serializers.FloatField(help_text="매수호가9", required=False, allow_null=True)
    BIDP10=serializers.FloatField(help_text="매수호가10", required=False, allow_null=True)
    ASKP_RSQN1 = serializers.FloatField(help_text="매도호가 잔량1", required=False, allow_null=True)
    ASKP_RSQN2 = serializers.FloatField(help_text="매도호가 잔량2", required=False, allow_null=True)
    ASKP_RSQN3 = serializers.FloatField(help_text="매도호가 잔량3", required=False, allow_null=True)
    ASKP_RSQN4 = serializers.FloatField(help_text="매도호가 잔량4", required=False, allow_null=True)
    ASKP_RSQN5 = serializers.FloatField(help_text="매도호가 잔량5", required=False, allow_null=True)
    ASKP_RSQN6 = serializers.FloatField(help_text="매도호가 잔량6", required=False, allow_null=True)
    ASKP_RSQN7 = serializers.FloatField(help_text="매도호가 잔량7", required=False, allow_null=True)
    ASKP_RSQN8 = serializers.FloatField(help_text="매도호가 잔량8", required=False, allow_null=True)
    ASKP_RSQN9 = serializers.FloatField(help_text="매도호가 잔량9", required=False, allow_null=True)
    ASKP_RSQN10=serializers.FloatField(help_text="매도호가 잔량10", required=False, allow_null=True)
    BIDP_RSQN1 = serializers.FloatField(help_text="매수호가 잔량1", required=False, allow_null=True)
    BIDP_RSQN2 = serializers.FloatField(help_text="매수호가 잔량2", required=False, allow_null=True)
    BIDP_RSQN3 = serializers.FloatField(help_text="매수호가 잔량3", required=False, allow_null=True)
    BIDP_RSQN4 = serializers.FloatField(help_text="매수호가 잔량4", required=False, allow_null=True)
    BIDP_RSQN5 = serializers.FloatField(help_text="매수호가 잔량5", required=False, allow_null=True)
    BIDP_RSQN6 = serializers.FloatField(help_text="매수호가 잔량6", required=False, allow_null=True)
    BIDP_RSQN7 = serializers.FloatField(help_text="매수호가 잔량7", required=False, allow_null=True)
    BIDP_RSQN8 = serializers.FloatField(help_text="매수호가 잔량8", required=False, allow_null=True)
    BIDP_RSQN9 = serializers.FloatField(help_text="매수호가 잔량9", required=False, allow_null=True)
    BIDP_RSQN10=serializers.FloatField(help_text="매수호가 잔량10", required=False, allow_null=True)
    TOTAL_ASKP_RSQN = serializers.FloatField(help_text="총 매도호가 잔량", required=False, allow_null=True)
    TOTAL_BIDP_RSQN = serializers.FloatField(help_text="총 매수호가 잔량", required=False, allow_null=True)
    OVTM_TOTAL_ASKP_RSQN = serializers.FloatField(help_text="시간외 총 매도호가 잔량", required=False, allow_null=True)
    OVTM_TOTAL_BIDP_RSQN = serializers.FloatField(help_text="시간외 총 매수호가 잔량", required=False, allow_null=True)
    ANTC_CNPR = serializers.FloatField(help_text="예상 체결가", required=False, allow_null=True)
    ANTC_CNQN = serializers.FloatField(help_text="예상 체결량", required=False, allow_null=True)
    ANTC_VOL = serializers.FloatField(help_text="예상 거래량", required=False, allow_null=True)
    ANTC_CNTG_VRSS = serializers.FloatField(help_text="예상 체결 대비", required=False, allow_null=True)
    ANTC_CNTG_VRSS_SIGN = serializers.CharField(help_text="예상 체결 대비 부호", required=False, allow_blank=True, allow_null=True)
    ANTC_CNTG_PRDY_CTRT = serializers.FloatField(help_text="예상 체결 전일 대비율", required=False, allow_null=True)
    ACML_VOL = serializers.FloatField(help_text="누적 거래량", required=False, allow_null=True)
    TOTAL_ASKP_RSQN_ICDC = serializers.FloatField(help_text="총 매도호가 잔량 증감", required=False, allow_null=True)
    TOTAL_BIDP_RSQN_ICDC = serializers.FloatField(help_text="총 매수호가 잔량 증감", required=False, allow_null=True)
    OVTM_TOTAL_ASKP_ICDC = serializers.FloatField(help_text="시간외 총 매도호가 증감", required=False, allow_null=True)
    OVTM_TOTAL_BIDP_ICDC = serializers.FloatField(help_text="시간외 총 매수호가 증감", required=False, allow_null=True)
    STCK_DEAL_CLS_CODE = serializers.CharField(help_text="주식 매매 구분 코드", required=False, allow_blank=True, allow_null=True)
    KMID_PRC = serializers.FloatField(help_text="KRX 중간가", required=False, allow_null=True)
    KMID_TOTAL_RSQN = serializers.FloatField(help_text="KRX 중간가잔량합계수량", required=False, allow_null=True)
    KMID_CLS_CODE = serializers.CharField(help_text="KRX 중간가 매수매도 구분", required=False, allow_blank=True, allow_null=True)
    NMID_PRC = serializers.FloatField(help_text="NXT 중간가", required=False, allow_null=True)
    NMID_TOTAL_RSQN = serializers.FloatField(help_text="NXT 중간가잔량합계수량", required=False, allow_null=True)
    NMID_CLS_CODE = serializers.CharField(help_text="NXT 중간가 매수매도 구분", required=False, allow_blank=True, allow_null=True)

    @classmethod
    def parse_from_raw(cls, raw_data):
        try:
            parts = raw_data.split('|')
            if len(parts) < 4:
                return None
            content = parts[3]
            fields = content.split('^')
            
            def get_val(idx, type_func=str):
                try:
                    val = fields[idx]
                    return type_func(val)
                except (IndexError, ValueError):
                    return None

            return {
                "MKSC_SHRN_ISCD": get_val(0),
                "BSOP_HOUR": get_val(1),
                "HOUR_CLS_CODE": get_val(2),
                "ASKP1": get_val(3, float),
                "ASKP2": get_val(4, float),
                "ASKP3": get_val(5, float),
                "ASKP4": get_val(6, float),
                "ASKP5": get_val(7, float),
                "ASKP6": get_val(8, float),
                "ASKP7": get_val(9, float),
                "ASKP8": get_val(10, float),
                "ASKP9": get_val(11, float),
                "ASKP10": get_val(12, float),
                "BIDP1": get_val(13, float),
                "BIDP2": get_val(14, float),
                "BIDP3": get_val(15, float),
                "BIDP4": get_val(16, float),
                "BIDP5": get_val(17, float),
                "BIDP6": get_val(18, float),
                "BIDP7": get_val(19, float),
                "BIDP8": get_val(20, float),
                "BIDP9": get_val(21, float),
                "BIDP10": get_val(22, float),
                "ASKP_RSQN1": get_val(23, float),
                "ASKP_RSQN2": get_val(24, float),
                "ASKP_RSQN3": get_val(25, float),
                "ASKP_RSQN4": get_val(26, float),
                "ASKP_RSQN5": get_val(27, float),
                "ASKP_RSQN6": get_val(28, float),
                "ASKP_RSQN7": get_val(29, float),
                "ASKP_RSQN8": get_val(30, float),
                "ASKP_RSQN9": get_val(31, float),
                "ASKP_RSQN10": get_val(32, float),
                "BIDP_RSQN1": get_val(33, float),
                "BIDP_RSQN2": get_val(34, float),
                "BIDP_RSQN3": get_val(35, float),
                "BIDP_RSQN4": get_val(36, float),
                "BIDP_RSQN5": get_val(37, float),
                "BIDP_RSQN6": get_val(38, float),
                "BIDP_RSQN7": get_val(39, float),
                "BIDP_RSQN8": get_val(40, float),
                "BIDP_RSQN9": get_val(41, float),
                "BIDP_RSQN10": get_val(42, float),
                "TOTAL_ASKP_RSQN": get_val(43, float),
                "TOTAL_BIDP_RSQN": get_val(44, float),
                "OVTM_TOTAL_ASKP_RSQN": get_val(45, float),
                "OVTM_TOTAL_BIDP_RSQN": get_val(46, float),
                "ANTC_CNPR": get_val(47, float),
                "ANTC_CNQN": get_val(48, float),
                "ANTC_VOL": get_val(49, float),
                "ANTC_CNTG_VRSS": get_val(50, float),
                "ANTC_CNTG_VRSS_SIGN": get_val(51),
                "ANTC_CNTG_PRDY_CTRT": get_val(52, float),
                "ACML_VOL": get_val(53, float),
                "TOTAL_ASKP_RSQN_ICDC": get_val(54, float),
                "TOTAL_BIDP_RSQN_ICDC": get_val(55, float),
                "OVTM_TOTAL_ASKP_ICDC": get_val(56, float),
                "OVTM_TOTAL_BIDP_ICDC": get_val(57, float),
                "STCK_DEAL_CLS_CODE": get_val(58),
                "KMID_PRC": get_val(59, float),
                "KMID_TOTAL_RSQN": get_val(60, float),
                "KMID_CLS_CODE": get_val(61),
                "NMID_PRC": get_val(62, float),
                "NMID_TOTAL_RSQN": get_val(63, float),
                "NMID_CLS_CODE": get_val(64),
            }
        except Exception:
            return None
