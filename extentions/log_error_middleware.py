# -*- coding: utf-8 -*-
import datetime
import inspect
import logging
import re
from django.utils.deprecation import MiddlewareMixin

import sys

logger = logging.getLogger("exception_middleware")


def get_exact_exception_info():
    try:
        exc_type, exc_obj, exact_tb = sys.exc_info()
        while exact_tb.tb_next:
            # this code is to stop nesting exception to prevent logging libraries exception and
            # find exact piece of code where error occurred
            pre_exact_tb = exact_tb
            exact_tb = exact_tb.tb_next
            exact_f = exact_tb.tb_frame
            exact_main_path = exact_f.f_code.co_filename
            if ('src' not in exact_main_path) or ('e_visa' not in exact_main_path):
                do_break = True
                try:
                    # this code is for the logging middleware,
                    # it goes to a library file and then goes to project code, so we handle this situation
                    next_filename = exact_tb.tb_next.tb_frame.f_code.co_filename
                    do_break = ('src' not in next_filename) or ('e_visa' not in next_filename)
                except:
                    pass
                if do_break:
                    exact_tb = pre_exact_tb
                    break
        exact_f = exact_tb.tb_frame
        exact_main_path = exact_f.f_code.co_filename
        exact_path_sections = exact_main_path.split('src')
        exact_path = exact_path_sections[-1]

        exact_func_name = exact_f.f_code.co_name

        exact_lineno = exact_tb.tb_lineno
        local_vars = ''
        try:
            if isinstance(exact_f.f_locals, dict):
                for key, val in exact_f.f_locals.items():
                    local_vars += '(%s: %s)' % (key, val)
        except:
            pass
        return "%s (%s: %s) local_vars: (%s)" % (exact_path, exact_func_name, exact_lineno, local_vars[:10000])
    except Exception as e:
        return "err"


def _get_tb_with_depth(depth):
    exc_type, exc_obj, tb = sys.exc_info()
    count = 0
    while (count < depth):
        count += 1
        if tb.tb_next:
            tb = tb.tb_next
        else:
            break
    return tb


def get_line_number(depth=0):
    """
    This function returns the current line number of program
    its useful in exception logging
    """
    try:
        tb = _get_tb_with_depth(depth)
        lineno = tb.tb_lineno
        return lineno
    except:
        return inspect.currentframe().f_back.f_lineno


def get_file_and_module_name(depth=0):
    """
    This function returns the current file name and function name
    its useful in exception logging
    """
    try:
        tb = _get_tb_with_depth(depth)
        f = tb.tb_frame
        main_path = f.f_code.co_filename
        path_sections = main_path.split('src')
        path = path_sections[-1]

        func_name = f.f_code.co_name
        return "%s (%s)" % (path, func_name)
    except:
        function = "---"
        path = "---"
        try:
            inspector = inspect.currentframe().f_back.f_code
            function = inspector.co_name
            main_path = str(inspect.currentframe().f_back.f_code.co_filename)
            path_sections = main_path.split('src')
            path = path_sections[-1]
            return "%s (%s)" % (path, function)
        except Exception:
            return "%s (%s)" % (path, function)


def is_only_number(input_string):
    """
    check input_string only number digits
    :param input_string: string
    :return: boolean
    """
    return bool(re.match(r'\d', input_string))


def hasNumber(input_string):
    """
    check if input_string contains any numbers
    """
    return bool(re.search(r'\d', input_string))


def hasAlphabeticChars(input_string):
    """
    check if input_string contains any alphabetic character a-z A-Z
    """
    return bool(re.search('[a-zA-Z]', input_string))


def hasCapitalChars(input_string):
    """
    check if input_string contains any capital char A-Z
    """
    return bool(re.search('[A-Z]', input_string))


def hasUpperCaseAndNumber(input_string):
    """
    A12343--> True   aA243--> False
    """
    if not input_string.isupper():
        return False
    return True


def only_number_and_letter(input_string):
    if re.match("^[A-Za-z0-9]*$", input_string):
        return True
    return False


def only_english_fields(value):
    if re.match("^[a-zA-z]+$", value.replace(" ", "")):
        return True
    return False


def only_number_and_letter_and_space(input_string):
    if re.match("^[A-Za-z0-9]*$", input_string.replace(" ", "")):
        return True
    return False


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception:
        return None


def passed_five_days(date):
    """
    this function checks if five or more days passed from request submission date
    """
    submit_day = date
    try:
        current = datetime.datetime.today()
        diff = (current - submit_day).days
    except:
        current = datetime.date.today()
        diff = (current - submit_day).days
    if diff >= 5:
        return True
    return False


def split_fullname(str_name):
    if not str_name:
        return ""
    array_name = str_name.split(' ')
    if len(array_name) > 1:
        return array_name[0] + ' ' + array_name[-1]
    else:
        return array_name[0]


def create_tuple_from_range(start, end):
    temp_list = []
    for i in range(start, end + 1):
        temp_list.append((i, i))
    result = tuple(temp_list)
    return result


class LogErrorMiddleWare(MiddlewareMixin):

    def process_exception(self, http_request, exception):
        from zarinpal.models import SystemExceptions
        try:
            exception_log = SystemExceptions.create_log(http_request.user,
                                                        get_file_and_module_name(depth=2),
                                                        get_line_number(depth=2),
                                                        str(exception),
                                                        name="error catch in LogErrorMiddleWare",
                                                        url=http_request.path_info,
                                                        ip=get_client_ip(http_request),
                                                        middleware=True,
                                                        extra=str(http_request.POST))

            payload = None
            files = None
            if http_request.method == 'GET':
                payload = http_request.GET
            elif http_request.method == 'POST':
                payload = http_request.POST
                files = http_request.FILES

            logger.exception("error_exception_id_" + str(exception_log.id),
                             extra={"payload": payload, "method": http_request.method,
                                    "url": http_request.path_info, "files": files})
        except Exception as e:
            print(e)
        return None
