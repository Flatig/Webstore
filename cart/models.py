from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum, F  # To perform operations at the database level.

from store.models import Product



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    total_quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total_list_numbers(self):
        return self.cartitem_set.count()

    def update_totals(self):
        totals = self.cartitem_set.aggregate(
            total_quantity=Sum('quantity'),
            total_price=Sum(F('quantity') * F('product__price'))
        )
        self.total_quantity = totals['total_quantity'] or 0
        self.total_price = totals['total_price'] or 0
        self.save()

    def __str__(self):
        return f'Cart {self.id} (User: {self.user.username})'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    list_number = models.PositiveIntegerField(default=1)


    class Meta:
        ordering = ['list_number']

    @transaction.atomic
    def save(self, *args, **kwargs):
        # Calculate the total price for the current cart item
        self.price = self.quantity * self.product.price

        # Check if the object is being created
        if self._state.adding:
            # Get the last item in the cart for the current user, sorted by descending list_number
            last_item = CartItem.objects.filter(cart=self.cart).order_by('-list_number').first()

            # Set the order number for the new cart item
            if last_item:
                # If the cart is not empty, increment the last item's list_number by 1
                self.list_number = last_item.list_number + 1
            else:
                # If the cart is empty, the new item's list_number will be 1
                self.list_number = 1

        # Save the object with the updated data
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        remaining_items = CartItem.objects.filter(cart=self.cart).order_by('list_number')
        for i, item in enumerate(remaining_items, start=1):
            item.list_number = i
            item.save()

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
