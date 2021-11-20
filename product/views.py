from django.shortcuts import render
from.models import ProductCategory, ProductCatalog, ProductAnswer, ProductQuestion, Product, ProductReviews
from .serializers import ProductAnswerSerializer,ProductCatalogSerializer,ProductCategorySerializer, ProductQuestionSerializer, ProductSerializer,ProductReviewsSerializer
from rest_framework import viewsets

class ProductCatalogViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCatalogSerializer
    queryset = ProductCatalog.objects.all()
    

class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductQuestionSerializer
    queryset = ProductQuestion.objects.all()

class ProductAnswerViewSet(viewsets.ModelViewSet):
    serializer_class =ProductAnswerSerializer
    queryset = ProductAnswer.objects.all()
    
class ProductReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewsSerializer
    queryset = ProductReviews.objects.all()
# Create your views here.
