from django.contrib import admin
from .models import Bookmark,Collection
#prepopulated_fields doesn’t accept DateTimeField, ForeignKey, OneToOneField, and #ManyToManyField fields.
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['title','url','user']
    filter_horizontal = ['collections']
    # filter_vertical = ['collections']

class CollectionAdmin(admin.ModelAdmin):
    list_display =['name','slug','id']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Collection,CollectionAdmin)
admin.site.register(Bookmark,BookmarkAdmin)
# instead:
# @admin.register(models.Bookmark)
# class BookmarkAdmin(admin.ModelAdmin):
#     list_display = ['title','url','user']
