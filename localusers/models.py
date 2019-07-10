from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from django.utils import timezone
import os

def upload_avatar(instance,file):
    """
    formatting file name:
    media/pict/user_id/filename_year-month-day.extention
    """
    time = timezone.now().strftime('%Y-%m-%d')
    tail = file.split('.')[-1]
    head = file.split('.')[0]
    if len(head)>15:
        head = head[:15]
    file_name = head +'_'+time+'.'+tail
    return os.path.join('avatars','user_{0}','{1}').format(instance.id,file_name)


class LocalUser(AbstractUser):
    bio = models.TextField(default="")
    avatar = models.ImageField(blank=True,upload_to=upload_avatar)


    def save(self,*args,**kwargs):

        super().save(*args,**kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height >300 or img.width >300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


    @property
    def get_avatar_url(self,*args,**kwargs):
        if self.avatar:
            return '/media/{}'.format(self.avatar)
        else:
            return  '/static/img/default_cat.png'
    def get_absolute_url(self):
        return reverse('localusers:profile',kwargs={'pk':self.id})

    def __str__(self):
        return self.username
    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name+' '+self.last_name
        else:
            return self.username            
