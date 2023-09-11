from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Charity
from django.template import loader
from .form import DonateForm


def charityhome(request):
    dnform = DonateForm(request.POST or None)
    context = {
        "dnform": dnform
    }

    if dnform.is_valid():
        dnform.save()
        return HttpResponseRedirect(
            reverse("request") + "?" + "w=" + str(dnform.cleaned_data.get("price")))

    return render(request, "charityhomepage.html", context)
