from django.db.models.fields.related import RelatedField
from rest_framework import serializers
from .models import (
    ProductMedia,
    Collection,
    Category,
    Product,
    ProductQuestion,
    ProductReviews,
    ProductAnswer,
)

from customer.serializers import ListCustomerSerializer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        # fields = '__all__'

        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    # catalog = CollectionSerializer(many=True)

    class Meta:
        model = Category
        # fields = '__all__'
        fields = "__all__"


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=False)

    class Meta:
        model = Product

        fields = "__all__"
        read_only_fields = ["category", "merchant"]

    # work on the media option

    def create(self, validated_data):
        category = self.initial_data["category"]
        try:
            category = Category.objects.get(name=category)
        except:
            raise serializers.ValidationError({"message": "Category does not exists"})
        product = Product.objects.create(**validated_data)
        product.category.add(category)
        product.save()
        if not validated_data.pop("media", False):
            media = ProductMedia(product=product)
            media.save()

        return product


class ProductDetailSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductQuestionSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    customer = ListCustomerSerializer()

    class Meta:
        model = ProductQuestion
        fields = "__all__"


class ProductAnswerSerializer(serializers.ModelSerializer):
    question = ProductQuestionSerializer()

    class Meta:
        model = ProductAnswer
        fields = "__all__"


class ProductReviewsSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # customer = CustomerSerializer()
    class Meta:
        model = ProductReviews
        fields = "__all__"


# TODO: try the depth meta attribute in serializers
