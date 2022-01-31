from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User

ORDER_BY_CHOICES = (
    ("price_asc", "Price Asc"),
    ("price_desc", "Price Desc"),
    ("popular", "Popular"),
)
TYPE_CHOICES = (("Product", "Product"), ("Service", "Service"))


# STATUS_CHOICES = ()

class Text(models.Model):
    value = models.TextField(verbose_name="Текст")

    def __str__(self):
        return f"{self.value}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Text")
        verbose_name_plural = _("Texts")


class Image(models.Model):
    Image = models.ImageField(verbose_name="Фото")

    def __str__(self):
        return f"{self.Image}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Photos(models.Model):
    photo = models.ImageField(null=True, blank=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.photo}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")


class Benefits(models.Model):
    photo = models.ImageField(verbose_name="Фото")
    value = models.TextField(verbose_name="Значение")

    class Meta:
        ordering = ["id"]
        verbose_name = _("Benefict")
        verbose_name_plural = _("Benefits")


class Contacts(models.Model):
    pole = models.TextField(null=True, verbose_name="Имя")
    value = models.CharField(max_length=40, null=True, verbose_name="Значение")
    adr = models.URLField(null=True, verbose_name="Ссылка")

    def __str__(self):
        return f"{self.pole},{self.value},{self.adr}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")


class Timetable(models.Model):
    name = models.CharField(max_length=200, verbose_name="День недели")
    value = models.TextField(blank=True, null=True, verbose_name="Значение")
    position = models.IntegerField(blank=True, null=True, verbose_name="Позиция")

    def __str__(self):
        return f"{self.name},{self.value},{self.position}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Timetable")
        verbose_name_plural = _("Timetables")


class Category(models.Model):
    Text = models.TextField(blank=True, verbose_name="Название")
    Photo = models.ImageField(blank=True, verbose_name="Фотография")
    is_main = models.BooleanField(default=True, verbose_name="Главная")

    def __str__(self):
        return f"{self.Text},{self.Photo},{self.is_main}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(models.Model):
    coast = models.TextField(blank=True, null=True, verbose_name="Цена")
    name = models.CharField(max_length=1000, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    popular = models.FloatField(default=0, verbose_name="Популярность")
    Image = models.ImageField(null=True, blank=True, verbose_name="Фотография")
    division = models.TextField(blank=True, null=True, verbose_name="Разделение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категория")

    def __str__(self):
        return f"{self.name},{self.coast},{self.description},{self.popular}, {self.category}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Sections(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    isMain = models.BooleanField(verbose_name="Главная")
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")

    def __str__(self):
        return f"{self.name},{self.isMain},{self.products}"

    class Meta:
        ordering = ["id"]
        verbose_name = _("Selection")
        verbose_name_plural = _("Selections")


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
    index = models.IntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.count}-{self.created_at}"

    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True, default=1)
    seller = models.IntegerField(blank=True, null=True)
    delivery = models.BooleanField(blank=True, null=True, verbose_name="Доставка")

    def __str__(self):
        return f"{self.user}"


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    index = models.IntegerField(blank=True, null=True)
    delivery = models.BooleanField(default=True, null=True, blank=True)
    ID = models.IntegerField(blank=True, null=True)


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, blank=True, null=True)
    coast = models.IntegerField(blank=True, null=True, default=1)
    phone = models.CharField(max_length=30, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    delivery = models.BooleanField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, blank=True, null=True)
    statuc = models.IntegerField(blank=True, null=True, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
