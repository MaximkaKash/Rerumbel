from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from ferumbel.models import Contacts, Photos, Benefits, Text, Product, Timetable, Purchase, Category, Profile, Order, \
    Customer
from ferumbel.forms import ProductFiltersForm
from django.views.generic import TemplateView
from ferumbel.services import filter_products
from ferumbel.forms import RegistrationForm, BasketForm, LoginForm, filter_form
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
            # user.set_password(password)
            # send_email()

            return redirect('/')
        else:
            form = RegistrationForm()
        return render(request, "register.html", {"form": form})
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


class ProductsView(TemplateView):
    template_name = "goods.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        products = Product.objects.all()
        filter_forms = filter_form(self.request.GET)
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

            if filter_forms.is_valid():
                if filter_forms.cleaned_data["categorys"]:
                    products = products.filter(category=filter_forms.cleaned_data["categorys"])
                if filter_forms.cleaned_data["way"] == "По популярности":
                    products = products.order_by("-popular")
                if filter_forms.cleaned_data["way"] == "По возростанию цены":
                    products = products.order_by("coast")
                if filter_forms.cleaned_data["way"] == "По убыванию цены":
                    products = products.order_by("-coast")
                if filter_forms.cleaned_data["price_1"]:
                    products = products.filter(price__gt=filters_form.cleaned_data["price_1"])
                if filter_forms.cleaned_data["price_1"]:
                    products = products.filter(price__lt=filters_form.cleaned_data["price_2"])
        categorys = Category.objects.all()
        return {"filters_form": filters_form,
                "products": products,
                "Text": text,
                "categorys": categorys,
                }


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
    text = Text.objects.get(id=4)
    return render(request, "contacts.html", {
        "contacts": contacts,
        "Text": text,
    })


def aboutUs(request):
    text = Text.objects.all()
    timetable = Timetable.objects.all().order_by("position")
    return render(request, "aboutUs.html", {
        "contacts": timetable,
        "texts": text.get(id=3),
        "text": text.get(id=2),
        "Text": text.get(id=4),
    })


def product_details_view(request, *args, **kwargs):
    product = Product.objects.get(id=kwargs["product_id"])
    text = Text.objects.get(id=4)

    if request.method == "POST":
        if request.user.is_authenticated:

            if request.user.is_staff:
                customer = Customer.objects.get(user=request.user)
                Purchase.objects.create(
                    product=product, user=request.user, count=int(request.POST["count"]),
                    index=int(customer.index)
                )

                purchases = Purchase.objects.filter(user=request.user).order_by("-created_at")[0]
                user = User.objects.get(id=(Order.objects.get(id=customer.ID).user_id))
                Order.objects.create(user=user,
                                     purchase=purchases,
                                     delivery=True,
                                     customer=customer,
                                     index=int(customer.index),
                                     )
                Order.save(self=request.user)
                return redirect("activeOrder_view", order_index=customer.ID)
            profile = Profile.objects.get(user=request.user)
            Purchase.objects.create(
                product=product, user=request.user, count=int(request.POST["count"]),
                index=int(profile.index)
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
            "Text": text,
        },
    )


def basket(request):
    if request.user.is_authenticated:
        text = Text.objects.get(id=4)
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=request.user)
        purchases = Purchase.objects.filter(user=request.user).filter(index=profile.index)
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
                    Order.objects.create(user=request.user,
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
                "Text": text,
            }
        )
    else:
        form = RegistrationForm()
        return redirect('/register', {"form": form})


def autorization(request):
    if request.user.is_staff:
        return redirect("/activeOrders")
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
                if Customer.objects.filter(user=user).exists():
                    return redirect("/activeOrders")
                else:
                    request.user = Customer.objects.create(user=request.user)
                return redirect("/activeOrders")
    form = LoginForm()
    return render(request, "autorization.html", {"form": form})


def activeOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=1).distinct("index", "user")
        return render(request, "activeOrders.html",
                      {"orders": orders})
    else:
        return redirect("/")


def activeOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
        form = BasketForm()
        user = Order.objects.get(id=kwargs["order_index"]).user_id
        index = Order.objects.get(id=kwargs["order_index"]).index
        orders = Order.objects.filter(user_id=user).filter(index=index)
        profile = User.objects.get(id=user)
        profile = Profile.objects.get(user=profile)
        # index = int(Order.objects.filter(index=kwargs["order_index"])[0].index)
        sum = 0
        count = 0
        for orde in orders:
            coast = 0
            coast = coast + int(orde.purchase.count) * int(orde.purchase.product.coast)
            orde.coast = coast
            count = count + int(orde.purchase.count)
            sum = sum + coast
            orde.save()
        if request.method == "POST":
            if request.POST.get("action", "") == "add":
                customer = Customer.objects.get(user=request.user)
                customer.index = index
                ID = Order.objects.get(id=kwargs["order_index"]).user_id
                customer.ID = kwargs["order_index"]
                print(customer.ID, user, ID)
                customer.save()
                return redirect("/catalog/")
            elif request.POST.get("action", "") == "delete":
                for orde in orders:
                    orde.statuc = 3
                    orde.save()
                return redirect("/activeOrders")
            elif request.POST.get("action", "") == "confirm":
                for orde in orders:
                    orde.statuc = 2
                    orde.save()
                profile = profile.objects.get(user_id=user)
                profile.username = form.cleaned_data["username"]
                profile.profile.phone = form.cleaned_data["phone"]
                # profile.delivery = form.cleaned_data["delivery"]
                profile.profile.adress = form.cleaned_data["address"]
                profile.user.profile.comment = form.cleaned_data["comment"]
                profile.save()
                return redirect("/activeOrders/")
            elif request.POST['delete']:
                orde = Order.objects.get(id=int(request.POST['delete']))
                orde.delete()
                orders = Order.objects.filter(user_id=user).filter(index=index)[0].id
                return redirect("activeOrder_view", order_index=orders)

        return render(
            request,
            "activeOrder.html",
            {
                "orders": orders,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": profile
            },
        )
    return redirect("/")


def confirmedOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=2).distinct("index", "user")
        return render(request, "confirmedOrders.html",
                      {"orders": orders})
    else:
        return redirect("/")


def confirmedOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
        user = Order.objects.get(id=kwargs["order_index"]).user_id
        index = Order.objects.get(id=kwargs["order_index"]).index
        orders = Order.objects.filter(user_id=user).filter(index=index)
        profile = User.objects.get(id=user)
        profile = Profile.objects.get(user=profile)
        print(orders)
        if request.method == "POST":
            if request.POST["action"] == "delete":
                for orde in orders:
                    orde.statuc = 3
                    orde.save()
                return redirect("/confirmedOrders/")
            elif request.POST["action"] == "vosstan":
                for orde in orders:
                    orde.statuc = 1
                    orde.save()
                return redirect("/confirmedOrders/")
        sum = 0
        count = 0

        for orde in orders:
            coast = 0
            coast = coast + int(orde.purchase.count) * int(orde.purchase.product.coast)
            orde.coast = coast
            count = count + int(orde.purchase.count)
            sum = sum + coast
            orde.save()
        return render(
            request,
            "confirmedOrder.html",
            {
                "orders": orders,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": profile,
            },
        )
    return redirect("/")


def deletedOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=3).distinct("index", "user")
        return render(request, "deletedOrders.html",
                      {"orders": orders})
    else:
        return redirect("/")


def deletedOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
        user = Order.objects.get(id=kwargs["order_index"]).user_id
        index = Order.objects.get(id=kwargs["order_index"]).index
        orders = Order.objects.filter(user_id=user).filter(index=index)
        profile = User.objects.get(id=user)
        profile = Profile.objects.get(user=profile)
        if request.method == "POST":
            if request.POST["action"] == "vosstan":
                for orde in orders:
                    orde.statuc = 2
                    orde.save()
                return redirect("/deletedOrders")
        sum = 0
        count = 0
        for orde in orders:
            coast = 0
            coast = coast + int(orde.purchase.count) * int(orde.purchase.product.coast)
            orde.coast = coast
            count = count + int(orde.purchase.count)
            sum = sum + coast
            orde.save()
        return render(
            request,
            "deletedOrder.html",
            {
                "orders": orders,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": profile,
            },
        )
    return redirect("/")


def logout_user(request):
    logout(request)
    return redirect("/")
