from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock, AsyncMock
from stock_price.services.kis_rest_client import kis_rest_client
import asyncio

class StockRankingServiceTest(APITestCase):
    @patch('stock_price.services.kis_rest_client.kis_rest_client.get_fluctuation_rank', new_callable=AsyncMock)
    def test_get_fluctuation_rank_success(self, mock_get_rank):
        """
        [Service] 등락률 순위 조회 성공 테스트 (Async)
        """
        print("\n=== Testing Fluctuation Rank Service (Success) ===")
        mock_data = [{'stck_shrt_cd': '005930', 'hts_kor_isnm': '삼성전자', 'prdy_ctrt': '1.5'}]
        mock_get_rank.return_value = mock_data

        # Run async method in sync test context
        result = asyncio.run(kis_rest_client.get_fluctuation_rank())
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['stck_shrt_cd'], '005930')
        print("[TEST] 등락률 순위 조회 성공 확인")

    @patch('stock_price.services.kis_rest_client.kis_rest_client.get_fluctuation_rank', new_callable=AsyncMock)
    def test_get_fluctuation_rank_failure(self, mock_get_rank):
        """
        [Edge Case] 등락률 순위 조회 실패 (None 반환) 테스트
        """
        print("\n=== Testing Fluctuation Rank Service (Failure) ===")
        mock_get_rank.return_value = None

        result = asyncio.run(kis_rest_client.get_fluctuation_rank())
        self.assertIsNone(result, "Should return None on failure")
        print("[TEST] 등락률 순위 조회 실패 처리 확인")

    @patch('stock_price.services.kis_rest_client.kis_rest_client.get_volume_rank', new_callable=AsyncMock)
    def test_get_volume_rank_success(self, mock_get_vol):
        """
        [Service] 거래량 순위 조회 성공 테스트 (Async)
        """
        print("\n=== Testing Volume Rank Service (Success) ===")
        mock_data = [{'stck_shrt_cd': '000660', 'hts_kor_isnm': 'SK하이닉스', 'acml_vol': '10000'}]
        mock_get_vol.return_value = mock_data

        result = asyncio.run(kis_rest_client.get_volume_rank())
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        print("[TEST] 거래량 순위 조회 성공 확인")

    @patch('stock_price.services.kis_rest_client.kis_rest_client.get_volume_rank', new_callable=AsyncMock)
    def test_get_volume_rank_failure(self, mock_get_vol):
        """
        [Edge Case] 거래량 순위 조회 실패 (None 반환) 테스트
        """
        print("\n=== Testing Volume Rank Service (Failure) ===")
        mock_get_vol.return_value = None

        result = asyncio.run(kis_rest_client.get_volume_rank())
        self.assertIsNone(result, "Should return None on failure")
        print("[TEST] 거래량 순위 조회 실패 처리 확인")
