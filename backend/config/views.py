from django.shortcuts import render, get_object_or_404

from products.models import Cake, Category, BakeryItem
from orders.models import CartItem, Address, Order


def home(request):

    bakery_items = BakeryItem.objects.filter(
        is_active=True
    ).order_by("created_at")

    return render(
        request,
        "home.html",
        {
            "bakery_items": bakery_items,
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