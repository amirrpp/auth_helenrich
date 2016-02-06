from django.contrib import admin
from webshopcart.models import *


class ProductInCartInline(admin.TabularInline):
    model = ProductInCart
    extra = 0


class ProductCartAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'status', 'all_products', 'date_on_add', 'sum', 'fixed_sum')
    inlines = (ProductInCartInline, )


admin.site.register(ProductInCart)
admin.site.register(ProductCart, ProductCartAdmin)
