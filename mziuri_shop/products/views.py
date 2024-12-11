from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', context={"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'product.html', {'product': product})
