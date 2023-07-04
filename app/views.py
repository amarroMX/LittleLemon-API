from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, UserSerializer, OrderSerializer
from .permissions import EditDeleteOnlyManagerOrAdmin, UserAllOnlyManagerOrAdmin
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404



class AllMenuItemView(ListCreateAPIView):
    """List all menu items or add new menu item"""

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, EditDeleteOnlyManagerOrAdmin]


class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    """Get , update or delete menu item"""

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, EditDeleteOnlyManagerOrAdmin]


class ManagerGroupUserView(ListCreateAPIView):
    """Get all user in manager group or assign user to the group"""

    queryset = User.objects.filter(groups__name__in=["Manager"])
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserAllOnlyManagerOrAdmin]

    def create(self, request, *args, **kwargs):
        """assigin provided user to Manager group"""
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=user_serializer.data["id"])
        manager_group = Group.objects.get(name="Manager")

        if user.groups.get(name="Manager").exists():
            message = {"message": f"user {user.username} already in the group manager."}

        manager_group.user_set.add(user)
        message = {
            "message": f"user {user.username} add to {manager_group.name} group."
        }
        return Response(data=message, status=201)


class RemoveUserFromManagerView(DestroyAPIView):
    """Remove user from manager group"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserAllOnlyManagerOrAdmin]

    def delete(self, request, *args, **kwargs):
        """remove a user from the manager group"""
        user_id = request.params["id"]
        user = User.objects.filter(groups__name__in=["Manager"]).get(id=user_id)

        if not user:
            message = {"message": "user with id {user_id} not found in group manager"}
            return Response(data=message, status=404)

        group_manager = user.groups.filter(name="Manager")

        group_manager.user_set.remove(user)
        message = {
            "message": f"successfuly remove {user.username} from {group_manager.name} group",
        }
        return Response(data=message, status=200)


class DeliveryGroupUserView(ListCreateAPIView):
    """Get all user in delivery crew group or assing user to the group"""

    queryset = User.objects.filter(groups__name__in=["Delivery Crew"])
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserAllOnlyManagerOrAdmin]

    def create(self, request, *args, **kwargs):
        """assign specific user to delivery crew group, if not return 404"""

        id = request.data["id"]
        user = User.objects.filter(id=id).first()
        if not user:
            message = {"message": f"user {id} does not exit."}
            return Response(data=message, status=404)

        group_delivery = user.groups.filter(name="Delivery Crew")

        if not group_delivery:
            group_delivery.user_set.add(user)
            message = {
                "message": f"user {user.username} add to {group_delivery.name} group."
            }
            return Response(data=message, status=201)

        message = {
            "message": f"user {user.user.name} already in {group_delivery.name} group."
        }
        return Response(data=message, status=400)


class RemoveUserFromDeliveryView(DestroyAPIView):
    """Remove user from delivery crew"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserAllOnlyManagerOrAdmin]

    def delete(self, request, *args, **kwargs):
        """remove a user from the delivery crew group"""
        user_id = request.params["id"]
        user = User.objects.filter(groups__name__in=["Delivery"]).get(id=user_id)

        if not user:
            message = {
                "message": "user with id {user_id} not found in group dlivery crew"
            }
            return Response(data=message, status=404)

        delivery_manager = user.groups.filter(name="Delivery")

        delivery_manager.user_set.remove(user)
        message = {
            "message": f"successfuly remove {user.username} from {delivery_manager.name} group",
        }
        return Response(data=message, status=200)


class UserAllCartView(ListCreateAPIView, DestroyAPIView):
    """List carts for current user or delete cart for user"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user).prefetch_related()

    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        message = {'message': f"sucessfully delete carts for {request.user.username}"}
        return Response(data=message, status=200)
    
class AllOrdersView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if(user.groups.filter(name="manager").exists()):
            return Order.objects.all().prefetch_related()
        elif(user.groups.filter(name='delivery').exists()):
            return Order.objects.filter(delivery_crew=user).prefetch_related()
        else:
            return Order.objects.all().filter(user=user).prefetch_related()
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        staff_group = user.groups.filter(name__in=['deliveryman','manager'])
        
        if(staff_group.exists()):
            message = {"message": "manager or delivery staff can only modified user's orders"}
            return Response(data=message, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = Cart.objects.all().filter(user=user)

        if(not cart_items):
                message = {"message": f"user {user.username} shopping chart empty"} 
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
       
        order = Order.objects.create(user=user)
        total = 0
        for cart in cart_items:
            total += cart.total
            orderItem = OrderItem.objects.create(order=order,
                                                menuitem=cart.menu_item,
                                                quantity=cart.quantity,
                                                unit_price=cart.price,
                                                price=cart.total)
            orderItem.save()
        order.total = total
        order.save()
        cart_items.all().delete()
        serializer = OrderSerializer(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(RetrieveUpdateAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]         
    
