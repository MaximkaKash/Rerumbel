from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from ferumbel.models import Contacts, Photos, Benefits, Text, Product, Timetable, Purchase, Category, Profile, Order
from ferumbel.forms import ProductFiltersForm
from django.views.generic import TemplateView
from ferumbel.services import filter_products
from ferumbel.forms import RegistrationForm, BasketForm
from django.contrib.auth import authenticate, login
from django.db.models import F, Sum

logger = logging.getLogger(__name__)


def page_not_found_view(request, exception):
    return render(request, 'mistake.html', status=404)


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # if User.objects.filter(username=form.cleaned_data.get('username')).exists():
            #     if User.objects.filter(username=form.cleaned_data.get('email')).exists():
            #         form = RegistrationForm()
            #         return render(request, "register1.html", {"form": form})
            request.user = User.objects.create(email=form.cleaned_data.get('email'),
                                               username=form.cleaned_data.get('username'),
                                               password=form.cleaned_data.get('email'))
            Profile.objects.create(email=form.cleaned_data.get('email'),
                                   user=request.user)
            Profile.save(self=request.user)
            user = authenticate(request, username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('email'))
            login(request, user)
            # password = ""
            # user.set_password(password)
            # send_email()

            return redirect('/')
        else:
            form = RegistrationForm()
        return render(request, "register2.html", {"form": form})
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


class ProductsView(TemplateView):
    template_name = "goods.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        filters_form = ProductFiltersForm(self.request.GET)

        if filters_form.is_valid():
            if filters_form.cleaned_data["section"]:
                products = products.filter(type=filters_form.cleaned_data["section"])
            if filters_form.cleaned_data["price__gt"]:
                products = products.filter(price__gt=filters_form.cleaned_data["price__gt"])
            if filters_form.cleaned_data["price__lt"]:
                products = products.filter(price__lt=filters_form.cleaned_data["price__lt"])

            if filters_form.cleaned_data["order_by"]:
                order_by = filters_form.cleaned_data["order_by"]
                if order_by == "popular":
                    products = products.order_by("-popular")
                if order_by == "price_asc":
                    products = products.order_by("coast")
                if order_by == "price_desc":
                    products = products.order_by("-coast")

        return {"filters_form": filters_form, "products": products}


def index(request):
    text = Text.objects.all()
    benefits = Benefits.objects.all()
    photo = Photos.objects.all()
    product = Product.objects.all().order_by("-popular")[0:3]
    # product = product.objects.order_by("popular")
    category = Category.objects.all().order_by("-is_main")[0:3]
    # category = category.filter(name="is_main").order_by("-is_main")
    return render(request, "index.html", {
        "benefits": benefits,
        "text": text.get(id=1),
        "photo": photo.get(id=1),
        "products": product,
        "categorys": category
    })
    # photos = Photos.objects.all()
    # return HttpResponse(photos)
    # return HttpResponse(json.dumps([c.photo for c in photos]))
    # return HttpResponse("Hello, world. You're at the polls index.")


def contacts(request):
    contacts = Contacts.objects.all()
    return render(request, "contacts.html", {
        "contacts": contacts
    })


def aboutUs(request):
    text = Text.objects.all()
    timetable = Timetable.objects.all().order_by("position")
    return render(request, "aboutUs.html", {
        "contacts": timetable,
        "texts": text.get(id=3),
        "text": text.get(id=2)
    })


def product_details_view(request, *args, **kwargs):
    product = Product.objects.get(id=kwargs["product_id"])

    if request.method == "POST":
        if request.user.is_authenticated:
            Purchase.objects.create(
                product=product, user=request.user, count=int(request.POST["count"])
            )
            redirect("product_details_view", product_id=product.id)
        else:
            form = RegistrationForm()
            return redirect('/register', {"form": form})

    return render(
        request,
        "good.html",
        {
            "product": product,
        },
    )


def basket(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
        # user = User.objects.filter(user=profile.user)
        profile = Profile.objects.filter(user=request.user)
        form = BasketForm(request.POST)
        sum_product = 0
        count = 0

        for purchase in purchases:
            sum_product = sum_product + int(purchase.product.coast)
            count = count + int(purchase.count)

        if request.method == "POST":
            if form.is_valid():
                request.user.username = form.cleaned_data["username"]
                request.user.save()

                request.user.profile.phone = form.cleaned_data["phone"]
                # profile.delivery = form.cleaned_data["delivery"]
                request.user.profile.adress = form.cleaned_data["address"]
                request.user.profile.comment = form.cleaned_data["comment"]
                request.user.profile.save()

                Order.objects.create(user=request.user.profile,
                                     purchase=purchase,
                                     phone=form.cleaned_data["phone"],
                                     comment=form.cleaned_data["comment"],
                                     delivery=True,
                                     adress=form.cleaned_data["address"], )
                Order.save(self=request.user)
                return redirect('/')

            # request.user.profile.address = form.cleaned_data[""]
            # request.user.profile.save()
            # request.user.save()
            # if Purchase.user.is_relation:
            # user = request.User.seller
            # orders = request.User.seller
            # # purchase = ...
            # result = purchases.objects.aggregate(purchases=Sum("count"))

            else:
                form = BasketForm()
        return render(
            request,
            "basket.html",
            {
                "name": request.user.username,
                "phone": request.user.profile.phone,
                # "delivery": profile.delivery,
                "address": request.user.profile.adress,
                "comment": request.user.profile.comment,
                "purhcase": purchases,
                "form": form,
                "sum": sum_product,
                "result": count,
            }
        )
    else:
        form = RegistrationForm()
        return redirect('/register', {"form": form})
