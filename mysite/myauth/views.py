from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


class MyLogoutView(LogoutView):
    next_page = '/admin/'


def cookies_get(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('cookie_value', 'default_value')
    return HttpResponse(f'Cookie value: {value!r}')


def cookies_set(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookies value set!')
    response.set_cookie('cookie_value', 'rabbit', max_age=3600)
    return response


def session_set(request: HttpRequest) -> HttpResponse:
    request.session['session_value'] = "Christmas soon!"
    return HttpResponse('Session value set!')


def session_get(request: HttpRequest) -> HttpResponse:
    value = request.session.get('session_value', 'Value is not set yet!')
    return HttpResponse(f'Session value: {value}')