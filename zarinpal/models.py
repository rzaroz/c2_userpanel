from django.db import models
from extensions.log_error_middleware import get_exact_exception_info

from extensions.utils import jalali_converter
from django.contrib.auth.models import User


class GeneralDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def jtime_updated_at(self):
        return jalali_converter(self.updated_at)

    def jtime_created_at(self):
        return jalali_converter(self.created_at)

    class Meta:
        abstract = True


class Payment(GeneralDate):
    amount = models.PositiveBigIntegerField(verbose_name="مقدار")
    status_choice = (
        ("pending", "pending"),
        ("success", "success"),
        ("failed", "failed"),
    )
    status = models.CharField(choices=status_choice, default="pending", max_length=30, verbose_name="وضعیت")
    user_id = models.IntegerField(null=True, blank=True)
    transaction_id = models.CharField(max_length=200, verbose_name="آیدی تراکنش")

    class Meta:
        verbose_name = "تراکنش ها"
        verbose_name_plural = "تراکنش ها"

    def __str__(self):
        return str(self.amount)


class FlowPayment(GeneralDate):
    name = models.CharField(max_length=100, verbose_name="نام پرداخت")
    amount = models.IntegerField(verbose_name="مقدار")
    discount = models.SmallIntegerField(default=0, verbose_name="تخفیف")

    class Meta:
        verbose_name = "پرداخت های فلو"
        verbose_name_plural = "پرداخت های فلو"

    def __str__(self):
        return self.name


class TransactionAmount(models.Model):
    amount = models.PositiveIntegerField(verbose_name="تومان")

    class Meta:
        verbose_name = "مقادیر پرداخت به کیف پول"
        verbose_name_plural = "مقادیر پرداخت به کیف پول"

    def __str__(self):
        return str(self.amount)


class SystemExceptions(models.Model):
    date_created = models.DateTimeField("تاریخ ایجاد", auto_now_add=True, editable=True)
    login_username = models.CharField("نام کاربری کاربر", max_length=50, null=True, blank=True)
    file_path = models.CharField("مسیر محل قرارگیری کد", max_length=250, null=True, blank=True)
    line_number = models.IntegerField("شماره خط", null=True, blank=True)
    exception_name = models.CharField("عنوان خطا", max_length=250, null=True, blank=True)
    exception_content = models.TextField("محتوای خطا")
    exact_info = models.TextField("اطلاعات دقیق خطا", null=True, blank=True)
    url = models.CharField("آدرس", max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "لاگ خطای سیستم"
        verbose_name_plural = "لاگ خطاهای سیستم"

    def __str__(self):
        return self.url

    @classmethod
    def create_log(cls, user, path, line, content, name=None, url=None, ip=None, is_deleted=False,
                   middleware=None, extra=""):
        exception_log = cls(file_path=path, line_number=line, exception_name=name,
                            exception_content=content, url=url, )
        if user:
            if user.is_anonymous:
                exception_log.login_username = str(user)
            else:
                exception_log.login_username = user.username
                if ip:
                    exception_log.login_username += "\n" + str(ip)

        exception_log.exact_info = get_exact_exception_info() + "\n" + extra
        exception_log.save()
        return exception_log
