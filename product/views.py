from re import T

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.permissions import IsMerchant

from .models import (
    Category,
    Collection,
    Product,
    ProductAnswer,
    ProductMedia,
    ProductQuestion,
    ProductReviews,
)
from .serializers import (
    CategorySerializer,
    CollectionSerializer,
    ProductAnswerSerializer,
    ProductQuestionSerializer,
    ProductReviewsSerializer,
    ProductSerializer,
)


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    lookup_field = "url_slug"


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "url_slug"


@swagger_auto_schema(request_body=ProductSerializer)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "url_slug"


class ProductQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductQuestionSerializer
    queryset = ProductQuestion.objects.all()


class ProductAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAnswerSerializer
    queryset = ProductAnswer.objects.all()


class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewsSerializer
    queryset = ProductReviews.objects.all()


@swagger_auto_schema(method="post", request_body=ProductSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsMerchant])
def postproduct(request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(merchant=request.user.merchant)
    for media in request.FILES.getlist("images"):
        ProductMedia.objects.create(product=serializer.instance, raw_image=media)
    product = ProductSerializer(serializer.instance)

    return Response(product.data)
