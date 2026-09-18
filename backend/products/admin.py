from django.contrib import admin

from .models import Category, Cake, BakeryItem


admin.site.register(Category)
admin.site.register(Cake)
admin.site.register(BakeryItem)