from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255, unique=True, db_index=True)


class MenuItem(models.Model):
    title = models.CharField(max_length=255, unique=True, db_index=True)
    featured = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
