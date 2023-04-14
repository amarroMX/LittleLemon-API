from rest_framework import serializers
from .models import Category, MenuItem , Cart
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
        fields = ["id","username","groups"]
        read_only_fields = ["username", "groups"]
        depth = 1 


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menu_item = MenuItemSerializer()
    price = serializers.RelatedField(queryset=MenuItem.objects.all().values('price'))

    class Meta:
        model = Cart
        fields = ['id','user','menu_item','price','quantity', 'total']
        read_only_fields = ['id','price','total', 'user']

    def create(self, validated_data):
        validated_data['user'] = serializers.CurrentUserDefault()
        validated_data['total'] = validated_data['price'] * validated_data['quantity']
        cart = Cart.objects.create(**validated_data)
        return cart
