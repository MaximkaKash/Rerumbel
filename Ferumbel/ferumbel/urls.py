from django.urls import path
from ferumbel.views import ProductsView, product_details_view, register_view, Contact, AboutUs, page_not_found_view, \
    logout_user, activeOrder_view, confirmedOrder_view, deletedOrder_view, \
    basket, autorization, activeOrders, confirmedOrders, deletedOrders, ProductsView1, \
    category_view, Index, get_file, CategorysView, CategorysView1, get_robots, get_sitemap
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from ferumbel.sitemaps import StaticViewSitemap
from ferumbel.models import Product  # new

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('contacts/', Contact.as_view(), name='contacts'),
    path("register/", register_view, name="register_view"),
    path('aboutUs/', AboutUs.as_view(), name='aboutUs'),
    path("catalog/", ProductsView.as_view(), name="productsView"),
    path("products/", CategorysView.as_view(), name="categorysView"),
    path("services/", CategorysView1.as_view(), name="categorysView1"),
    path("catalog1/", ProductsView1.as_view(), name="products_view1"),
    path(
        "product/<int:product_id>/", product_details_view, name="product_details_view"
    ),
    path("category/<int:category_id>/", category_view, name="category_view"),
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
    path("logout/", logout_user, name='logout'),
    path("file/", get_file, name='get_file'),
    # path("robots.txt", get_robots, name="get_robots"),
    # path("sitemap.xml", get_sitemap, name="get_sitemap"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]

handler404 = page_not_found_view

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     # Serve static and media files from development server
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
