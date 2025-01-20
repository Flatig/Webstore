from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Defines how many empty rows to display by default in the inline form.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('list_number', 'user', 'status', 'total_quantity', 'total_price', 'created', 'updated')
    list_filter = ('status', 'user')  # Filter by status and user
    search_fields = ('user__username', 'status')  # Allows searching by username and status
    inlines = [OrderItemInline]  # Display OrderItems within the Order admin page
    actions = ['mark_as_shipped', 'mark_as_delivered']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, "Selected orders have been marked as shipped.")
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, "Selected orders have been marked as delivered.")
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'name', 'email', 'address', 'city', 'total_quantity', 'total_price')
        }),
        ('Important Dates', {
            'fields': ('created', 'updated')
        }),
    )
    readonly_fields = ('created', 'updated')  # Make 'created' and 'updated' read-only

# Custom admin for OrderItem to exclude the cart_item field
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'list_number')
    list_filter = ('order', 'product')  # Add filters for order and product
    search_fields = ('product__name', 'order__list_number')  # Search by product name and order number

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)