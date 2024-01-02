from django.contrib.auth.views import LoginView
from django.urls import path

from myauth.views import (MyLogoutView, cookies_set, cookies_get,
                          session_set, session_get, RegistrationView,
                          ProfileDetailView, UserListView, ProfileUpdateView,
                          about_me)

app_name = 'myauth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/',
         MyLogoutView.as_view(),
         name='logout'),
    path('about-me/',
         about_me,
         name='about_me'),
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
    path('profiles/',
         UserListView.as_view(),
         name='profile_list'),
    path('profiles/<int:pk>/',
         ProfileDetailView.as_view(),
         name='profile_detail'),
    path('profiles/<int:pk>/update/',
         ProfileUpdateView.as_view(),
         name='profile_update')
]

