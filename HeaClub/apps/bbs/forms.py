# -*- coding: utf-8 -*-
from django import forms


class AddTieForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True)



class CommentForm(forms.Form):
    content = forms.CharField(required=True)