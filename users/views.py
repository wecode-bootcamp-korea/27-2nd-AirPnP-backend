import json, bcrypt, jwt, boto3, functools, random
from datetime                   import datetime

from my_settings                import ALGORITHM, SECRET_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, IMAGE_URL

from geopy.geocoders            import Nominatim
from decimal                    import Decimal
from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q

from core.utils.KakaoAPI        import KakaoAPI
from core.utils.decorator       import signin_decorator
from core.utils.imageHandler import ImageHandler

from users.models               import User, Image, Host
from categories.models          import Category

class KakaoLoginView(View):
    def post(self, request):
        try:
            kakao_access_token = request.headers['Authorization']
            kakao_api          = KakaoAPI(kakao_access_token)
            kakao_user         = kakao_api.get_kakao_user()
            
            user, created = User.objects.get_or_create(
                kakao_id  = kakao_user['id'],
                defaults  = {
                    'name'  : kakao_user['properties']["nickname"],
                    'email' : kakao_user['kakao_account']["email"],
                }
            )

            token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS', 'token' : token}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

boto3_resource = boto3.resource(
                's3',
                aws_access_key_id     = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )
            
class ImageUploader(View) :
    def post(self, request) :
            files = request.FILES.getlist('files')
            host_id = request.GET.get('host_id')
            
            image_handler = ImageHandler(boto3_resource, AWS_STORAGE_BUCKET_NAME, IMAGE_URL)

            urls = image_handler.upload_files(files, host_id)

            Image.objects.bulk_create([Image(image_url = url, host_id = host_id) for url in urls])

            return JsonResponse({"MESSGE" : "SUCCESS"}, status=200)

class HostListView(View):
    def get(self, request):
        category        = request.GET.get('category', '')
        start_date      = request.GET.get('start_date', '')
        end_date        = request.GET.get('end_date', '')
        start_longitude = request.GET.get('start_longitude', '')
        end_longitude   = request.GET.get('end_longitude', '')
        start_latitude  = request.GET.get('start_latitude', '')
        end_latitude    = request.GET.get('end_latitude', '')
        
        exclude_set = {
            "start_date" : Q(booking__start_date__lte=start_date) & Q(booking__end_date__gte=start_date),
            "end_date"   : Q(booking__start_date__lte=end_date) & Q(booking__end_date__gte=end_date)
        }

        FILTER_SET = {
            "start_longitude" : Q(longitude__lte=end_longitude),
            "end_longitude"   : Q(longitude__gte=start_longitude),
            "start_latitude"  : Q(latitude__lte=end_latitude),
            "end_latitude"    : Q(latitude__gte=start_latitude),
            "category"        : Q(category__talent=category)
        }

        if category =="" :
             hosts = Host.objects.all()
        else :
            f = functools.reduce(lambda q1, q2 : q1&q2, [FILTER_SET.get(key, Q()) for key in request.GET.keys()])
            e = functools.reduce(lambda q1, q2 : q1|q2, [exclude_set.get(key, Q()) for key in request.GET.keys()])
            hosts = Host.objects.filter(f).exclude(e)

        results = [{
            'host_id'    : host.id,
            'category'   : host.category.talent,
            'name'       : host.user.name,
            'price'      : host.price,
            'description': host.description,
            'longitude'  : float(host.longitude),
            'latitude'   : float(host.latitude),
            'address'    : host.address,
            'images'     : list(host.image_set.values()),
            'start_date' : start_date,
            'end_date'   : end_date
        } for host in hosts]

        random.shuffle(results)

        return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': results}, status=200)

class HostView(View):
    @signin_decorator
    def post(self, request):
        try : 
            user     = request.user
            data     = json.loads(request.body)
            category = Category.objects.get(talent = data["category"])

            if Host.objects.filter(category = category, user=user).exists():
                return JsonResponse({'result':'Registered Category'}, status = 400)
            
            address       = data["address"]
            location      = Nominatim(user_agent="Users")
            host_location = location.geocode(address)

            host = Host.objects.create(
                    phone_number      = data['phone_number'],
                    user              = user,
                    career            = data['career'],
                    price             = data['price'],
                    title             = data['title'],
                    subtitle          = data['subtitle'],
                    description       = data['description'],
                    local_description = data['local_description'],
                    longitude         = Decimal(host_location.longitude),
                    latitude          = Decimal(host_location.latitude),
                    address           = address,
                    category          = category
            )    

            return JsonResponse({'result' : 'CREATED', 'host_id' : host.id}, status = 201)

        except KeyError:
            return JsonResponse({'message' : "KEYERROER"}, status = 400)
        except Category.DoesNotExist :
            return JsonResponse({'message' : "DOSENOTEXIST"}, status = 401)
      
class HostDetailView(View):
    def get(self, request, host_id):
        try: 
            host       = Host.objects.prefetch_related('image_set', 'booking_set').get(id=host_id)
            start_date = request.GET.get('start_date', '')
            end_date   = request.GET.get('end_date', '')

            result = {
                'category'         : host.category.talent,
                'host_name'        : host.user.name,
                'career'           : host.career,
                'price'            : host.price,
                'description'      : host.description,
                'longitude'        : float(host.longitude),
                'latitude'         : float(host.latitude),
                'title'            : host.title,
                'subtitle'         : host.subtitle,
                'address'          : host.address,
                'local_description': host.local_description,
                'booking_date'     : [{
                    'start_date': datetime.strftime(booking.start_date, '%Y-%m-%d'),
                    'end_date'  : datetime.strftime(booking.end_date, '%Y-%m-%d')
                } for booking in host.booking_set.all()],
                'images'    : list(host.image_set.values()),
                'start_date': start_date,
                'end_date'  : end_date
            }

            return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)

        except Host.DoesNotExist:
            return JsonResponse({"MESSAGE": "HOST_DOES_NOT_EXISTS"},status = 404)
