from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from ferumbel.models import Contacts, Photos, Benefits, Text, Product, Timetable, Purchase, Category, Profile, Order, \
    Customer
from django.views.generic import TemplateView
from ferumbel.forms import RegistrationForm, BasketForm, LoginForm, filter_form
from django.contrib.auth import authenticate, login, logout
from ferumbel.cart import Cart
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
import random

logger = logging.getLogger(__name__)


# error 404
# from django.http import Http404
# from django.views.generic.detail import DetailView
#
# class  HorseView(DetailView):
#     model = Horse
#     template_name = "horses/horse_view.html"
#
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     horse = Horse.objects.get(pk = self.kwargs['pk'])
#
#     if not horse.is_viewable_by(self.request.user):
#         raise Http404
#
#     # continue with the rest of the method populating the context
#     return context

def page_not_found_view(request, exception):
    text = Text.objects.get(id=4)
    return render(request, 'mistake.html', {"Text": text}, status=404)


def register_view(request):
    text = Text.objects.get(id=4)
    if request.method == "POST":
        # form = RegistrationForm(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            # if User.objects.filter(username=form.cleaned_data.get('username')).exists():
            #     if User.objects.filter(username=form.cleaned_data.get('email')).exists():
            #         form = RegistrationForm()
            #         return render(request, "register1.html", {"form": form})

            # request.user = User.objects.create(email=form.cleaned_data.get('email'),
            #                                    username=form.cleaned_data.get('username'),
            #                                    password=form.cleaned_data.get('password'))
            # Profile.objects.create(email=form.cleaned_data.get('email'),
            #                        user=request.user)
            # Profile.save(self=request.user)
            if User.objects.filter(username=form.cleaned_data.get('login')).exists():
                user = User.objects.get(username=form.cleaned_data.get('login'))
                if user.password == form.cleaned_data.get('password'):
                    user = authenticate(request, username=form.cleaned_data.get('login'),
                                        password=form.cleaned_data.get('password'))
                    login(request, user)
                else:
                    return redirect('/register/')
                # user.set_password(password)
                # send_email()

                return redirect('/')
            else:
                request.user = User.objects.create(username=form.cleaned_data.get('login'),
                                                   password=form.cleaned_data.get('password'))
                Profile.objects.create(user=request.user)
                Profile.save(self=request.user)

            user = authenticate(request, username=form.cleaned_data.get('login'),
                                password=form.cleaned_data.get('password'))
            login(request, user)
            # user.set_password(password)
            # send_email()

            return redirect('/')
        else:
            form = LoginForm()
            # form = RegistrationForm()
        return render(request, "registration_start.html", {"form": form,
                                                           "Text": text, })
    else:
        form = LoginForm()
        # form = RegistrationForm()
    return render(request, "registration_start.html", {"form": form,
                                                       "Text": text, })


class ProductsView(TemplateView):
    template_name = "goods.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        products = Product.objects.all()
        products = products.filter(division=True)
        filter_forms = filter_form(self.request.GET)

        if filter_forms.is_valid():
            if filter_forms.cleaned_data["category"]:
                if filter_forms.cleaned_data["category"] == "Все" or filter_forms.cleaned_data["category"] == "":
                    a = 'Все'
                else:
                    category = Category.objects.get(Text=filter_forms.cleaned_data["category"])
                    a = filter_forms.cleaned_data["category"]
                    products = products.filter(category=category.id)
            if filter_forms.cleaned_data["way"] == "По популярности":
                b = 'По популярности'
                products = products.order_by("-popular")
            if filter_forms.cleaned_data["way"] == "По возростанию цены":
                b = "По возростанию цены"
                products = products.order_by("coast")
            if filter_forms.cleaned_data["way"] == "По убыванию цены":
                b = "По убыванию цены"
                products = products.order_by("-coast")
            if filter_forms.cleaned_data["min_price"]:
                c = filter_forms.cleaned_data["min_price"]
                products = products.filter(coast__gt=filter_forms.cleaned_data["min_price"] - 1)
            if filter_forms.cleaned_data["max_price"]:
                d = filter_forms.cleaned_data["max_price"]
                products = products.filter(coast__lt=filter_forms.cleaned_data["max_price"] + 1)
            a = filter_forms.cleaned_data["category"]
            b = filter_forms.cleaned_data["way"]
            c = filter_forms.cleaned_data["min_price"]
            d = filter_forms.cleaned_data["max_price"]
        else:
            a = 0
            b = 0
            c = 0
            d = 0
        print(a, b, c, d)
        categorys = Category.objects.all()
        filter_forms = filter_form()
        categorys = categorys.order_by("Text")
        return {"filter_forms": filter_forms,
                "products": products,
                "Text": text,
                "categorys": categorys,
                "category": a,
                "way": b,
                "min_price": c,
                "max_price": d,
                }


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.all()
        benefits = Benefits.objects.all()
        photo = Photos.objects.all()
        product = Product.objects.all().order_by("-popular")[0:3]
        # product = product.objects.order_by("popular")
        category = Category.objects.all().order_by("-is_main")[0:3]
        # category = category.filter(name="is_main").order_by("-is_main")
        return {
            "benefits": benefits,
            "text": text.get(id=1),
            "photo": photo.get(id=1),
            "products": product,
            "categorys": category,
            "Text": text.get(id=4),
        }


# def index(request):
#     text = Text.objects.all()
#     benefits = Benefits.objects.all()
#     photo = Photos.objects.all()
#     product = Product.objects.all().order_by("-popular")[0:3]
#     # product = product.objects.order_by("popular")
#     category = Category.objects.all().order_by("-is_main")[0:3]
#     # category = category.filter(name="is_main").order_by("-is_main")
#     return render(request, "index.html", {
#         "benefits": benefits,
#         "text": text.get(id=1),
#         "photo": photo.get(id=1),
#         "products": product,
#         "categorys": category,
#         "Text": text.get(id=4),
#     })


def category_view(request, *args, **kwargs):
    categorys = Category.objects.all()
    text = Text.objects.get(id=4)
    category = Category.objects.get(id=kwargs["category_id"])
    product = Product.objects.all().filter(category=category)
    # print(product[0].division)
    # tovar = product[0].division
    if product[0].division:
        url = 'http://127.0.0.1:8000/catalog/?category=' + category.Text + '&way=%D0%9F%D0%BE+%D0%BF%D0%BE%D0%BF%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D0%BE%D1%81%D1%82%D0%B8&min_price=&max_price='
        return redirect(url)

    url = 'http://127.0.0.1:8000/catalog1/?category=' + category.Text + '&way=%D0%9F%D0%BE+%D0%BF%D0%BE%D0%BF%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D0%BE%D1%81%D1%82%D0%B8&min_price=&max_price='
    return redirect(url)


# def transport_index_to_topycs(request, *args, **kwargs):
#     product = Product.objects.get(id=kwargs["product_id"])
#     category = product.category
#     if category == True:
#         return render(
#             request,
#             "goods1.html",
#             {
#                 "product": product,
#                 "category": category,
#             }
#         )
#     pass


class Contact(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        contacts = Contacts.objects.all()
        text = Text.objects.get(id=4)
        return {
            "contacts": contacts,
            "Text": text,
        }


# def contacts(request):
#     contacts = Contacts.objects.all()
#     text = Text.objects.get(id=4)
#     return render(request, "contacts.html", {
#         "contacts": contacts,
#         "Text": text,
#     })

class AboutUs(TemplateView):
    template_name = "aboutUs.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.all()
        timetable = Timetable.objects.all().order_by("position")
        return {
            "contacts": timetable,
            "texts": text.get(id=3),
            "text": text.get(id=2),
            "Text": text.get(id=4),
        }


# def aboutUs(request):
#     text = Text.objects.all()
#     timetable = Timetable.objects.all().order_by("position")
#     return render(request, "aboutUs.html", {
#         "contacts": timetable,
#         "texts": text.get(id=3),
#         "text": text.get(id=2),
#         "Text": text.get(id=4),
#     })


# @require_POST
# def cart_add(request, product_id, count):
#     cart = Cart(request)
#     product = product_id
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('/goods/')
#
#
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = product_id
#     cart.remove(product)
#     return redirect('cart:cart_detail')
#
#
# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/detail.html', {'cart': cart})

def product_details_view(request, *args, **kwargs):
    product = Product.objects.get(id=kwargs["product_id"])
    product.popular += 1
    product.save()
    text = Text.objects.get(id=4)
    products = Product.objects.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.is_staff:
                customer = Customer.objects.get(user=request.user)
                Purchase.objects.create(
                    product=product, user=request.user, count=int(request.POST["count"]),
                    index=int(customer.index)
                )

                purchases = Purchase.objects.filter(user=request.user).order_by("-created_at")[0]
                if customer.foruser:
                    user = User.objects.get(id=(Order.objects.get(id=customer.foruser).user_id))
                    Order.objects.create(user=user,
                                         purchase=purchases,
                                         delivery=True,
                                         customer=customer,
                                         index=int(customer.index),
                                         )
                    Order.save(self=request.user)
                customer.foruser = None
                customer.save()
                return redirect("activeOrder_view", order_index=customer.foruser)
            else:
                profile = Profile.objects.get(user=request.user)
                Purchase.objects.create(
                    product=product, user=request.user, count=int(request.POST["count"]),
                    index=int(profile.index)
                )
                return render(
                    request,
                    "good.html",
                    {
                        "a": True,
                        "products": products,
                        "product": product,
                        "Text": text,
                    },
                )
        else:
            Login = random.randint(10000, 99999)
            request.user = User.objects.create(username=Login,
                                               password=1111)
            Profile.objects.create(user=request.user)
            Profile.save(self=request.user)

            user = authenticate(request, username=Login,
                                password=1111)
            login(request, user)
            profile = Profile.objects.get(user=request.user)
            Purchase.objects.create(
                product=product, user=request.user, count=int(request.POST["count"]),
                index=int(profile.index)
            )
            return render(
                request,
                "good.html",
                {"a": True,
                 "products": products,
                 "product": product,
                 "Text": text,
                 },
            )
            # count = int(request.POST["count"])
            # cart_add(request, kwargs["product_id"], count)

            # forma_log = LoginForm()
            # return redirect('/register', {"form": forma_log})
            form = filter_form
            return redirect('/catalog/', {"form": form})

    return render(
        request,
        "good.html",
        {
            "products": products,
            "product": product,
            "Text": text,
        },
    )

    # class Product_details_view(TemplateView):
    #     template_name = "good.html"
    #
    #     def get_context_data(self, **kwargs):
    #         product = Product.objects.get(id=kwargs["product_id"])
    #         text = Text.objects.get(id=4)
    #         request = self.request
    #
    #
    # if request.method == "POST":
    #     if request.user.is_authenticated:
    #         if request.user.is_staff:
    #             customer = Customer.objects.get(user=request.user)
    #             Purchase.objects.create(
    #                 product=product, user=request.user, count=int(request.POST["count"]),
    #                 index=int(customer.index)
    #             )
    #
    #             purchases = Purchase.objects.filter(user=request.user).order_by("-created_at")[0]
    #             if customer.foruser:
    #                 user = User.objects.get(id=(Order.objects.get(id=customer.foruser).user_id))
    #                 Order.objects.create(user=user,
    #                                      purchase=purchases,
    #                                      delivery=True,
    #                                      customer=customer,
    #                                      index=int(customer.index),
    #                                      )
    #                 Order.save(self=request.user)
    #             customer.foruser = None
    #             customer.save()
    #             return redirect("activeOrder_view", order_index=customer.foruser)
    #         else:
    #             profile = Profile.objects.get(user=request.user)
    #             Purchase.objects.create(
    #                 product=product, user=request.user, count=int(request.POST["count"]),
    #                 index=int(profile.index)
    #             )
    #             redirect("product_details_view", product_id=product.id)
    #     else:
    #         Login = random.randint(10000, 99999)
    #         request.user = User.objects.create(username=Login,
    #                                            password=1111)
    #         Profile.objects.create(user=request.user)
    #         Profile.save(self=request.user)
    #
    #         user = authenticate(request, username=Login,
    #                             password=1111)
    #         login(request, user)
    #         profile = Profile.objects.get(user=request.user)
    #         Purchase.objects.create(
    #             product=product, user=request.user, count=int(request.POST["count"]),
    #             index=int(profile.index)
    #         )
    #         redirect("product_details_view", product_id=product.id)
    #         # count = int(request.POST["count"])
    #         # cart_add(request, kwargs["product_id"], count)
    #
    #         # forma_log = LoginForm()
    #         # return redirect('/register', {"form": forma_log})
    #         form = filter_form
    #         return redirect('/catalog/', {"form": form})
    #
    # return {
    #     "product": product,
    #     "Text": text,
    # }


def basket(request):
    if request.user.is_authenticated:
        text = Text.objects.get(id=4)
        if request.user.is_staff:
            return render(
                request,
                "basket.html", {
                    "Text": text, })
        print(request.user)

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=request.user)
        print(profile.delivery)
        purchases = Purchase.objects.filter(user=request.user).filter(index=profile.index)
        form = BasketForm(request.POST)
        sum_product = 0
        count = 0
        for purchase in purchases:
            sum_product = sum_product + int(purchase.product.coast) * int(purchase.count)
            count = count + int(purchase.count)
            # purchase.index = int(purchase.index) + 1
            purchase.save()
        if request.POST.get('delete', ):
            purchas = purchases.get(id=int(request.POST['delete']))
            purchas.delete()
            purchases = Purchase.objects.filter(user=request.user).filter(index=profile.index)
        if request.method == "POST":
            if form.is_valid():

                print(form.cleaned_data["ch"])

                for purchase in purchases:
                    Order.objects.create(user=request.user,
                                         purchase=purchase,
                                         name=form.cleaned_data["username"],
                                         phone=form.cleaned_data["phone"],
                                         comment=form.cleaned_data["comment"],
                                         delivery=form.cleaned_data["ch"],
                                         index=int(request.user.profile.index),
                                         adress=form.cleaned_data["address"], )
                    Order.save(self=request.user)

                request.user.profile.name = form.cleaned_data["username"]
                request.user.profile.phone = form.cleaned_data["phone"]
                request.user.profile.delivery = form.cleaned_data["ch"]
                request.user.profile.adress = form.cleaned_data["address"]
                request.user.profile.comment = form.cleaned_data["comment"]
                request.user.profile.index = int(request.user.profile.index) + 1
                request.user.profile.save()
                form = BasketForm()

                return render(
                    request,
                    "basket.html",
                    {
                        "a": True,
                        "name": request.user.profile.name,
                        "phone": request.user.profile.phone,
                        "delivery": request.user.profile.delivery,
                        "address": request.user.profile.adress,
                        "comment": request.user.profile.comment,
                        "purhcase": purchases,
                        "form": form,
                        "sum": sum_product,
                        "result": count,
                        "Text": text,
                    }
                )
        form = BasketForm()
        return render(
            request,
            "basket.html",
            {
                "a": False,
                "name": request.user.profile.name,
                "phone": request.user.profile.phone,
                "delivery": profile.delivery,
                "address": request.user.profile.adress,
                "comment": request.user.profile.comment,
                "purhcase": purchases,
                "form": form,
                "sum": sum_product,
                "result": count,
                "Text": text,
            }
        )
    form = RegistrationForm()
    return redirect('/register', {"form": form})


def autorization(request):
    if request.user.is_staff:
        return redirect("/activeOrders")
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data.get('login'),
                                    password=form.cleaned_data.get('password'))
                if user:
                    login(request, user)
    form = LoginForm()
    return render(request, "autorization_admin.html", {"form": form})


def activeOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=1)
        # orders = Order.objects.filter(statuc=1).distinct("index", "user")
        return render(request, "activeOrders_admin.html",
                      {"orders": orders})
    else:
        return redirect("/")


def activeOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
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
            print(orde.delivery)
        if request.method == "POST":
            form = BasketForm(request.POST)
            if request.POST.get("action", "") == "add":
                customer = Customer.objects.get(user=request.user)
                customer.index = index
                foruser = Order.objects.get(id=kwargs["order_index"]).user_id
                customer.foruser = kwargs["order_index"]
                print(customer.foruser, user, foruser)
                customer.save()
                return redirect("/catalog/")
            elif request.POST.get("action", "") == "delete":
                customer = Customer.objects.get(user=request.user)
                for orde in orders:
                    orde.statuc = 3
                    orde.customer = customer
                    orde.save()
                return redirect("/activeOrders")
            elif request.POST.get("action", "") == "confirm":
                customer = Customer.objects.get(user=request.user)
                for orde in orders:
                    orde.customer = customer
                    orde.statuc = 2
                    orde.save()
                profile = Profile.objects.get(user_id=user)
                # print(form.cleaned_data["username"])
                print(form)
                if form.is_valid():
                    for order in orders:
                        orde.name = form.cleaned_data["username"]
                        orde.phone = form.cleaned_data["phone"]
                        if form.cleaned_data["ch"] == True:
                            orde.delivery = form.cleaned_data["ch"]
                            orde.adress = form.cleaned_data["address"]
                        else:
                            orde.delivery = False
                            orde.adress = ''
                        orde.comment = form.cleaned_data["comment"]
                        orde.save()
                return redirect("/activeOrders/")
            elif request.POST['delete']:
                orde = Order.objects.get(id=int(request.POST['delete']))
                orde.delete()
                orders = Order.objects.filter(user_id=user).filter(index=index)[0].id
                return redirect("activeOrder_view", order_index=orders)
        form = BasketForm()
        return render(
            request,
            "activeOrder_admin.html",
            {
                "punt": orders[0].delivery,
                "orders": orders,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": orders[0]
            },
        )
    return redirect("/")


def confirmedOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=2).distinct("index", "user")
        return render(request, "confirmedOrders_admin.html",
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
        sum = 0
        count = 0
        punt = 0
        for orde in orders:
            coast = 0
            coast = coast + int(orde.purchase.count) * int(orde.purchase.product.coast)
            orde.coast = coast
            count = count + int(orde.purchase.count)
            sum = sum + coast
            punt = orde.delivery
            orde.save()
        print(punt)
        if request.method == "POST":
            if request.POST["action"] == "delete":
                customer = Customer.objects.get(user=request.user)
                for orde in orders:
                    orde.customer = customer
                    orde.statuc = 3
                    orde.save()
                return redirect("/confirmedOrders/")
            elif request.POST["action"] == "vosstan":
                customer = Customer.objects.get(user=request.user)
                for orde in orders:
                    orde.customer = customer
                    orde.statuc = 1
                    orde.save()
                return redirect("/confirmedOrders/")
        return render(
            request,
            "confirmedOrder_admin.html",
            {
                "punt": punt,
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
        return render(request, "deletedOrders_admin.html",
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
                customer = Customer.objects.get(user=request.user)
                for orde in orders:
                    orde.customer = customer
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
            "deletedOrder_admin.html",
            {
                "orders": orders,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": profile,
            },
        )
    return redirect("/")


class ProductsView1(TemplateView):
    template_name = "goods1.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        products = Product.objects.all()
        products = products.filter(division=False)
        filter_forms = filter_form(self.request.GET)

        if filter_forms.is_valid():
            if filter_forms.cleaned_data["category"]:
                if filter_forms.cleaned_data["category"] == "Все" or filter_forms.cleaned_data["category"] == "":
                    a = 'Все'
                else:
                    category = Category.objects.get(Text=filter_forms.cleaned_data["category"])
                    a = filter_forms.cleaned_data["category"]
                    products = products.filter(category=category.id)
            if filter_forms.cleaned_data["way"] == "По популярности":
                b = 'По популярности'
                products = products.order_by("-popular")
            if filter_forms.cleaned_data["way"] == "По возростанию цены":
                b = "По возростанию цены"
                products = products.order_by("coast")
            if filter_forms.cleaned_data["way"] == "По убыванию цены":
                b = "По убыванию цены"
                products = products.order_by("-coast")
            if filter_forms.cleaned_data["min_price"]:
                c = filter_forms.cleaned_data["min_price"]
                products = products.filter(coast__gt=filter_forms.cleaned_data["min_price"] - 1)
            if filter_forms.cleaned_data["max_price"]:
                d = filter_forms.cleaned_data["max_price"]
                products = products.filter(coast__lt=filter_forms.cleaned_data["max_price"] + 1)
            a = filter_forms.cleaned_data["category"]
            b = filter_forms.cleaned_data["way"]
            c = filter_forms.cleaned_data["min_price"]
            d = filter_forms.cleaned_data["max_price"]
        else:
            a = 0
            b = 0
            c = 0
            d = 0
        print(a, b, c, d)
        categorys = Category.objects.all()
        filter_forms = filter_form()
        categorys = categorys.order_by("Text")
        return {"filter_forms": filter_forms,
                "products": products,
                "Text": text,
                "categorys": categorys,
                "category": a,
                "way": b,
                "min_price": c,
                "max_price": d,
                }


def logout_user(request):
    logout(request)
    return redirect("/")
