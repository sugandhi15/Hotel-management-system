from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User
from django_recaptcha.fields import ReCaptchaField


class SignupForm(forms.Form):
    captcha = ReCaptchaField()  

    # class Meta:
    #     model = User
    #     fields = '__all__'