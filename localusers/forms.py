from django import forms
from .models import LocalUser


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=56,required=False)
    last_name = forms.CharField(max_length=56,required=False)
    bio = forms.CharField(widget=forms.Textarea,max_length=1012)
    avatar = forms.ImageField(required=False)
    class Meta:
        model = LocalUser
        fields = ('first_name','last_name','bio','avatar')
