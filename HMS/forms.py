from django import forms
from django_recaptcha.fields import ReCaptchaField


class SignupForm(forms.Form):
    captcha = ReCaptchaField()  
