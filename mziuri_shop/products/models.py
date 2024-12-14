from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, default='product name')
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(default=datetime.now)
    write_time = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.ImageField(upload_to='products/', default='default.jpg')

    def __str__(self):
        return self.name
