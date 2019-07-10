from django.urls import path
from .views import Profile,UpdateProfile,DeleteProfile

app_name='localusers'
urlpatterns = [
    path('<int:pk>/',Profile.as_view(),name='profile'),
    path('edit/<int:pk>/',UpdateProfile.as_view(),name='edit-profile'),
    path('delete/<int:pk>/',DeleteProfile.as_view(),name='delete-profile'),
]
