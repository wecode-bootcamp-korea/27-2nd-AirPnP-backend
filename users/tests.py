import json, bcrypt, unittest

from django.http        import response
from .models            import User
from django.test        import TestCase, Client
from unittest           import mock
from unittest.mock      import patch


class SignInTest(TestCase):
    @patch("core.utils.KakaoAPI.requests")
    def test_kakao_signin_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:     
            def json(self):
                return {
                    "id": 2033314461,
                    "connected_at": "2021-12-14T09:03:16Z",
                    "properties": {
                        "nickname": "김은혜"
                    },
                    "kakao_account": {
                        "has_email": True,
                        "email_needs_agreement": False,
                        "is_email_valid": True,
                        "is_email_verified": True,
                        "email": "jino63@naver.com"
                    }
                }       
                
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "access_token"}
        response            = client.post("/users/signin", **headers)

        self.assertEqual(response.status_code, 201)
