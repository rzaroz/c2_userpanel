from django import forms


class SubmitRequest(forms.Form):
    name = forms.CharField(
        label_suffix="",
        label="عنوان تبلیغ",
        widget=forms.TextInput(attrs={"placeholder": "تبلیغ شرکت ، تبلیغ کار . . ."})
    )
    desc = forms.CharField(
        label="توظیحات تبلیغ",
        label_suffix="",
        widget=forms.Textarea(attrs={"placeholder": "توظیحات خودتان را درمورد تبلیغ خود بنویسید ."})
    )
    adfile = forms.FileField(
        label_suffix="",
        label="فایل تبلیغاتی(ویدیو یا عکس تبلیغ خود را آپلود کنید)",
        required=True
    )
    time = forms.CharField(
        label_suffix="",
        label="مدت زمان تبلیغ",
        widget=forms.TextInput(
            attrs={
                "placeholder": "مدت زمان که میخواهید تبلیغ دیده شود"
            }
        )
    )
    maxview = forms.CharField(
        label_suffix="",
        label="تعداد بازدید مورد نظر",
        widget=forms.TextInput(
            attrs={
                "placeholder": "تعداد بازدیدی که می خواهید روی تبلیغتان انحام شود"
            }
        )
    )

    def clean(self):
        data = self.cleaned_data
        name = data.get("name")
        desc = data.get("desc")
        video = data.get("adfile")
        time = data.get("time")
        maxview = data.get("maxview")

        if len(name) > 130:
            raise forms.ValidationError("اسم باید کمتر از 130 حرف باشد")

        if len(desc) > 400:
            raise forms.ValidationError("عنوان باید کمتر از 130 حرف باشد")

        # if not video.name.endswith(".mp4") and not video.name.endswith(".jpg"):
        #     raise forms.ValidationError("فایل تبلیغی شما می تواند تنها به دو حالت jpg و mp4 باشد")

        # timetype = int(time)
        # if type(timetype) != int:
        #     raise forms.ValidationError("زمان باید به عدد باشد")
        #
        # maxvidetype = int(maxview)
        # if type(maxvidetype) != int:
        #     raise forms.ValidationError("مقدار ویو باید به عدد باشد")
