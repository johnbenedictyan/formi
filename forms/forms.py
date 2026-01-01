from django import forms

from .models import Formi


class FormiForm(forms.ModelForm):
    class Meta:
        model = Formi
        fields = ("title",)
