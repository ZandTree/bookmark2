from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,UpdateView,DeleteView
from .forms import ProfileForm
from .models import LocalUser


class Profile(LoginRequiredMixin,DetailView):
    model = LocalUser #settings.AUTH_USER_MODEL ?????????
    template_name = 'localusers/profile.html'

    def get_object(self,queryset=None):
        return self.request.user

class UpdateProfile(LoginRequiredMixin,UpdateView):
    model = LocalUser
    form_class = ProfileForm
    template_name = 'localusers/edit_profile.html'

    def get_object(self,queryset=None):
        return self.request.user

class DeleteProfile(LoginRequiredMixin,DeleteView):
    model = LocalUser
    success_url = reverse_lazy('my_bookmarks:list')
    def get_object(self,queryset=None):
        return self.request.user
