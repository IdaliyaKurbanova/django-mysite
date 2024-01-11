from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from .forms import OnlyAvatarForm
from django.contrib.auth.models import User
from myauth.models import Profile


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        user = authenticate(request=self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response


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


class ProfileDetailView(DetailView):
    model = Profile


class UserListView(ListView):
    template_name = 'myauth/user_list.html'
    queryset = User.objects.select_related('profile')


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = 'avatar', 'bio'

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.is_staff or self.request.user.profile == self.object

    def get_success_url(self):
        return reverse('myauth:profile_detail', kwargs={'pk': self.object.pk})


def about_me(request: HttpRequest):
    if request.method == 'POST' and request.FILES['avatar']:
        form = OnlyAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
    form = OnlyAvatarForm()
    context = {'form': form}
    return render(request, 'myauth/about_me.html', context=context)







