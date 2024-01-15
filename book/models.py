from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='products', blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=125)

    def __str__(self):
        return self.title


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, blank=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.text}'
