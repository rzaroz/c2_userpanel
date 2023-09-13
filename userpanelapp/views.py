from django.shortcuts import render

from .forms import SearchForm
from .models import *
from django.shortcuts import HttpResponse


def user_panel(request):
    context = {}
    profile = Profile.objects.filter(user_id=request.user.id).first()
    if profile:
        context['balance'] = profile.balance
    if request.user:
        context["username"] = request.user.username
    return render(request, 'userpanel.html', context)


def setting(request):
    context = {}

    return render(request, 'setting.html', context)


def ajax_get_rate(request):
    star = 5
    # if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    profile = Profile.objects.filter(user_id=request.user.id).first()
    rate = Rate.objects.filter(profile=profile).all()
    if rate:
        length = 0
        total = 0
        for index in rate:
            total += index.star
            length += 1
        star = total / length
    return HttpResponse(star)
    # else:
    #     return HttpResponse(None)


def search(request):
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            results = Profile.objects.filter(user_id__icontains=query).all()
        else:
            results = []
    else:
        form = SearchForm()
        results = []
    context = {'form': form, 'results': results}
    return render(request, 'search.html', context)
