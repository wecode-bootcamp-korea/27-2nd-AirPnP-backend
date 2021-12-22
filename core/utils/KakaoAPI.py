import json, bcrypt, jwt, requests

from django.http                import JsonResponse

class KakaoAPI:
   def __init__(self, access_token):
        self.access_token = access_token
        self.user_url     = "https://kapi.kakao.com/v2/user/me?secure_resource=true&property_keys=%5B%22properties.nickname%22%2C%22kakao_account.email%22%5D"
        
    def get_kakao_user(self):
        try :
            headers  = {"Authorization" : f"Bearer ${self.access_token}"}
            response = requests.get(self.user_url, headers = headers, timeout = 3)
            if not kakao_response.status_code == 200:
                raise Exception("INVALID KAKAO USER")

            return response.json()

        except requests.Timeout:
            return JsonResponse({"message" :'TIMEOUT'}, status = 408)
