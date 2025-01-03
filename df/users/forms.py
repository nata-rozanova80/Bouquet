# users/forms.py
from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # Cюда? добавить поле для телеграм?

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
