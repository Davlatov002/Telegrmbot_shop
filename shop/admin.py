from django.contrib import admin
from .models import Category, Product, Order
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('display_image',)

    def display_image(self, obj):
        return format_html('<img src="{}" width="300" height="300" />'.format(obj.image.url))

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('name','price', 'data')
    readonly_fields = ['data']
    list_filter = ('data', 'user_id', 'product_id')

    def name(self, obj):
            return obj.user_id.first_name


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderModelAdmin)
