from django.urls import path,re_path
from ..views import bookmarks as views

# app_name='my_bookmarks'
app_name = 'my_bookmarks'
urlpatterns = [
    re_path(r'^(?:t:(?P<tag>[-\w]+)/)?$',views.ListBookmarks.as_view(),name='list'),
    path('create-bookmark/',views.CreateBookmark.as_view(),name='create'),
    path('edit-bookmark/<int:pk>/',views.UpdateBookmark.as_view(),name='edit'),
    path('delete/<int:pk>/',views.SoftDeleteBookmark.as_view(),name='soft-delete'),
    path('trash/',views.Trash.as_view(),name='trash'),
    path('restore/<int:pk>/',views.Restore.as_view(),name='restore'),
    path('search/',views.Search.as_view(),name='search'),
    path('final-delete/<int:pk>/',views.FinalTrash.as_view(),name='final_del'),
    # re_path(r'^t:(?P<tag>[-\w]+)/$',Search.as_view(),name='tag-search'),
    path('add-to-collection/',views.AddBookmarkToCollection.as_view(),name='add-to-collect'),

]
