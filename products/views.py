from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', context={"products": products})


def product_detail(request):
    return render(request, 'product.html')