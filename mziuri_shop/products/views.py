from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F

from .forms import ProductForm
from .models import Product, Category, CartItem, Cart


def home(request):
    filters = dict()

    product_name = request.GET.get('product_name')
    if product_name:
        filters['name__icontains'] = product_name
    min_price = request.GET.get('min_price')
    if min_price:
        filters['price__gt'] = min_price
    max_price = request.GET.get('max_price')
    if max_price:
        filters['price__lt'] = max_price

    category = request.GET.get('category')
    if category:
        filters['category_id'] = category

    products = Product.objects.filter(**filters)
    sort = request.GET.get('sort')
    if sort:
        products = Product.objects.filter(**filters).order_by(sort)

    categories = Category.objects.all()
    return render(request, 'home.html', context={"products": products, 'categories': categories})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.views += 1
    product.save()

    return render(request, 'product.html', {'product': product})


def create_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your product was uploaded successfully.')
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, "Your product wasn't uploaded successfully.")
    return render(request, 'product_form.html', {'form': form})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product '{product.name}' was updated successfully.")
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, f"Product '{product.name}' wasn't updated successfully.")
    return render(request, 'product_form.html', {'form': ProductForm(instance=product), 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.add_message(request, messages.SUCCESS, f"Product '{product.name} was deleted successfully.")
    return redirect('home')


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html',{'cart': cart})


def add_product_to_cart(request, id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if not created:
        cart_item.qty += 1
        cart_item.save()
    messages.add_message(request, messages.SUCCESS, "Your product was added to a cart.")
    return redirect('product_detail', pk=id)


def remove_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    messages.add_message(request, messages.SUCCESS, 'cart item has been removed.')
    return redirect('cart_view')


def confirm_purchase(request):
    items = CartItem.objects.all()
    for i in items:
        print(i.product.id)
        product = Product.objects.filter(id=i.product.id)
        product.update(stock_qty=F('stock_qty') - 1)
        if product[0].stock_qty == 0:
            product.delete()
        i.delete()
    messages.add_message(request, messages.SUCCESS, 'Successfully Purchased.')
    return redirect('cart_view')
