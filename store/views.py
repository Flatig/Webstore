from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

from .forms import SearchForm
from .models import Category, Product
from cart.models import Cart, CartItem


# Get products in the current user's cart to add the selected product to the cart
def get_cart_products(user):
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        return [item.product for item in cart_items]
    return []


def store_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    cart_products = get_cart_products(request.user)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    search_form = SearchForm(request.GET or None)

    context = {
        'category': category,
        'category_slug': category.slug if category else None,
        'categories': categories,
        'page_obj': products_page,
        'cart_products': cart_products,
        'search_form': search_form,
    }
    return render(request, 'store/store_list.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart_products = get_cart_products(request.user)

    return render(
        request,
        'store/product_detail.html',
        {'product': product, 'cart_products': cart_products},
    )


def store_search(request):
    search_form = SearchForm(request.GET)
    products = []
    num_results = 0

    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        if search:
            products = Product.objects.annotate(
                similarity_name=TrigramSimilarity('name', search),
            ).filter(
                Q(similarity_name__gt=0.1)
            ).order_by('-similarity_name').distinct()

            num_results = products.count()
            message = (
                f"{num_results} product{'' if num_results == 1 else 's'} found."
                if num_results > 0
                else "No products found."
            )
            messages.success(request, message)

    context = {
        'products': products,
        'num_results': num_results,
        'search_form': search_form,
    }
    return render(request, 'store/store_search.html', context)