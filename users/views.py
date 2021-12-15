import json, bcrypt, jwt

from my_settings                import ALGORITHM, SECRET_KEY

from django.http                import JsonResponse, response
from django.views               import View
from django.core.exceptions     import ValidationError
from core.utils.KakaoAPI        import KakaoAPI
from users.models               import User


class KakaoLoginView(View):
    def post(self, request):
        try:
            kakao_access_token = request.headers['Authorization']
            kakao              = KakaoAPI(kakao_access_token)
            
            kakao_response = kakao.get_kakao_user()

            if kakao_response.get('code') == -401:
                return JsonResponse({'message': 'INVALID KAKAO USER'}, status=400)

            kakao_id   = kakao_response['id']
            email      = kakao_response['kakao_account']["email"]
            name       = kakao_response['properties']["nickname"]
            
            user, created = User.objects.get_or_create(
                kakao_id = kakao_id,
                defaults = {
                    'name'  : name,
                    'email' : email,
                }
            )
            user.save()

            token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS', 'token' : token}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)