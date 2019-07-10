from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import make_title
from django.utils.text import slugify
import requests


class BookmarkManager(models.Manager):
    def deleted(self,user):
        return user.bookmarks.filter(deleted_at__isnull=False)

    def current(self,user):
        return user.bookmarks.filter(deleted_at__isnull=True)



class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name='bookmarks'
                        )
    url = models.URLField()
    title = models.CharField(max_length=255,default='',blank=True)
    description = models.TextField(default='',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    collections = models.ManyToManyField('Collection',related_name='bm_collect')

    objects = BookmarkManager()
    tags = TaggableManager()

    def __str__(self):
        if self.title:
            return self.title
        else:
            self.title = str(self.url)[:24]
        return self.title
    def get_absolute_url(self):
        return reverse('my_bookmarks:bookmark_detail.html',kwargs={'pk':self.pk})
    class Meta:
        unique_together = ('user','url')

class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='collections')
    name = models.CharField(max_length=124)
    slug = models.SlugField()

    class Meta:
        unique_together = ('user','slug')

    def __str__(self):
        return "{}'s collection: {} ".format(self.user,self.slug)

    def save(self,*args,**kwargs):
        """
        each time obj saved ==> each time will be checked for the name
        and updeated accordingly
        """
        self.slug = slugify(self.name)[:50]
        super().save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse('collection:detail',kwargs={'slug':self.slug})    




@receiver(post_save,sender=Bookmark)
def fetch_url_title(sender,instance,created,**kwargs):
    if created:
        response = requests.get(instance.url)
        if response.ok:
            text = response.text[:255]
            instance.title = make_title(text)
            instance.save()
        else:
            print('resp status is not ok')
