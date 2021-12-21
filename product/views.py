from product.permissions import IsMerchant
from re import T
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductAnswerSerializer, CollectionSerializer, CategorySerializer, ProductCreateSerializer, ProductQuestionSerializer, ProductSerializer, ProductReviewsSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from.models import Category, Collection, ProductAnswer, ProductQuestion, Product, ProductReviews


# class CollectionViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get', 'post', 'update']
#     lookup_field = 'url_slug'
#     def get(self, url_slug=None):


# class CategoryViewSet(APIView):
#     def get(self, request):
#         return Response({'message': 'Category get method'})

#     def post(self, request):
#         return Response({'message': 'Category post method'})

#     def update(self, request):
#         return Response({'message': 'Category update method'})


# class ProductViewSet(APIView):

#     def get(self, request):
#         return Response({'message': 'it worked'}, status=status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=ProductSerializer)
#     def post(self, request):
#         return Response({'message': 'okay i get it'})

#     def update(self, request):
#         return Response({'message': 'Product update method'})


# class ProductQuestionsViewSet(APIView):
#     def get(self, request):
#         return Response({'message': 'Question get method'})

#     def post(self, request):
#         return Response({'message': 'Question post method'})

#     def update(self, request):
#         return Response({'message': 'Question update method'})


# class ProductAnswersViewSet(APIView):
#     def get(self, request):
#         return Response({'message': 'Answer get method'})

#     def post(self, request):
#         return Response({'message': 'Answer post method'})

#     def update(self, request):
#         return Response({'message': 'Answer update method'})


# class ProductReviewsViewSet(APIView):
#     def get(self, request):
#         return Response({'message': 'Review get method'})

#     def post(self, request):
#         return Response({'message': 'Review post method'})

#     def update(self, request):
#         return Response({'message': 'Review update method'})

class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    lookup_field = 'url_slug'


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'url_slug'


@swagger_auto_schema(request_body=ProductSerializer)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'url_slug'


class ProductQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductQuestionSerializer
    queryset = ProductQuestion.objects.all()


class ProductAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAnswerSerializer
    queryset = ProductAnswer.objects.all()


class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewsSerializer
    queryset = ProductReviews.objects.all()
# Create your views here.


# @swagger_auto_schema(methods=['post'], request_body=ProductCreateSerializer)
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated, IsMerchant])
# def postproduct(request):
#     if request.method == 'GET':
#         queryset = Category.objects.all()
#         print(queryset)
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     # TODO: prevent multiple products with the same product
#     if request.method == 'POST':
#         serializer = ProductCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(merchant=request.user.merchant)
#         return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=ProductCreateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsMerchant])
def postproduct(request):
    serializer = ProductCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(merchant=request.user.merchant)
    return Response(serializer.data)
