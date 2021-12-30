from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CollectionViewSet,
    ProductAnswerViewSet,
    ProductQuestionViewSet,
    ProductReviewViewSet,
    ProductViewSet,
    postproduct,
)

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"collection", CollectionViewSet, basename="collection")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"productquestions", ProductQuestionViewSet, basename="productquestion")
router.register(r"productanswer", ProductAnswerViewSet, basename="productanswer")
router.register(r"productreview", ProductReviewViewSet, basename="productreview")

urlpatterns = [path("post-product/", postproduct, name="post-product")]
urlpatterns += router.urls
