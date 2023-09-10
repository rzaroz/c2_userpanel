from django.shortcuts import render

def userpanel(request):
    context = {}

    return render(request, 'userpanel.html', context)

def setting(request):
    context = {}

    return render(request, 'setting.html', context)