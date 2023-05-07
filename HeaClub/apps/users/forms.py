# -*- coding: utf-8 -*-
#字段验证
from django import forms

from users.models import UserMessage


class LoginForm(forms.Form):

    username=forms.CharField(required=True)
    password=forms.CharField(required=True)

class RegisterForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True)

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['username', 'sex', 'birthday', 'address', 'mobile']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['image']


