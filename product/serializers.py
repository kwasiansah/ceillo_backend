from django.db.models.fields.related import RelatedField
from rest_framework import serializers
from .models import ProductCatalog, ProductCategory, Product, ProductQuestion, ProductReviews, ProductAnswer

from customer.serializers import ListCustomerSerializer

class ProductCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCatalog
        # fields = '__all__'
        
        fields = ['title', 'url_slug', 'thumbnail', 'description', 'active']
        
class ProductCategorySerializer(serializers.ModelSerializer):
    catalog = ProductCatalogSerializer()
    class Meta:
        model = ProductCategory
        # fields = '__all__'
        fields = [
            'title', 'url_slug', 'thumbnail', 'description', 'active', 'catalog'
        ]
        
class ProductSerializer(serializers.ModelSerializer):
    # category = ProductCategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'url_slug', 'image', 'brand', 'price', 'description', 'long_description','in_stock', 'active', 'digital', 'merchant', 'category']
        
class ProductQuestionSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    customer = ListCustomerSerializer()
    class Meta:
        model = ProductQuestion
        fields = ['question', 'product','active', 'created', 'customer']
        
class ProductAnswerSerializer(serializers.ModelSerializer):
    question = ProductQuestionSerializer()
    class Meta:
        model = ProductAnswer
        fields = ['answer', 'question', 'voting', 'customer', 'created', 'updated', 'status']
        
class ProductReviewsSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # customer = CustomerSerializer()
    class Meta:
        model = ProductReviews
        fields = ['image', 'review', 'customer', 'product', 'active', 'created']
        
# TODO: try the depth meta attribute in serializers