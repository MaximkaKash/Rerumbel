from ferumbel.models import Snippet


def run():
    url = "http://127.0.0.1:8000/"
    for i in range(100):
        slug = "product/" + str(i)
        Snippet.objects.create(title="product/" + str(i), slug=slug).save()


run()
