from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from ferumbel.models import Contacts, Photos, Benefits, Text, Product, Timetable, Purchase, Category, Profile, Order, \
    Customer, Image, Characteristic, Curs
from django.views.generic import TemplateView
from ferumbel.forms import RegistrationForm, BasketForm, LoginForm, filter_form
from django.contrib.auth import authenticate, login, logout
import random

logger = logging.getLogger(__name__)


def page_not_found_view(request, exception):
    products = Product.objects.all()
    text = Text.objects.get(id=4)
    return render(request, 'mistake.html', {"Text": text,
                                            "product": products
                                            }, status=404)


def get_sitemap(request):
    return render(request, "sitemap.xml")


def get_robots(request):
    return render(request, "robots.txt")


def get_file(request):
    filename = "Login_and_password.txt"
    content = "Добрый день, компания Ферумбел заботится, чтобы Вы не потеряли логин и пороль для последующего входа." + "\n" + "Логин: " + str(
        request.user) + "\n" + "Пароль: " + str(request.user.password)
    response = HttpResponse(str(content), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def register_view(request):
    products = Product.objects.all()
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
                                                           "product": products,
                                                           "Text": text, })
    else:
        form = LoginForm()
        # form = RegistrationForm()
    return render(request, "registration_start.html", {"form": form,
                                                       "product": products,
                                                       "Text": text, })


class CategorysView(TemplateView):
    template_name = "categorys.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        category = Category.objects.all()
        category = category.filter(division=True)
        products = Product.objects.all()
        z = category[0].division
        return {"products": category,
                "Text": text,
                "z": z,
                "product": products,
                }


class CategorysView1(TemplateView):
    template_name = "categorys.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        category = Category.objects.all()
        category = category.filter(division=False)
        products = Product.objects.all()

        z = category[0].division
        return {"products": category,
                "Text": text,
                "z": z,
                "product": products,
                }


class ProductsView(TemplateView):
    template_name = "goods.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        products = Product.objects.all()
        product = products
        products = products.filter(division=True)
        filter_forms = filter_form(self.request.GET)
        curs = Curs.objects.get(id=1).value

        if filter_forms.is_valid():
            if filter_forms.cleaned_data["category"]:
                if filter_forms.cleaned_data["category"] == "Все" or filter_forms.cleaned_data["category"] == "":
                    a = 0
                else:
                    poe = filter_forms.cleaned_data["category"]
                    category = Category.objects.get(Text=poe)
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
        categorys = Category.objects.all()
        categorys = categorys.order_by("Text")
        filter_forms = filter_form()
        return {"filter_forms": filter_forms,
                "products": products,
                "product": product,
                "Text": text,
                "categorys": categorys,
                "category": a,
                "way": b,
                "min_price": c,
                "max_price": d,
                "curs": curs,
                }


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        image = Image.objects.all()
        text = Text.objects.all()
        benefits = Benefits.objects.all()
        # photo = Photos.objects.all()
        product = Product.objects.all().order_by("-popular")[0:3]
        products = Product.objects.all()
        # product = product.objects.order_by("popular")
        category = Category.objects.all().order_by("-is_main")[0:3]
        # category = category.filter(name="is_main").order_by("-is_main")
        return {
            "photo": image,
            "benefits": benefits,
            "text": text.get(id=1),
            # "photo": photo.get(id=1),
            'product': products,
            "products": product,
            "categorys": category,
            "Text": text.get(id=4),
        }


def category_view(request, *args, **kwargs):
    categorys = Category.objects.all()
    text = Text.objects.get(id=4)
    category = Category.objects.get(id=kwargs["category_id"])
    product = Product.objects.all().filter(category=category)
    # print(product[0].division)
    # tovar = product[0].division
    if category.division:
        url = '/catalog/?category=' + category.Text + '&way=По+популярности&min_price=&max_price='

    else:
        url = '/catalog1/?category=' + category.Text + '&way=По+популярности&min_price=&max_price='
    return redirect(url)


def transport_index_to_topycs(request, *args, **kwargs):
    product = Product.objects.get(id=kwargs["product_id"])
    category = product.category
    if category == True:
        return render(
            request,
            "goods1.html",
            {
                "product": product,
                "category": category,
            },
        )
    pass


class Contact(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        contacts = Contacts.objects.all()
        text = Text.objects.get(id=4)
        return {
            'product': products,
            "contacts": contacts,
            "Text": text,
        }


class AboutUs(TemplateView):
    template_name = "aboutUs.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.all()
        products = Product.objects.all()
        timetable = Timetable.objects.all().order_by("position")
        return {
            'product': products,
            "contacts": timetable,
            "texts": text.get(id=3),
            "text": text.get(id=2),
            "Text": text.get(id=4),
        }


def product_details_view(request, *args, **kwargs):
    product = Product.objects.get(id=kwargs["product_id"])
    har = Characteristic.objects.all().filter(product=product)
    curs = Curs.objects.get(id=1).value
    print('-----')
    # print(product, product.charact)
    for characteristic in har:
        print(characteristic.pole, characteristic.value)
        print(product.category.id)
    print('------')
    product.popular += 1
    product.save()
    text = Text.objects.get(id=2)
    products = Product.objects.all()
    photos = Photos.objects.all().filter(product=product)
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.is_staff:
                customer = Customer.objects.get(user=request.user)
                user = User.objects.get(id=customer.foruser)
                Purchase.objects.create(
                    product=product, user=user, count=int(request.POST["count"]),
                    index=int(customer.index)
                )
                order = Order.objects.get(user=user, index=customer.index)
                return redirect("activeOrder_view", order_index=order.id)
                # url = '/activeOrder/' + str(order)
                # return redirect(url,order_index=order.id)
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
                        "photos": photos,
                        "products": product,
                        "product": products,
                        "Text": text,
                        "hars": har,
                        "curs": curs,
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
                 "photos": photos,
                 "products": product,
                 "product": products,
                 "Text": text,
                 "hars": har,
                 "curs": curs,
                 },
            )
            form = filter_form
            return redirect('/catalog/', {"form": form})

    return render(
        request,
        "good.html",
        {
            "photos": photos,
            "products": product,
            "product": products,
            "Text": text,
            "hars": har,
            "curs": curs,
        },
    )


def basket(request):
    product = Product.objects.all()
    if request.user.is_authenticated:
        text = Text.objects.get(id=2)
        if request.user.is_staff:
            return render(
                request,
                "basket.html", {
                    "Text": text,
                    "product": product,

                })

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=request.user)
        purchases = Purchase.objects.filter(user=request.user).filter(index=profile.index)
        form = BasketForm(request.POST)
        sum_product = 0
        count = 0

        if request.method == "POST":
            if request.POST.get('delete', ):
                purchas = purchases.get(id=int(request.POST['delete']))
                purchas.delete()
                purchases = Purchase.objects.filter(user=request.user).filter(index=profile.index)
                return render(
                    request,
                    "basket.html",
                    {
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
                        "product": product,
                    }
                )
        for purchase in purchases:
            sum_product = sum_product + int(purchase.product.coast) * int(purchase.count)
            count = count + int(purchase.count)
            # purchase.index = int(purchase.index) + 1
            purchase.save()
            if form.is_valid():
                Order.objects.create(user=request.user,
                                     purchase=purchases[0],
                                     name=form.cleaned_data["username"],
                                     phone=form.cleaned_data["phone"],
                                     comment=form.cleaned_data["comment"],
                                     delivery=form.cleaned_data["ch"],
                                     index=int(request.user.profile.index),
                                     adress=form.cleaned_data["address"], )
                Order.save(self=request.user)
                # for purchase in purchases:
                # Order.objects.create(user=request.user,
                #                      purchase=purchase,
                #                      name=form.cleaned_data["username"],
                #                      phone=form.cleaned_data["phone"],
                #                      comment=form.cleaned_data["comment"],
                #                      delivery=form.cleaned_data["ch"],
                #                      index=int(request.user.profile.index),
                #                      adress=form.cleaned_data["address"], )
                # Order.save(self=request.user)

                request.user.profile.name = form.cleaned_data["username"]
                request.user.profile.phone = form.cleaned_data["phone"]
                request.user.profile.delivery = form.cleaned_data["ch"]
                request.user.profile.adress = form.cleaned_data["address"]
                request.user.profile.comment = form.cleaned_data["comment"]
                request.user.profile.index = int(request.user.profile.index) + 1
                request.user.profile.save()
                form = BasketForm()
                punt = profile.delivery

                return render(
                    request,
                    "basket.html",
                    {
                        "a": True,
                        "punt": punt,
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
        punt = profile.delivery
        return render(
            request,
            "basket.html",
            {
                "punt": punt,
                "name": request.user.profile.name,
                "phone": request.user.profile.phone,
                # "delivery": profile.delivery,
                "address": request.user.profile.adress,
                "comment": request.user.profile.comment,
                "purhcase": purchases,
                "form": form,
                "sum": sum_product,
                "result": count,
                "Text": text,
                "product": product,
            }
        )
    else:
        form = RegistrationForm()
        return redirect('/register', {"form": form})


def autorization(request):
    if request.user.is_staff:
        if Customer.objects.filter(user=request.user).exists():
            return redirect("/activeOrders")
        else:
            Customer.objects.create(user=request.user)
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
        return render(request, "activeOrders_admin.html",
                      {"orders": orders})
    else:
        return redirect("/")


def activeOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
        user = Order.objects.get(id=kwargs["order_index"]).user_id
        index = Order.objects.get(id=kwargs["order_index"]).index
        purchases = Purchase.objects.filter(user_id=user).filter(index=index)
        order = Order.objects.all().get(id=kwargs["order_index"])
        profile = User.objects.get(id=user)
        profile = Profile.objects.get(user=profile)
        print(order.user_id)
        # index = int(Order.objects.filter(index=kwargs["order_index"])[0].index)
        if request.method == "POST":
            form = BasketForm(request.POST)

            if request.POST.get("action", "") == "add":  # Добавление нового товара
                customer = Customer.objects.get(user=request.user)
                customer.index = index
                foruser = Order.objects.get(id=kwargs["order_index"]).user_id
                customer.foruser = foruser
                print(customer.foruser, user, foruser)
                customer.save()
                return redirect("/catalog/")

            elif request.POST.get("action", "") == "delete":  # Удаление заказа
                customer = Customer.objects.get(user=request.user)
                order.statuc = 3
                order.customer = customer
                order.save()
                return redirect("/activeOrders")

            elif request.POST.get("action", "") == "confirm":  # Подтверждение заказа
                customer = Customer.objects.get(user=request.user)
                order.customer = customer
                order.statuc = 2
                order.save()
                profile = Profile.objects.get(user_id=user)
                if form.is_valid():
                    order.name = form.cleaned_data["username"]
                    order.phone = form.cleaned_data["phone"]
                    if form.cleaned_data["ch"] == True:
                        order.delivery = form.cleaned_data["ch"]
                        order.adress = form.cleaned_data["address"]
                    else:
                        order.delivery = False
                        order.adress = 'Фоминых 46/2-1'
                    order.comment = form.cleaned_data["comment"]
                    order.save()
                return redirect("/activeOrders/")

            elif request.POST['delete']:  # Удаление товара в заказе
                purch = Purchase.objects.get(id=int(request.POST['delete']))
                purch.delete()
                purchases = Purchase.objects.filter(user_id=user).filter(index=index)
        form = BasketForm()
        sum = 0
        count = 0
        for purchase in purchases:
            coast = 0
            coast = coast + int(purchase.count) * int(purchase.product.coast)
            count = count + int(purchase.count)
            purchase.coast = coast
            sum = sum + coast
        order.coast = sum
        order.save()
        return render(
            request,
            "activeOrder_admin.html",
            {
                "punt": order.delivery,
                "purchases": purchases,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": order,
            },
        )
    return redirect("/")


def confirmedOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=2)
        return render(request, "confirmedOrders_admin.html",
                      {"orders": orders})
    else:
        return redirect("/")


def confirmedOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
        user = Order.objects.get(id=kwargs["order_index"]).user_id
        index = Order.objects.get(id=kwargs["order_index"]).index
        order = Order.objects.all().get(id=kwargs["order_index"])
        purchases = Purchase.objects.filter(user_id=user).filter(index=index)
        profile = User.objects.get(id=user)
        profile = Profile.objects.get(user=profile)
        if request.method == "POST":
            if request.POST["action"] == "delete":
                customer = Customer.objects.get(user=request.user)
                order.customer = customer
                order.statuc = 3
                order.save()
                return redirect("/confirmedOrders/")
            elif request.POST["action"] == "vosstan":
                customer = Customer.objects.get(user=request.user)
                order.customer = customer
                order.statuc = 1
                order.save()
                return redirect("/confirmedOrders/")

        sum = 0
        count = 0
        for purchase in purchases:
            coast = 0
            coast = coast + int(purchase.count) * int(purchase.product.coast)
            count = count + int(purchase.count)
            purchase.coast = coast
            sum = sum + coast
        order.coast = sum
        order.save()
        return render(
            request,
            "confirmedOrder_admin.html",
            {
                "punt": order.delivery,
                "purchases": purchases,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": order,
            },
        )
    return redirect("/")


def deletedOrders(request):
    if request.user.is_staff:
        orders = Order.objects.filter(statuc=3)
        return render(request, "deletedOrders_admin.html",
                      {"orders": orders})
    else:
        return redirect("/")


def deletedOrder_view(request, *args, **kwargs):
    if request.user.is_staff:
        user = Order.objects.get(id=kwargs["order_index"]).user_id
        index = Order.objects.get(id=kwargs["order_index"]).index
        order = Order.objects.all().get(id=kwargs["order_index"])
        purchases = Purchase.objects.filter(user_id=user).filter(index=index)
        profile = User.objects.get(id=user)
        profile = Profile.objects.get(user=profile)
        if request.method == "POST":
            if request.POST["action"] == "vosstan":
                customer = Customer.objects.get(user=request.user)
                order.customer = customer
                order.statuc = 2
                order.save()
                return redirect("/deletedOrders")
        sum = 0
        count = 0
        for purchase in purchases:
            coast = 0
            coast = coast + int(purchase.count) * int(purchase.product.coast)
            count = count + int(purchase.count)
            purchase.coast = coast
            sum = sum + coast
        order.coast = sum
        order.save()
        return render(
            request,
            "deletedOrder_admin.html",
            {
                "purchases": purchases,
                "sum": sum,
                "count": count,
                "index": index,
                "profile": order,
            },
        )
    return redirect("/")


class ProductsView1(TemplateView):
    template_name = "goods1.html"

    def get_context_data(self, **kwargs):
        text = Text.objects.get(id=4)
        products = Product.objects.all()
        product = products
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
        categorys = Category.objects.all()
        categorys = categorys.order_by("Text")
        filter_forms = filter_form()
        return {"filter_forms": filter_forms,
                "products": products,
                "product": product,
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
