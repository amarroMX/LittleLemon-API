from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_field = ["id", "slug"]

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"])
        category, _ = Category.objects.get_or_create(**validated_data)
        return category


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "featured", "category"]
        read_only_fields = ["category"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "groups"]
        read_only_fields = ["username", "groups"]
        depth = 1

class UsernameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ["id","username", "group_name"]
        depth = 1



class CartSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all().values_list('id', flat=True), write_only=True)
    price = serializers.DecimalField(decimal_places=2, max_digits=6, read_only=True)


    class Meta:
        model = Cart
        fields = ["id", "user", "menu_item_id", "price", "total", "quantity", "menu_item"]
        read_only_fields = ["id", "total", "user", "menu_item", "user", "price", "owner"]
    


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['price'] = self.get_price(self,id=validated_data['menu_item_id'])
        validated_data["total"] = validated_data["price"] * validated_data["quantity"]
        cart = Cart.objects.create(**validated_data)
        return cart
    
    def get_price(self, obj, id):
        price = MenuItem.objects.get(id=id).price
        return price

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'delivery_crew', 'status', 'date', 'total')
        read_only_fields = ('user', 'delivery_crew', 'status', 'date', 'total')



