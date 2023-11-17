import time
from django.db import connection, reset_queries
from django.shortcuts import render


class PermissionCode:
    Owner = 'فروشگاه دار'

    End_User = 'کاربر نهایی'

    Waiter = 'گارسون'


def authority(perm_list):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            Owner = ""
            End_User = ""
            if getattr(request.user, "cafe_profile", None) is not None:
                Owner = "فروشگاه دار"
            if Owner in perm_list:
                return view_method(request, *args, **kwargs)
            if getattr(request.user, "cafe_profile", None) is None:
                End_User = "کاربر نهایی"
            if End_User in perm_list:
                return view_method(request, *args, **kwargs)
            else:
                return render(request, "adminpanel/404.html")

        return _arguments_wrapper

    return _method_wrapper


def debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        st = time.time()
        value = func(*args, **kwargs)
        et = time.time()
        queries = len(connection.queries)
        print(queries)
        print(et - st)
        return value

    return wrapper
