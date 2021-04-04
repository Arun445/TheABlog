from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django import forms


from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmailChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']



class ProfileChangeForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        fields = ['user_image', 'about']
        labels = {
            'user_image': 'My profile picture',
            'about': 'About me'
                  }

#Method to change field to be not required

#    def __init__(self, *args, **kwargs):
#       super(ProfileChangeForm, self).__init__(*args, **kwargs)
#       self.fields['about'].required = False





