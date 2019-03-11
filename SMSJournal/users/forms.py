from django import forms
from .models import Subscriber


class PhoneNumberForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PhoneNumberForm,self).__init__(*args, **kwargs)

    phone_number = forms.CharField(required=True)
    phone_number_verify = forms.CharField(required=True)

    # Requires clean and verify methods
