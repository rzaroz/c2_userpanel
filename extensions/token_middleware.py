import logging

from django.contrib.auth.models import AnonymousUser, User
from django.utils.deprecation import MiddlewareMixin
import json, requests
from django.shortcuts import HttpResponseRedirect, reverse
import json

from django.conf import settings

from account.models import Profile

if settings.ENV["REAL_SERVER"]:
    host = 'http://c2oo.ir/'
else:
    host = 'http://127.0.0.1:8000/'


class TokenMiddleWare(MiddlewareMixin):
    def process_request(self, request):

        token = request.COOKIES.get("auth_token")
        url = host + "api/user_info/"
        payload = json.dumps({
            "token": token
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            # user_id = response.json()['user_id']
            # user = User.objects.filter(id=user_id).first()
            user_id = response.json()['user_id']
            username = response.json()['username']
            first_name = response.json()['first_name']
            is_superuser = response.json()['is_superuser']
            is_staff = response.json()['is_staff']
            user = User(id=user_id,
                        username=username,
                        first_name=first_name,
                        is_superuser=is_superuser,
                        is_staff=is_staff)
            profile = Profile.objects.filter(user_id=user.id).first()
            setattr(user, "profile", profile)
            setattr(request, "user", user)
        else:
            setattr(request, "user", AnonymousUser())
