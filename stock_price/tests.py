from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class StockRankingServiceTest(APITestCase):
    def test_get_fluctuation_rank(self):
        """
        [Service] 등락률 순위 조회 테스트
        """
        from stock_price.services import get_fluctuation_rank
        print("\n=== Testing Fluctuation Rank Service ===")
        result = get_fluctuation_rank()
        
        if result is None:
            print("[TEST] 등락률 순위 조회 실패 (API 오류 또는 장시간 외)")
        else:
            self.assertIsInstance(result, list)
            print(f"[TEST] 조회된 등락률 순위 개수: {len(result)}")
            if len(result) > 0: 
                for i, r in enumerate(result):
                    print(r)
                    # print(f"[TEST] {i+1}위: {r.get('hts_kor_isnm')} ({r.get('prdy_ctrt')}%)")

    def test_get_volume_rank(self):
        """
        [Service] 거래량 순위 조회 테스트
        """
        from stock_price.services import get_volume_rank
        print("\n=== Testing Volume Rank Service ===")
        result = get_volume_rank()
        
        if result is None:
             print("[TEST] 거래량 순위 조회 실패")
        else:
            self.assertIsInstance(result, list)
            print(f"[TEST] 조회된 거래량 순위 개수: {len(result)}")
            if len(result) > 0:
                for i, r in enumerate(result):
                    print(r)
                    # print(f"[TEST] {i+1}위: {r.get('hts_kor_isnm')} ({r.get('acml_vol')}주)")
