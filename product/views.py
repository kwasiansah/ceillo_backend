from re import T

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customer.models import Customer
from rest_framework.pagination import PageNumberPagination
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


class ProductResultsPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return None
        return page_number


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
    pagination_class = ProductResultsPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if isinstance(self.request.user, Customer):
            user = self.request.user
            try:
                merchant = user.merchant
            except Customer.merchant.RelatedObjectDoesNotExist:
                merchant = None
            queryset = queryset.filter(merchant=merchant)
            print("merchant specific products retrived")
            return queryset
        print("general products retrieved")
        return queryset

    def update(self, request, *args, **kwargs):
        print(request.data)
        print()
        print(request.FILES)
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print("product created")
        if request.FILES.getlist("images"):
            ProductMedia.objects.filter(product=instance).delete()
            for media in request.FILES.getlist("images"):
                ProductMedia.objects.create(
                    product=serializer.instance, image_url=media
                )
            print("images updated")

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        data = {"message": "Product Successfully Updated"}
        return Response(data, status.http_200_ok)


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
    print(request.data)
    print()
    print(request.FILES)
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(merchant=request.user.merchant)
    for media in request.FILES.getlist("images"):
        ProductMedia.objects.create(product=serializer.instance, image_url=media)
    product = ProductSerializer(serializer.instance)
    print(product.data)
    data = {"message": "Product Successfully Posted"}
    return Response(data, status.HTTP_200_OK)
