import json, bcrypt, jwt, boto3, uuid

from my_settings                import ALGORITHM, SECRET_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, IMAGE_URL

from django.http                import JsonResponse, response
from django.views               import View
from django.core.exceptions     import ValidationError
from core.utils.KakaoAPI        import KakaoAPI
from users.models               import User, Image


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

class ImageUploader(View) :
    
    def post(self, request) :
        try :
            files = request.FILES.getlist('files')
            host_id = request.GET.get('host_id')
            s3r = boto3.resource('s3', aws_access_key_id= AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
            key = "%s" %(host_id)

            for file in files :
                file._set_name(str(uuid.uuid4()))
                s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object( Key=key+'/%s'%(file), Body=file, ContentType='jpg')
                Image.objects.create(
                    image_url = IMAGE_URL+"%s/%s"%(host_id, file),
                    host_id = host_id
                )
            return JsonResponse({"MESSGE" : "SUCCESS"}, status=200)

        except Exception as e :
            return JsonResponse({"ERROR" : e.message})
