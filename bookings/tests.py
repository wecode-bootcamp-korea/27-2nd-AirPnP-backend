import json
import uuid

from datetime import datetime

from categories.models import Category
from .models import Booking
from users.models import User, Host

from django.test import TestCase, Client


class BookingTest(TestCase) :
    def setUp(self) :
        bulk_list = []
        for i in range(5) :
            talent = "talent %s" %i
            id = 1+i
            bulk_list.append(Category(talent=talent, id= id))

        Category.objects.bulk_create(bulk_list)

        User.objects.create(
            id       = 1,
            name     = "user1",
            email    = "user1@hello.com",
            kakao_id = "user1"
        )
        User.objects.create(
            id       = 2,
            name     = "user2",
            email    = "user2@hello.com",
            kakao_id = "user2"
        )

        Host.objects.create(
            id                = 1,
            phone_number      = "010",
            career            = 1,
            price             = 5000,
            job               = "job1",
            title             = "title1",
            subtitle          = "subtitle1",
            description       = "description1",
            longitude         = 1,
            latitude          = 1,
            address           = "address1",
            local_description = "local_descripion1",
            category_id       = 1,
            user_id           = 1,
        )

        Booking.objects.create(
            booking_number = uuid.uuid4(),
            start_date     = datetime.strptime("2021-12-18", "%Y-%m-%d"),
            end_date       = datetime.strptime("2021-12-18", "%Y-%m-%d"),
            total_price    = 5000,
            host_id        = 1,
            user_id        = 2
        )
        Booking.objects.create(
            booking_number = uuid.uuid4(),
            start_date     = datetime.strptime("2021-12-19", "%Y-%m-%d"),
            end_date       = datetime.strptime("2021-12-20", "%Y-%m-%d"),
            total_price    = 5000,
            host_id        = 1,
            user_id        = 2
        )
        Booking.objects.create(
            booking_number = uuid.uuid4(),
            start_date     = datetime.strptime("2021-12-22", "%Y-%m-%d"),
            end_date       = datetime.strptime("2021-12-25", "%Y-%m-%d"),
            total_price    = 5000,
            host_id        = 1,
            user_id        = 2
        )

    def tearDown(self) :
        Host.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

    def test_bookingview_post_success(self) :
        client =Client()

        booking = {
            'start_date' : '2021-12-21',
            'end_date'   : '2021-12-21',
            'host_id'    : 1,
            'user_id'    : 2,
            'total_price': 5000
        }
        response = client.post('/bookings', json.dumps(booking), content_type='application/json')

        self.assertEqual(response.status_code, 200)
    
    def test_bookingview_booking_before_today(self) :
        client = Client()

        booking = {
            'start_date' : '2021-12-18',
            'end_date'   : '2021-12-18',
            'host_id'    : 1,
            'user_id'    : 2,
            'total_price': 5000
        }
        response = client.post('/bookings', json.dumps(booking), content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'ERROR' : 'NO_WAY_TO_BOOK_BEFORE_TODAY'})

    def test_bookingview_impossible_booking(self) :
        client = Client()

        booking = {
            'start_date' : '2021-12-21',
            'end_date'   : '2021-12-20',
            'host_id'    : 1,
            'user_id'    : 2,
            'total_price': 5000
        }
        response = client.post('/bookings', json.dumps(booking), content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'ERROR' : 'IMPOSSIBLE_BOOKING_DATE'})

    def test_bookingview_already_booked(self) :
        client = Client()

        booking = {
            'start_date' : '2021-12-20',
            'end_date'   : '2021-12-22',
            'host_id'    : 1,
            'user_id'    : 2,
            'total_price': 5000
        }
        response = client.post('/bookings', json.dumps(booking), content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'ERROR' : 'ALREADY_BOOKED'})

    def test_bookingview_key_error(self) :
        client = Client()

        booking = {
            'date'       : '2021-12-21',
            'end_date'   : '2021-12-21',
            'host_id'    : 1,
            'user_id'    : 2,
            'total_price': 5000
        }
        response = client.post('/bookings', json.dumps(booking), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSGE" :"KEY_ERROR"})