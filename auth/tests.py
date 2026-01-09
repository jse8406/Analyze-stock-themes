
from django.test import TestCase
from .kis_auth import get_access_token, get_approval_key, get_current_price

class KISAuthTokenTest(TestCase):
    def test_get_approval_key(self):
        """
        get_approval_key 함수가 정상적으로 approval_key를 반환하는지 테스트
        """
        result = get_approval_key()
        self.assertIsNotNone(result, "get_approval_key() should not return None")
        self.assertIsInstance(result, str, "approval_key should be a string")
        self.assertTrue(result, "approval_key should not be empty")
        print("[TEST] Approval key 발급 성공!")
    
    def test_get_access_token_returns_token(self):
        """
        get_access_token 함수가 정상적으로 access_token을 반환하는지 테스트
        """
        result = get_access_token()
        self.assertIsNotNone(result, "get_access_token() should not return None")
        self.assertIn("access_token", result, "Response should contain 'access_token'")
        self.assertTrue(result["access_token"], "access_token should not be empty")
        print("[TEST] Access token 발급 성공!")

    def test_get_access_token_uses_cache(self):
        """
        두 번째 호출 시 캐시된 토큰을 사용하는지 테스트
        """
        result1 = get_access_token()
        result2 = get_access_token()
        self.assertEqual(result1['access_token'], result2['access_token'], 
                        "Second call should return cached token")
        print("[TEST] 토큰 캐싱 동작 확인!")

    def test_get_current_price(self):
        """
        get_current_price 함수가 삼성전자(005930) 현재가를 반환하는지 테스트
        """
        result = get_current_price("005930")
        self.assertIsNotNone(result, "get_current_price() should not return None")
        self.assertIn("stck_prpr", result, "Response should contain 'stck_prpr' (현재가)")
        print(f"[TEST] 삼성전자 현재가: {result.get('stck_prpr')}원")
