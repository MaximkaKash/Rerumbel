from ferumbel.models import Product, Curs


def run():
    products = Product.objects.all()
    curs = Curs.object.all()
    curs = curs.value
    for product in products:
        product.coast = product.coefficient * curs
        product.save()
        print(product.coast)
