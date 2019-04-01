from django import forms


class PhoneNumberForm(forms.Form):

    phone_number = forms.CharField(required=True)
    phone_number_confirm = forms.CharField(required=True)

    def validate(self):
        super(PhoneNumberForm, self).is_valid()
        if self.cleaned_data["phone_number"] != self.cleaned_data["phone_number_confirm"]:
            return False
        num_str = str(self.cleaned_data["phone_number"])
        num = ""
        for char in num_str:
            try:
                int(char)
                num = num + char #concatenate
            except:
                pass #Not a number
        if len(num) == 10:
            return "+1" + num
        else:
            return False


class PhoneNumberVerifyForm(forms.Form):

    code = forms.CharField(required=True)
