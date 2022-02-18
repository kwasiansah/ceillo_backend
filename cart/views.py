from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from cart.serializers import CartSerializer, CartItemSerializer
from .models import CartItem
from product.models import Product
from .utils.helper_func import get_or_create_cart

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(user=request.user)
        serializer = CartSerializer(cart)
        data = {
            "data":serializer.data,
        }
        return Response(data, status.HTTP_200_OK)
    
    def post(self, request):
        cart = get_or_create_cart(user=request.user)
        product = Product.objects.filter(url_slug=request.data["url_slug"]).last()
        if not product:
            return Response({"data":"product with this url does not exist"}, status.HTTP_404_NOT_FOUND)
        update = CartItem.objects.filter(product=product, cart=cart).last()
        if update:
            serializer = CartItemSerializer(update, data={"quantity":int(request.data["quantity"])}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {
                "data": serializer.data,
                "message": "cart item successfully updated"
            }
            return Response(data, status.HTTP_200_OK)

        serializer = CartItemSerializer(data={"quantity": int(request.data["quantity"])})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, cart=cart)
        data = {
            "data":serializer.data,
            "message": "cart item successfully created"
        }
        return Response(data, status.HTTP_200_OK)
        
    def delete(self, request):
        cart = get_or_create_cart(user=request.user)
        product = Product.objects.filter(
            url_slug=request.data["url_slug"]).last()
        if not product:
            return Response({"data": "product with this url does not exist"}, status.HTTP_404_NOT_FOUND)
        cartitem = CartItem.objects.filter(product=product, cart=cart).last()
        if not cartitem:
            return Response({"message":"cart item not created"} , status.HTTP_404_NOT_FOUND)
        cartitem.delete()
        return Response({"message":"deleted item"}, status.HTTP_404_NOT_FOUND)
        