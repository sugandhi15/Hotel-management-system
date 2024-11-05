from django import forms
from django_recaptcha.fields import ReCaptchaField
from .models import User


class SignupForm(forms.Form):
    captcha = ReCaptchaField()  

    class Meta:
        model = User
        fields = "__all__"