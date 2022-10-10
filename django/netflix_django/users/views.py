from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/user_form.html'

    def get_success_url(self):
        print("회원가입 성공")
        return reverse('movie-list')