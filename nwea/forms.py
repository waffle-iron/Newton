from django import forms
from django.core import validators
from . import models


class InputNWEAScores(forms.ModelForm):
    class Meta:
        model = models.NWEAScore
        fields = [
            "student",
            "year",
            "season",
            "subdomain1",
            "subdomain2",
            "subdomain3",
            "subdomain4",
            "subdomain5",
            "subdomain6",
            "subdomain7",
            "subdomain8",
        ]
