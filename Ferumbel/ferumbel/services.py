from django.db.models import Sum, F, QuerySet


def filter_products(
        products: QuerySet,
        price__gt: int = None,
        price__lt: int = None,
        order_by: str = None,
) -> QuerySet:
    if price__gt:
        products = products.filter(price__gt=price__gt)
    if price__lt:
        products = products.filter(price__lt=price__lt)
    if order_by:
        if order_by == "price_asc":
            products = products.order_by("price")
        if order_by == "price_desc":
            products = products.order_by("-price")
        if order_by == "max_count":
            products = products.annotate(total_count=Sum("purchases__count")).order_by(
                "-total_count"
            )
        if order_by == "max_price":
            products = products.annotate(
                total_price=Sum("purchases__count") * F("price")
            ).order_by("-total_price")
    return products