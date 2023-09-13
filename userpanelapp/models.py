from django.db import models

from extentions.utils import jalali_converter


class GeneralDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def jtime_updated_at(self):
        return jalali_converter(self.updated_at)

    def jtime_created_at(self):
        return jalali_converter(self.created_at)

    class Meta:
        abstract = True


class Profile(GeneralDate):
    STORE = 1
    SERVICE = 2
    type_choices = ((STORE, 'store'), (SERVICE, 'service'))
    level_choices = (
        (STORE, 'store'), (SERVICE, 'service')
    )
    choices = [(STORE, 'store'), (SERVICE, 'service')]
    user_id = models.IntegerField()
    level = models.IntegerField(choices=level_choices, default=0, verbose_name="سطح")
    category = models.IntegerField(choices=choices, default=SERVICE, verbose_name="دسته بندی")
    type = models.IntegerField(choices=type_choices, verbose_name="نوع")
    balance = models.PositiveIntegerField(default=0)
    skill_count = models.IntegerField(default=1)
    hash = models.CharField(max_length=20)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل"

    def __str__(self):
        return str(self.user_id)

    @property
    def user(self):
        return User()

    def save(
            self, *args, **kwargs
    ):
        if not self.hash:
            self.hash = make_hash(Flow)
        super().save(*args, **kwargs)


class Address(GeneralDate):
    address = models.TextField()
    lat = models.FloatField()
    lang = models.FloatField()
    zone = models.FileField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_address')


class Service(GeneralDate):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_service')
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()


class Factor(GeneralDate):
    status = models.IntegerField()
    charity = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    gift = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    owner = models.ForeignKey(Profile,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='profile_owner')
    end_user = models.ForeignKey(Profile,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='profile_end_user')


class FactorRow(GeneralDate):
    factor = models.ForeignKey(Factor, on_delete=models.SET_NULL, null=True, blank=True, related_name='factor')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service')
    count = models.PositiveIntegerField()


class Rate(GeneralDate):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile_rate')
    star = models.PositiveIntegerField()


class Payment(GeneralDate):
    amount = models.PositiveBigIntegerField(verbose_name="مقدار")
    status_choice = (
        ("pending", "pending"),
        ("success", "success"),
        ("failed", "failed"),
    )
    status = models.CharField(choices=status_choice, default="pending", max_length=30, verbose_name="وضعیت")
    profile = models.ForeignKey(Profile,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='profile_payment')
    transaction_id = models.CharField(max_length=200, verbose_name="آیدی تراکنش")

    class Meta:
        verbose_name = "تراکنش ها"
        verbose_name_plural = "تراکنش ها"

    def __str__(self):
        return str(self.amount)


class TransactionAmount(models.Model):
    amount = models.PositiveIntegerField(verbose_name="تومان")

    class Meta:
        verbose_name = "مقادیر پرداخت به کیف پول"
        verbose_name_plural = "مقادیر پرداخت به کیف پول"

    def __str__(self):
        return str(self.amount)
