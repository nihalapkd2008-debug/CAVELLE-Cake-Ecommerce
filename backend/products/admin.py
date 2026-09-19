from django.contrib import admin

from .models import (
    Category,
    Cake,
    BakeryItem,
    BakeryGalleryImage,
)


admin.site.register(Category)

admin.site.register(Cake)

admin.site.register(BakeryItem)

admin.site.register(BakeryGalleryImage)