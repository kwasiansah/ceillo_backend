from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity", "product", "cart"]
        read_only_fields = ["product", "cart"]
    
class CartSerializer(serializers.ModelSerializer):
    totalPrice = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ["totalPrice", "items"]
        read_only_fields = ["customer"]
        
    def get_totalPrice(self, obj):
        return obj.totalPrice