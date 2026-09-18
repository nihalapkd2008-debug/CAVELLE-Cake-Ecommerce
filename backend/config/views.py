from django.shortcuts import render, get_object_or_404

from products.models import Cake, Category
from orders.models import CartItem, Address, Order


def home(request):

    featured_cake = Cake.objects.filter(
        image__isnull=False,
        is_available=True,
        stock__gt=0
    ).first()

    categories = Category.objects.all()

    return render(
        request,
        "home.html",
        {
            "featured_cake": featured_cake,
            "categories": categories,
        }
    )


def products_page(request):

    cakes = Cake.objects.select_related(
        "category"
    ).all()

    category = request.GET.get("category")

    if category:
        cakes = cakes.filter(
            category__name__iexact=category
        )

    categories = Category.objects.all()

    return render(
        request,
        "products.html",
        {
            "cakes": cakes,
            "categories": categories,
        }
    )


def product_detail(request, cake_id):

    cake = get_object_or_404(
        Cake.objects.select_related("category"),
        id=cake_id
    )

    return render(
        request,
        "product-detail.html",
        {
            "cake": cake
        }
    )


def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def cart_page(request):
    return render(
        request,
        "cart.html",
        {
            "cart_items": [],
            "total": 0
        }
    )


def checkout_page(request):
    return render(
        request,
        "checkout.html",
        {
            "addresses": [],
            "cart_items": [],
            "total": 0
        }
    )


def orders_page(request):
    return render(
        request,
        "orders.html",
        {
            "orders": []
        }
    )


def staff_orders_page(request):
    return render(
        request,
        "staff-orders.html"
    )