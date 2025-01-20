from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .forms import OrderCreateForm


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/order_list.html', {'orders': orders})


@login_required
@transaction.atomic
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == "POST":
        order_create_form = OrderCreateForm(request.POST)
        if order_create_form.is_valid():
            order = order_create_form.save(commit=False)
            order.user = request.user
            order.created = timezone.now()
            order.updated = timezone.now()
            order.total_quantity = cart.total_quantity
            order.total_price = cart.total_price
            order.save()

            # Create OrderItem for each CartItem
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    cart_item=cart_item,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                    list_number=cart_item.list_number,
                )

            cart_items.delete()

            messages.success(request, "Your order has been successfully created!")
            return redirect('order:order_detail', order_id=order.id)
    else:
        order_create_form = OrderCreateForm()

    context = {
        'order_create_form': order_create_form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'order/order_create.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order/order_detail.html', context)