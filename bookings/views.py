import json

from django.views import View
from django.db.models import Q
from django.http.response import JsonResponse

from datetime import datetime
from .models import Booking

class BookingView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            host_id     = data['host_id']
            user_id     = data['user_id']
            start_date  = datetime.strptime(data['start_date'], "%Y-%m-%d")
            end_date    = datetime.strptime(data['end_date'], "%Y-%m-%d")
            total_price = data['total_price']

            if start_date < datetime.strptime((datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") :
                return JsonResponse({'ERROR' : 'NO_WAY_TO_BOOK_BEFORE_TODAY'}, status=403)

            if end_date < start_date :
                return JsonResponse({'ERROR' : 'IMPOSSIBLE_BOOKING_DATE'}, status=403)
                
            if Booking.objects.filter(Q(host_id=host_id) & Q(start_date__range= [ start_date, end_date]) | Q(end_date__range=[start_date, end_date])) :
                return JsonResponse({'ERROR' : 'ALREADY_BOOKED'}, status=403)

            booking = Booking.objects.create(
                user_id     = user_id,
                host_id     = host_id,
                start_date  = start_date,
                end_date    = end_date,
                total_price = total_price
            )
            return JsonResponse({"예약 성공" : booking.booking_number}, status= 200)
            
        except KeyError :
            return JsonResponse({"MESSGE" :"KEY_ERROR"}, status= 400)