from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import ProductForm
from .models import Product, Category


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
