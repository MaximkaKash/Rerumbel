from django.urls import path
from ferumbel.views import ProductsView, product_details_view, register_view, contacts, aboutUs, page_not_found_view, basket
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path("register/", register_view, name="register_view"),
    path('aboutUs/', aboutUs, name='aboutUs'),
    path("catalog/", ProductsView.as_view(), name="products_view"),
    path(
        "product/<int:product_id>/", product_details_view, name="product_details_view"
    ),
    path("basket/", basket, name="basket"),
]

handler404 = page_not_found_view

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     # Serve static and media files from development server
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)