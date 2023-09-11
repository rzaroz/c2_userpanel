from _ast import pattern

from django import forms
from .models import Charity


class DonateForm(forms.Form):
    name = forms.CharField(
        label="نام",
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "لطفا نام خود را وارد نمائید", "lang": "fa-ir"})
    )
    lname = forms.CharField(
        label="نام خانوادگی",
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "لطفا نام خانوادگی خود را وارد نمائید", "lang": "fa-ir"})
    )
    price = forms.IntegerField(
        label="مبلغ کمک به خیریه",
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "لطفا مبلغ مورد نظر خود را وارد نمائید"})
    )
    phone = forms.CharField(
        label="شماره همراه",
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "09..."})
    )

    def clean_price(self):
        form_price = self.cleaned_data.get("price")

        if form_price <= 0:
            raise forms.ValidationError(
                "مبلغ وارد شده نامعتبر می باشد."
            )
        return form_price

    def clean_phone(self):
        form_phone = self.cleaned_data.get("phone")

        if len(str(form_phone)) != 11:
            raise forms.ValidationError(
                "شماره همراه خود را به درستی وارد نمائید"
            )
        return form_phone

    def save(self):
        try:
            a = Charity(first_name=self.cleaned_data.get("name"), last_name=self.cleaned_data.get("fname"), phone_number=DonateForm.clean_phone.__get__("form_phone"),
                                       price=DonateForm.clean_price.__get__("price"))
            a.save()
        except Exception as  e:
            print(e)

