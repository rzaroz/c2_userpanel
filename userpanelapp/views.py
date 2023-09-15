from django.shortcuts import render
import random
from .forms import SearchForm
from .models import *
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect, HttpResponse


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
    star = 0
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
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
    else:
        return HttpResponse(None)


def test_ajax(request):
    return render(request, 'test_ajax.html')


def ajax_set_rate(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            user_id = request.GET.get("user_id")
            star = int(request.GET.get("star"))
            profile = Profile.objects.filter(user_id=user_id).first()
            rate = Rate.objects.filter(profile=profile).all()
            rate.delete()
            rate = Rate(profile=profile, star=star)
            rate.save()
            return HttpResponse(True)
        except:
            return HttpResponse(False)


def ajax_add_service(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            name = request.GET.get('name')
            description = request.GET.get('description')
            price = request.GET.get('price')
            profile = Profile.objects.filter(user_id=request.user.id).first()
            service_instance = Service(profile=profile, name=name, description=description, price=int(price))
            service_instance.save()
            return HttpResponse(True)
        except:
            return HttpResponse(False)


def search(request):
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            results = Service.objects.filter(name__icontains=query).all()
        else:
            results = []
    else:
        form = SearchForm()
        results = []
    context = {'form': form, 'results': results}
    return render(request, 'search.html', context)


def service(request):
    context = {}
    profile = Profile.objects.filter(user_id=request.user.id).first()
    service_instance = Service.objects.filter(profile=profile).all()
    context['service'] = service_instance
    return render(request, '', context)


def factor(request, factor_id):
    context = {}
    if request.POST:
        total_price = 0

        discount = request.POST.get('discount')
        context['discount'] = discount

        factor = Factor.objects.filter(id=factor_id).first()
        factor_rows = factor.factor_rows.all()

        for index in factor_rows:
            total_price += index.count * index.service.price

        context['factor_rows'] = factor_rows
        context['total_price'] = total_price
    return render(request, 'factor.html', context)


def factors(request):
    context = {}
    factors_list = Factor.objects.filter(owner__user_id=request.user.id).all()
    context['factors'] = factors_list
    if request.POST:
        factor_id = request.POST.get('factor_id')
        return HttpResponseRedirect(reverse("factor", kwargs={"factor_id": factor_id}))
    return render(request, 'factors.html', context)


def choose_lottery_winner(filter_value):
    participants = Profile.objects.filter(category=filter_value).all()

    if not participants:
        return None

    winner = random.choice(participants)
    return winner


def lottery(request):
    context = {}
    winners = []

    if request.method == 'POST':
        try:
            number = int(request.POST.get('number'))
            category = request.POST.get('category')

            for _ in range(number):
                winner = choose_lottery_winner(category)
                if not winner:
                    context['error'] = 'برای دسته بندی انتخاب شده کاربری پیدا نشد'
                    return render(request, '', context)

                if winner not in winners:
                    winners.append(winner)

            context['winners_list'] = winners
        except ValueError:
            context['error'] = 'Please enter a valid number.'

    return render(request, '', context)
