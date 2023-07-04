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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)

class Order(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    develivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True, auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')