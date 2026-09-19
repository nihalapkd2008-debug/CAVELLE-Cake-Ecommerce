from django.shortcuts import render, get_object_or_404

from products.models import Cake, Category, BakeryItem
from orders.models import CartItem, Address, Order


# =========================================
# HOME PAGE
# =========================================

def home(request):

    bakery_items = BakeryItem.objects.filter(
        is_active=True
    ).order_by("created_at")

    featured_cakes = Cake.objects.filter(
        is_available=True
    ).order_by("-created_at")[:4]

    return render(
        request,
        "home.html",
        {
            "bakery_items": bakery_items,
            "featured_cakes": featured_cakes,
        }
    )


# =========================================
# BAKERY GALLERY
# =========================================

def bakery_gallery(request, item_id):

    item = get_object_or_404(
        BakeryItem,
        id=item_id,
        is_active=True
    )

    gallery_images = item.gallery_images.all()

    return render(
        request,
        "bakery-gallery.html",
        {
            "item": item,
            "gallery_images": gallery_images,
        }
    )


# =========================================
# PRODUCTS PAGE
# =========================================

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


# =========================================
# PRODUCT DETAIL
# =========================================

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


# =========================================
# LOGIN
# =========================================

def login_page(request):

    return render(
        request,
        "login.html"
    )


# =========================================
# REGISTER
# =========================================

def register_page(request):

    return render(
        request,
        "register.html"
    )


# =========================================
# CART
# =========================================

def cart_page(request):

    return render(
        request,
        "cart.html",
        {
            "cart_items": [],
            "total": 0
        }
    )


# =========================================
# CHECKOUT
# =========================================

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


# =========================================
# ORDERS
# =========================================

def orders_page(request):

    return render(
        request,
        "orders.html",
        {
            "orders": []
        }
    )


# =========================================
# WISHLIST
# =========================================

def wishlist_page(request):

    return render(
        request,
        "wishlist.html"
    )


# =========================================
# STAFF ORDERS
# =========================================

def staff_orders_page(request):

    return render(
        request,
        "staff-orders.html"
    )