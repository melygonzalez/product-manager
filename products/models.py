from django.db import models


STATUS_LIST = [
    ('AC', 'ACTIVE'),
    ('IN', 'INACTIVE')]


class Category(models.Model):
    name = models.CharField(max_length=20, help_text="Enter category name")


class Product(models.Model):
    name = models.CharField(max_length=30, help_text="Enter product name")
    status = models.CharField(max_length=15, help_text="Enter product status", choices=STATUS_LIST, default='AC')
    categories = models.ManyToManyField(Category)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.URLField(help_text="Enter product image link")
