from django.contrib.auth.views import LoginView
from django.urls import path

from myauth.views import MyLogoutView, cookies_set, cookies_get, session_set, session_get, RegistrationView

app_name = 'myauth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/',
         MyLogoutView.as_view(),
         name='logout'),
    path('register/',
         RegistrationView.as_view(), name='registration'),
    path('cookies-set/',
         cookies_set,
         name='cookies_set'),
    path('cookies-get/',
         cookies_get,
         name='cookies_get'),
    path('session-set/',
         session_set,
         name='session_set'),
    path('session-get/',
         session_get,
         name='session_get'),
]

