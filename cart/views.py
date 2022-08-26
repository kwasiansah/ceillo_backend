from django.core.serializers import serialize
from django.db.models.query import Q
from product.models import Product
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.serializers import CartItemSerializer, CartSerializer

from .models import CartItem
from .utils.helper_func import get_or_create_cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(user=request.user)
        serializer = CartSerializer(cart, context={"request": request})
        data = {
            "data": serializer.data,
        }
        return Response(data, status.HTTP_200_OK)

    def post(self, request):
        cart = get_or_create_cart(user=request.user)
        cart_items = request.data["cart_items"]
        saved_items = []
        CartItem.objects.filter(cart=cart).delete()

        for item in cart_items:
            product = Product.objects.filter(url_slug=item["url_slug"]).last()
            if not product:
                return Response(
                    {"data": "product with this url does not exist"},
                    status.HTTP_404_NOT_FOUND,
                )

            serializer = CartItemSerializer(
                data={"quantity": int(item["quantity"])}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product, cart=cart)
            saved_items.append(serializer.data)
        data = {
            "data": saved_items,
            "message": "Cart Item Successfully Updated",
        }
        return Response(data, status.HTTP_200_OK)
