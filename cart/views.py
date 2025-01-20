from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction
from django.http import HttpResponseRedirect

from store.models import Category, Product
from .models import Cart, CartItem


@login_required
def cart_list(request):
    # Get the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get all the items in the user's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate totals in cart/models.py
    total_list_number = cart.total_list_numbers()

    cart.update_totals()


    return render(request, 'cart/cart_list.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_list_number': total_list_number,
        'total_quantity': cart.total_quantity,
        'total_price': cart.total_price,
    })


@login_required
@transaction.atomic
def cart_add(request, product_slug):
    # Get the product by slug or return 404 if not found
    product = get_object_or_404(Product, slug=product_slug)

    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create the cart item for the specified product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Set the quantity to 1
    cart_item.quantity = 1
    cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def cart_update(request, product_slug):
    # Get the cart item for the specified product
    cart_item = get_object_or_404(CartItem, product__slug=product_slug, cart__user=request.user)

    # Get the quantity of the product from the POST request (default is 1)
    quantity = int(request.POST.get('quantity', 1))

    # If the quantity is greater than 0, update the quantity of the item in the cart
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart:cart_list')


@login_required
@transaction.atomic
def cart_remove(request, product_slug):
    cart_item = get_object_or_404(CartItem, product__slug=product_slug, cart__user=request.user)
    cart_item.delete()  # Look in cart/models.py

    return redirect('cart:cart_list')
