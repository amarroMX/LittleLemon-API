from django.contrib import admin
from django.urls import path, include
from .views import (
    AllMenuItemView,
    SingleMenuItemView,
    ManagerGroupUserView,
    RemoveUserFromManagerView,
    RemoveUserFromDeliveryView,
    DeliveryGroupUserView,
    UserAllCartView,
)

urlpatterns = [
    path("menu-items", AllMenuItemView.as_view(), name="menu items"),
    path(
        "menu-item/<int:pk>",
        SingleMenuItemView.as_view(),
        name="single menu item",
    ),
    path(
        "groups/manager/users",
        ManagerGroupUserView.as_view(),
        name="manager group users",
    ),
    path(
        "groups/manager/users/<int:pk>",
        RemoveUserFromManagerView.as_view(),
        name="remove user from manager group",
    ),
    path(
        "groups/delivery-crew/users",
        DeliveryGroupUserView.as_view(),
        name="delivery crew group users"

    ),
    path(
        "groups/delivery-crew/users/<int:pk>",
        RemoveUserFromDeliveryView.as_view(),
        name="remove user from delivery crew group"
    ),
    path(
        "carts/menu-items", 
        UserAllCartView.as_view(),
        name="user carts"
    ),
]
