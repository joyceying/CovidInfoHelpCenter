from HelpCenter import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from HelpCenter.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.User
        fields = ["name", "password"]



