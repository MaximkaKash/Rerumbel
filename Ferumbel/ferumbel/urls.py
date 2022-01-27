from django.urls import path
from ferumbel.views import ProductsView, product_details_view, register_view, contacts, aboutUs, page_not_found_view, \
    logout_user, activeOrder_view, confirmedOrder_view, deletedOrder_view, \
    basket, autorization, activeOrders, confirmedOrders, deletedOrders
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


    path("autorization/", autorization, name="autorization"),
    path("activeOrders/", activeOrders, name="activeOrders"),
    path(
        "activeOrder/<int:order_index>/", activeOrder_view, name="activeOrder_view"
    ),
    path("confirmedOrders/", confirmedOrders, name="confirmedOrders"),
    path(
        "confirmedOrder/<int:order_index>/", confirmedOrder_view, name="confirmedOrder_view"
    ),
    path("deletedOrders/", deletedOrders, name="deletedOrders"),
    path(
        "deletedOrder/<int:order_index>/", deletedOrder_view, name="deletedOrder_view"
    ),
    path("logout/", logout_user, name='logout')
]

handler404 = page_not_found_view

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     # Serve static and media files from development server
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
