from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # This defines how many empty rows to display by default in the inline form.


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_quantity', 'total_price')
    search_fields = ('user__username',)  # Allows searching by username
    inlines = [CartItemInline]  # To display CartItems within the Cart admin form


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price', 'list_number')
    list_filter = ('cart', 'product')  # Adds filters for the cart and product
    search_fields = ('product__name',)  # Allows searching by product name


# Register the models with the admin site
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)