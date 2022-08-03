from django.contrib import admin

from ferumbel.models import Product, Photos, Text, Benefits, Contacts, Timetable, Image, Category, Purchase, Profile, \
    Sections, Order, Customer, Characteristic


# class CategoryInline(admin.TabularInline):
#     model = Product

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ("product", "pole", "value")
    search_fields = ("product",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "coast", "popular", "category", "division")
    search_fields = ("name", "coast")
    # readonly_fields = ("name", ) атрибуты нельзя переименовать
    # list_filter = ("coast", "name")


@admin.register(Sections)
class SectionsAdmin(admin.ModelAdmin):
    list_display = ("name", "isMain", "products")
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "phone", "email", "delivery")
    search_fields = ("user", "name", "phone", "delivery")


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("photo", "product")
    search_fields = ("photo",)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "count", "created_at")
    search_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("Text", "Photo", "is_main", "division")
    search_fields = ("Text",)
    ordering = ('Text',)
    # inlines = [CategoryInline]


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    display = "value"

    def get_actions(self, request):
        actions = super(TextAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


def has_delete_permission(request, obj=None):
    return False


@admin.register(Benefits)
class BenefitsAdmin(admin.ModelAdmin):
    list_display = ("value", "photo")


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("pole", "value", "adr")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    display = "Image"


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "position")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "coast", "created_at", "statuc", "customer")
    search_fields = ("created_at",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "index", "delivery", "foruser")
