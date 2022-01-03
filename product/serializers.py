from django.db.models.fields.related import RelatedField
from rest_framework import serializers


from .models import (
    Category,
    Collection,
    Product,
    ProductAnswer,
    ProductMedia,
    ProductQuestion,
    ProductReviews,
)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    # catalog = CollectionSerializer(many=True)
    class Meta:
        model = Category
        fields = "__all__"


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductMediaSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["category", "merchant"]

    def create(self, validated_data):
        category = self.initial_data["category"]
        print(validated_data)
        print(self.initial_data)
        try:
            category = Category.objects.get(id=category)
        except:
            raise serializers.ValidationError({"message": "Category Does Not Exists"})
        product = Product.objects.create(**validated_data)
        product.category.add(category)
        product.save()

        return product


class ProductQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = "__all__"


class ProductAnswerSerializer(serializers.ModelSerializer):
    question = ProductQuestionSerializer()

    class Meta:
        model = ProductAnswer
        fields = "__all__"


class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = "__all__"


# TODO: try the depth meta attribute in serializers
