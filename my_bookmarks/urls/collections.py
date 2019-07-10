from django.urls import path,re_path
from ..views import collections as views

# app_name='my_bookmarks'
app_name='collection'


urlpatterns = [
    path('create-collection/',views.Create.as_view(),name='create-collection'),
    path('collection-detail/<slug:slug>/',views.CollectionDetail.as_view(),name='detail'),
    path('all-collections/',views.ListCollections.as_view(),name='all-collections'),



]
