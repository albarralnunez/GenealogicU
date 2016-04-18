from django import forms
from django.forms.extras.widgets import SelectDateWidget
import account.forms
import re


alnum_re = re.compile(r"^\w+$")


class SignupForm(account.forms.SignupForm):

    name = forms.CharField(
        label=("Name"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    def clean_name(self):
        if not alnum_re.search(self.cleaned_data["name"]):
            raise forms.ValidationError(("Names can only contain letters."))
