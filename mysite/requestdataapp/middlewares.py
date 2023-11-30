from django.http import HttpRequest, HttpResponse
from datetime import datetime


class Throttling_Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_data = {}

    def __call__(self, request: HttpRequest):
        user_id = request.META['REMOTE_ADDR']
        current_datetime = datetime.now()
        last_time_update = self.user_data.get(user_id)
        self.user_data[user_id] = current_datetime
        if last_time_update and (current_datetime - last_time_update).seconds < 2:
            print(f"User {user_id} makes too frequent requests")
            return HttpResponse('Too frequent requests, wait a little, please!')
        else:
            response = self.get_response(request)
            return response



