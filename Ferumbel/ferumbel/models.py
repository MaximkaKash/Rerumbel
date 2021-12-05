from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User


ORDER_BY_CHOICES = (
    ("price_asc", "Price Asc"),
    ("price_desc", "Price Desc"),
    ("popular", "Popular"),
)


class Text(models.Model):
    value = models.TextField()

    def __str__(self):
        return f"{self.value}"


class Image(models.Model):
    Image = models.ImageField()

    def __str__(self):
        return f"{self.Image}"


class Photos(models.Model):
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.photo}"

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"


class Benefits(models.Model):
    photo = models.ImageField()
    value = models.TextField()

    class Meta:
        verbose_name = "Benefict"
        verbose_name_plural = "Benefits"


class Contacts(models.Model):
    pole = models.TextField(null=True)
    value = models.CharField(max_length=40, null=True)
    adr = models.URLField(null=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class Timetable(models.Model):
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name},{self.value},{self.position}"


class Category(models.Model):
    Text = models.TextField(blank=True, default=1)
    Photo = models.ImageField(blank=True)
    is_main = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Text},{self.Photo},{self.is_main}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


ORDER_BY_CHOICES = (
    ("price_asc", "Price Asc"),
    ("price_desc", "Price Desc"),
    ("popular", "Popular"),
)
TYPE_CHOICES = (("Product", "Product"), ("Service", "Service"))


# STATUS_CHOICES = ()


class Product(models.Model):
    coast = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    popular = models.FloatField(default=0)
    Image = models.ImageField(null=True, blank=True)
    division = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(
        max_length=100, choices=TYPE_CHOICES, default="IN_STOCK"
    )

    def __str__(self):
        return f"{self.name},{self.coast},{self.description},{self.division},{self.popular}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sections(models.Model):
    name = models.CharField(max_length=200)
    isMain = models.BooleanField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Selection"
        verbose_name_plural = "Selections"


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.count}-{self.created_at}"

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    seller = models.IntegerField(blank=True, null=True)
    delivery = models.BooleanField(blank=True, null=True)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    delivery = models.BooleanField(default=True, null=True, blank=True)
    Text = models.TextField(blank=True)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    delivery = models.BooleanField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
