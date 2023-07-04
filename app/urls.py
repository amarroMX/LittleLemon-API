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
    OrderDetailView,
    AllOrdersView
)

urlpatterns = [
    path("menu-items", AllMenuItemView.as_view(), name="menu-items"),
    path(
        "menu-item/<int:pk>",
        SingleMenuItemView.as_view(),
        name="menu-items-detail",
    ),
    path(
        "groups/manager/users",
        ManagerGroupUserView.as_view(),
        name="users-add-manager-group",
    ),
    path(
        "groups/manager/users/<int:pk>",
        RemoveUserFromManagerView.as_view(),
        name="users-remove-manager-group",
    ),
    path(
        "groups/delivery-crew/users",
        DeliveryGroupUserView.as_view(),
        name="users-add-delivery-group",
    ),
    path('groups/delivery-crew/users/<int:pk>',
         RemoveUserFromDeliveryView.as_view(),
         name="users-remove-delivery-group"),
    path(
        "groups/delivery-crew/users/<int:pk>",
        RemoveUserFromDeliveryView.as_view(),
        name="users-remove-delivery-group",
    ),
    path("carts/menu-items", UserAllCartView.as_view(), name="carts"),
    path('orders/', AllOrdersView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='orders-detail'),

]
