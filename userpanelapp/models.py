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

    # @property
    # def user(self):
    #     return User()

    # def save(
    #         self, *args, **kwargs
    # ):
    #     if not self.hash:
    #         self.hash = make_hash(Flow)
    #     super().save(*args, **kwargs)


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
    price = models.PositiveIntegerField()


class Factor(GeneralDate):
    status = models.IntegerField()
    charity = models.ForeignKey("Charity", on_delete=models.SET_NULL, null=True, blank=True)
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
    STORE = 1
    SERVICE = 2
    TYPE_CHOICES = ((STORE, 'store'), (SERVICE, 'service'))

    row_number = models.PositiveIntegerField()
    factor = models.ForeignKey(Factor,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='factor_rows')
    service = models.OneToOneField(Service,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='service_factor')
    description = models.TextField()
    count = models.PositiveIntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES)


class Rate(GeneralDate):
    profile = models.OneToOneField("Profile", on_delete=models.CASCADE, related_name='profile_rate')
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


class MyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class General(GeneralDate):
    is_delete = models.BooleanField(default=False)
    objects = MyManager()
    allobject = models.Manager()

    def delete(self):
        self.is_delete = True
        self.save()

    class Meta:
        abstract = True


class Charity(GeneralDate):
    ACCEPTED = 1
    REJECTED = 2
    PENDING = 3

    payment_Status = (
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
        (PENDING, "Pending")
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    price = models.PositiveBigIntegerField(null=False, blank=False)
    phone_number = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(choices=payment_Status, null=False, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="charity")
