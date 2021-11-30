from django.contrib import admin

from ferumbel.models import Product, Photos, Text, Benefits, Contacts, Timetable, Image, Category, Purchase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "coast", "description", "popular")
    search_fields = ("name", "coast")


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    display = "photo"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    display_list = ("user", "product", "count", "created_at")
    search_fields = ("user",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    display = "Text"


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    display = "value"


@admin.register(Benefits)
class BenefitsAdmin(admin.ModelAdmin):
    list_display = ("value", "photo")


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("pole", "value")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    display = ("Image")


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    display = ("text", "name", "value", "position")
