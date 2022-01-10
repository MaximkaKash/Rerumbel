from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from ferumbel.models import Contacts, Photos, Benefits, Text, Product, Timetable, Purchase, Category, Profile, Order
from ferumbel.forms import ProductFiltersForm
from django.views.generic import TemplateView
from ferumbel.services import filter_products
from ferumbel.forms import RegistrationForm, BasketForm, LoginForm
from django.contrib.auth import authenticate, login, logout
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
        "categorys": category,
        "Text": text.get(id=4),
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
                product=product, user=request.user, count=int(request.POST["count"]),
                index=int(request.user.profile.index)
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
        purchases = Purchase.objects.filter(user=request.user).filter(index=request.user.profile.index)
        # user = User.objects.filter(user=profile.user)
        form = BasketForm(request.POST)
        sum_product = 0
        count = 0

        for purchase in purchases:
            sum_product = sum_product + int(purchase.product.coast) * int(purchase.count)
            count = count + int(purchase.count)
            # purchase.index = int(purchase.index) + 1
            purchase.save()

        if request.method == "POST":
            if form.is_valid():
                request.user.username = form.cleaned_data["username"]
                request.user.save()
                for purchase in purchases:
                    Order.objects.create(user=request.user.profile,
                                         purchase=purchase,
                                         phone=form.cleaned_data["phone"],
                                         comment=form.cleaned_data["comment"],
                                         delivery=True,
                                         index=int(request.user.profile.index),
                                         adress=form.cleaned_data["address"], )
                    Order.save(self=request.user)

                request.user.profile.phone = form.cleaned_data["phone"]
                # profile.delivery = form.cleaned_data["delivery"]
                request.user.profile.adress = form.cleaned_data["address"]
                request.user.profile.comment = form.cleaned_data["comment"]
                request.user.profile.index = int(request.user.profile.index) + 1
                request.user.profile.save()
                return redirect('/')

            # request.user.profile.address = form.cleaned_data[""]
            # request.user.profile.save()
            # request.user.save()
            # if Purchase.user.is_relation:
            # user = request.User.seller
            # orders = request.User.seller
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


def autorization(request):
    form = LoginForm()
    if request.user.is_staff:
        return render(request, "activeOrders.html")
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            # data = form.cleaned_data['login']
            # data = form.cleaned_data.get('login')
            # print(data)
            if form.is_valid():
                #     user = User.objects.filter(username=form.cleaned_data.get('login'))
                #     if User.objects.filter(username=form.cleaned_data.get('password')) == user.get("password"):
                #         return render(request, "index.html")
                # form = LoginForm()
                user = authenticate(request, username=form.cleaned_data.get('login'),
                                    password=form.cleaned_data.get('password'))

                login(request, user)
                return redirect('/activeOrders')
            form = LoginForm()
        return render(request, "autorization.html", {"form": form})


from itertools import groupby


def activeOrders(request):
    if request.user.is_staff:
        # if request.method == "Exit":
        #     logout_user(request)
        #     return redirect("/")
        orders = Order.objects.all()
        # index = orders.objects.all().order_by("index")[0]
        orde = list(range(0))
        ord = list(range(0))

        for order in orders:
            orde.append(int(order.index))

        orde = [el for el, _ in groupby(orde)]
        for i in orde:
            order = Order.objects.all().filter(index=i)
            ord.append(order.order_by("id")[0])
            print(order)
        print(ord)
        return render(request, "activeOrders.html",
                      {"orders": ord})
    else:
        return redirect("/")


def activeOrder_view(request, *args, **kwargs):
    order = Order.objects.get(id=kwargs["order_id"])
    # if request.method == "POST":
    #     if request.user.is_authenticated:
    #         Purchase.objects.create(
    #             product=product, user=request.user, count=int(request.POST["count"])
    #         )
    #         redirect("product_details_view", product_id=product.id)
    #     else:
    #         form = RegistrationForm()
    #         return redirect('/register', {"form": form})
    return render(
        request,
        "activeOrder.html",
        {
            "orders": order,
        },
    )


def confirmedOrders(request):
    if request.user.is_staff:
        return render(request, "confirmedOrders.html")
    else:
        return redirect("/")


def deletedOrders(request):
    if request.user.is_staff:
        return render(request, "deletedOrders.html")
    else:
        return redirect("/")


def logout_user(request):
    logout(request)
    return redirect("/")
