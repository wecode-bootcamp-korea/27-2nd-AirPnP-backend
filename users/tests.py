import json, jwt, bcrypt, unittest
import re

from django.http        import response
from .models            import User, Host, Image
from categories.models  import Category
from bookings.models    import Booking
from my_settings        import ALGORITHM, SECRET_KEY

from django.test        import TestCase, Client
from unittest           import mock
from unittest.mock      import patch


class SignInTest(TestCase):
    @patch("core.utils.KakaoAPI.requests")
    def test_kakao_signin_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            status_code = 200
            
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
        print(MockedResponse().__dir__()) 
        headers             = {"HTTP_Authorization" : "access_token"}
        response            = client.post("/users/signin", **headers)

        self.assertEqual(response.status_code, 201)

class HostListTest(TestCase):
    def setUp(self):
        self.client = Client()

        Category.objects.create(
            id        = 1,
            talent    = 'a'
        )

        Category.objects.create(
            id        = 2,
            talent    = 'b'
        )

        Category.objects.create(
            id        = 3,
            talent    = 'c'
        )

        User.objects.create(
            id        = 1,
            name      = 'a',
            email     = 'a',
            kakao_id  = 'a'
        )

        User.objects.create(
            id        = 2,
            name      = 'b',
            email     = 'b',
            kakao_id  = 'b'
        )

        User.objects.create(
            id        = 3,
            name      = 'c',
            email     = 'c',
            kakao_id  = 'c'
        )
        
        Host.objects.create(
            id                = 1,
            phone_number      = 'a',
            career            = 1,
            price             = 1,
            title             = 'a',
            subtitle          = 'a',
            description       = 'a',
            longitude         = 1.000000,
            latitude          = 1.000000,
            address           = 'a',
            local_description = 'a',
            category          = Category.objects.get(id=1),
            user              = User.objects.get(id=1)
        )

        Host.objects.create(
            id                = 2,
            phone_number      = 'b',
            career            = 2,
            price             = 2,
            title             = 'b',
            subtitle          = 'b',
            description       = 'b',
            longitude         = 2.000000,
            latitude          = 2.000000,
            address           = 'b',
            local_description = 'b',
            category          = Category.objects.get(id=2),
            user              = User.objects.get(id=2)
        )

        Host.objects.create(
            id                = 3,
            phone_number      = 'c',
            career            = 3,
            price             = 3,
            title             = 'c',
            subtitle          = 'c',
            description       = 'c',
            longitude         = 3.000000,
            latitude          = 3.000000,
            address           = 'c',
            local_description = 'c',
            category          = Category.objects.get(id=3),
            user              = User.objects.get(id=3)
        )

        Image.objects.create(
            id        = 1,
            image_url = 'a',
            host      = Host.objects.get(id=1)
        )

        Image.objects.create(
            id        = 2,
            image_url = 'b',
            host      = Host.objects.get(id=2)
        )

        Image.objects.create(
            id        = 3,
            image_url = 'c',
            host      = Host.objects.get(id=3)
        )

        Booking.objects.create(
            id             = 1,
            booking_number = 1,
            start_date     = '2021-12-22',
            end_date       = '2021-12-23',
            total_price    = 1,
            host           = Host.objects.get(id=1),
            user           = User.objects.get(id=1)
        )
      
    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Category.objects.all().delete()
        Booking.objects.all().delete()

    def test_hostlist_get_success_with_category(self):
        response = self.client.get('/users/hosts?start_longitude=0&end_longitude=20&start_latitude=0&end_latitude=20&category=a')
        self.assertEqual(response.json(),
            {
                'MESSAGE': 'SUCCESS',
                "RESULT" : [{
                    'host_id'      : 1,
                    'category'     : 'a',
                    'name'         : 'a',
                    'price'        : 1,
                    'description'  : 'a',
                    'longitude'    : 1.000000,
                    'latitude'     : 1.000000,
                    'address'      : 'a',
                    'images'       : ['a'],
                    'start_date'   : '',
                    'end_date'     : ''
                }]
                         
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_hostlist_get_success_with_date(self):
        response = self.client.get('/users/hosts?start_longitude=0&end_longitude=20&start_latitude=0&end_latitude=20&start_date=2021-12-23&end_date=2021-12-25')
        self.assertEqual(response.json(),
            {
                'MESSAGE': 'SUCCESS',
                "RESULT" : [
                    {
                        'host_id'      : 2,
                        'category'     : 'b',
                        'name'         : 'b',
                        'price'        : 2,
                        'description'  : 'b',
                        'longitude'    : 2.000000,
                        'latitude'     : 2.000000,
                        'address'      : 'b',
                        'images'       : ['b'],
                        'start_date'   : '2021-12-23',
                        'end_date'     : '2021-12-25'
                    },
                    {
                        'host_id'      : 3,
                        'category'     : 'c',
                        'name'         : 'c',
                        'price'        : 3,
                        'description'  : 'c',
                        'longitude'    : 3.000000,
                        'latitude'     : 3.000000,
                        'address'      : 'c',
                        'images'       : ['c'],
                        'start_date'   : '2021-12-23',
                        'end_date'     : '2021-12-25'
                    }
                ]
                         
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_hostlist_get_success_with_category_and_date(self):
        response = self.client.get('/users/hosts?start_longitude=0&end_longitude=20&start_latitude=0&end_latitude=20&category=c&start_date=2021-12-23&end_date=2021-12-25')
        self.assertEqual(response.json(),
            {
                'MESSAGE': 'SUCCESS',
                "RESULT" : [{
                    'host_id'      : 3,
                    'category'     : 'c',
                    'name'         : 'c',
                    'price'        : 3,
                    'description'  : 'c',
                    'longitude'    : 3.000000,
                    'latitude'     : 3.000000,
                    'address'      : 'c',
                    'images'       : ['c'],
                    'start_date'   : '2021-12-23',
                    'end_date'     : '2021-12-25'
                }]
                        
            }
        )
        self.assertEqual(response.status_code, 200)
        
class HostViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(
            id       = 1,
            name     = '김은혜',
            email    = 'lilo@gmail.com',
            kakao_id = '203331446'
        )

        User.objects.create(
            id       = 2,
            name     = '여희동',
            email    = 'alex@gmail.com',
            kakao_id = '203331447'
        )

        Category.objects.create(
            id = 1,
            talent = "Musician"
        )

        Category.objects.create(
            id = 2,
            talent = "Actor"
        )

        Host.objects.create(
            id                = 1,
            phone_number      = '01052085188',
            user              = User.objects.get(id=1),
            career            = 3,
            price             = 10000,
            title             = 'hello',
            subtitle          = 'hello',
            description       = 'hello',
            local_description = 'hello',
            longitude         = 1.00,
            latitude          = 2.00,
            address           = '서울시 강남구 대치동',
            category          = Category.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete(),
        Category.objects.all().delete(),
        Host.objects.all().delete()
        
    def test_hostview_post_success(self):
        client = Client()
        
        host   = {
            'phone_number'     : '01052085188',
            'user_id'          : 1,
            'career'           : 3,
            'price'            : 10000,
            'title'            : 'hello',
            'subtitle'         : 'hello',
            'description'      : 'hello',
            'local_description': 'hello',
            'longitude'        : 1.00,
            'latitude'         : 2.00,
            'address'          : '서울시 강남구 대치동',
            'category'         : 'Actor'
        }
        
        access_token = jwt.encode({'id': 1}, SECRET_KEY, ALGORITHM)
        headers = {"HTTP_Authorization" : access_token}
        response = client.post('/users/host', json.dumps(host), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'result' : 'CREATED'
            }
        )

    def test_hostview_post_exist_category(self):
        client = Client()

        host   = {
            'phone_number'     : '01052085188',
            'user_id'          : 1,
            'career'           : 3,
            'price'            : 10000,
            'title'            : 'hello',
            'subtitle'         : 'hello',
            'description'      : 'hello',
            'local_description': 'hello',
            'longitude'        : 1.00,
            'latitude'         : 2.00,
            'address'          : '서울시 강남구 대치동',
            'category'         : 'Musician'
        }

        access_token = jwt.encode({'id': 1}, SECRET_KEY, ALGORITHM)
        headers  = {"HTTP_Authorization" : access_token}
        response = client.post('/users/host', json.dumps(host), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'result' : 'Registered Category'
            }
        )

    def test_hostview_post_invalid_token(self):
        client = Client()

        host   = {
            'phone_number'     : '01052085188',
            'user_id'          : 3,
            'career'           : 3,
            'price'            : 10000,
            'title'            : 'hello',
            'subtitle'         : 'hello',
            'description'      : 'hello',
            'local_description': 'hello',
            'longitude'        : 1.00,
            'latitude'         : 2.00,
            'address'          : '서울시 강남구 대치동',
            'category'         : 'Musician'
        }

        headers = {"HTTP_Authorization" : "access_token"}
        response = client.post('/users/host', json.dumps(host), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_TOKEN'
            }
        )

class HostDetailTest(TestCase):
    def setUp(self):
        self.client = Client()

        Category.objects.create(
            id        = 1,
            talent    = 'a'
        ) 

        User.objects.create(
            id        = 1,
            name      = 'a',
            email     = 'a',
            kakao_id  = 'a'
        )

        Host.objects.create(
            id                = 1,
            phone_number      = 'a',
            career            = 1,
            price             = 1,
            title             = 'a',
            subtitle          = 'a',
            description       = 'a',
            longitude         = 1.000000,
            latitude          = 1.000000,
            address           = 'a',
            local_description = 'a',
            category          = Category.objects.get(id=1),
            user              = User.objects.get(id=1)
        )

        Image.objects.create(
            id        = 1,
            image_url = 'a',
            host      = Host.objects.get(id=1)
        )

        Booking.objects.create(
            id             = 1,
            booking_number = 1,
            start_date     = '2021-12-22',
            end_date       = '2021-12-23',
            total_price    = 1,
            host           = Host.objects.get(id=1),
            user           = User.objects.get(id=1)
        )

        Booking.objects.create(
            id             = 2,
            booking_number = 2,
            start_date     = '2021-12-27',
            end_date       = '2021-12-29',
            total_price    = 2,
            host           = Host.objects.get(id=1),
            user           = User.objects.get(id=1)
        )
    
    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Category.objects.all().delete()
        Booking.objects.all().delete()
        
    def test_hostdetail_get_success(self):
        response = self.client.get('/users/hosts/detail/1?start_date=2021-12-06&end_date=2021-12-10')
        self.assertEqual(response.json(),
            {
                'MESSAGE': 'SUCCESS',
                "RESULT" : {
                    'category'          : 'a',
                    'host_name'         : 'a',
                    'career'            : 1,
                    'price'             : 1,
                    'description'       : 'a',
                    'longitude'         : 1.000000,   
                    'latitude'          : 1.000000,
                    'title'             : 'a',
                    'subtitle'          : 'a',
                    'address'           : 'a',
                    'local_description' : 'a',   
                    'booking_date'      : [
                        {
                            'start_date' : '2021-12-22',
                            'end_date'   : '2021-12-23'
                        },
                        {
                            'start_date' : '2021-12-27',
                            'end_date'   : '2021-12-29'
                        }
                    ],
                    'images'            : ['a'],
                    'start_date'        : '2021-12-06',
                    'end_date'          : '2021-12-10'
                }
            }
        )
        self.assertEqual(response.status_code, 200)
