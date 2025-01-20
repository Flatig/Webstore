from django.db import models, transaction
from store.models import Product
from django.utils import timezone
from django.contrib.auth.models import User

from cart.models import CartItem


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('processing', '🔄 Processing'),
        ('shipped', '🚚 Shipped'),
        ('delivered', '✅ Delivered'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    total_quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    list_number = models.PositiveIntegerField(default=1)
    # Recipient data:
    name = models.CharField(max_length=50, default='Name')
    email = models.EmailField(default='example@example.com')
    address = models.CharField(max_length=250, default='Address')
    city = models.CharField(max_length=100, default='City')

    class Meta:
        ordering = ['list_number']


    @transaction.atomic
    def save(self, *args, **kwargs):
        # Set the order list_number for the new order based on the user
        if self._state.adding:  # Check if the order is being created
            last_order = Order.objects.filter(user=self.user).order_by('-list_number').first()
            if last_order:
                # If there are previous orders, increment the last one's list_number
                self.list_number = last_order.list_number + 1
            else:
                # If no orders exist for the user, the new order gets list_number 1
                self.list_number = 1

        # Save the order with the updated data
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.list_number} - {self.get_status_display()} - {self.name} ({self.total_quantity} items, ${self.total_price})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    list_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['list_number']

    def __str__(self):
        return f"OrderItem #{self.list_number} - {self.product.name} x {self.quantity} - ${self.price}"
