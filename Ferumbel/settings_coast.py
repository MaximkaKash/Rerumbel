from ferumbel.models import Product, Curs


def run():
    products = Product.objects.all()
    curs = Curs.objects.all()
    curs = curs.get(id=1)
    curs = curs.value
    for product in products:
        product.coast = product.coefficient * curs
        product.save()
        print(product.coast, product.coefficient, curs)


run()
