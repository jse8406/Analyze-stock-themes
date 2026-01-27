
from django.test import TestCase
from .kis_auth import get_access_token, get_approval_key
import unittest
from unittest.mock import patch
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


    @patch('auth.kis_auth.requests.post')
    def test_get_approval_key_failure(self, mock_post):
        """
        [Edge Case] approval_key 발급 요청 실패 시 None 반환 테스트
        """
        # Mocking a failed response (e.g., 500 Server Error)
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = get_approval_key()
        self.assertIsNone(result, "Should return None on API failure")
        print("[TEST] Approval Key 발급 실패 처리 확인완료")

    @patch('auth.kis_auth.requests.post')
    def test_get_approval_key_exception(self, mock_post):
        """
        [Edge Case] approval_key 발급 중 예외 발생 시 None 반환 테스트
        """
        mock_post.side_effect = Exception("Network Error")
        
        result = get_approval_key()
        self.assertIsNone(result, "Should return None on Exception")
        print("[TEST] Approval Key 예외 처리 확인완료")

    @patch('auth.kis_auth.requests.post')
    def test_get_access_token_failure(self, mock_post):
        """
        [Edge Case] access_token 발급 요청 실패 시 None 반환 테스트
        """
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        # force_refresh=True to bypass cache and hit the mock
        result = get_access_token(force_refresh=True)
        self.assertIsNone(result, "Should return None on API failure")
        print("[TEST] Access Token 발급 실패 처리 확인완료")
