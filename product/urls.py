from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CollectionViewSet, ProductAnswerViewSet,
                    ProductQuestionViewSet, ProductReviewViewSet,
                    ProductViewSet, postproduct)

router = DefaultRouter()
router.register(r"Collection", CollectionViewSet, basename="Collection")
router.register(r"Category", CategoryViewSet, basename="Category")
router.register(r"productquestions", ProductQuestionViewSet, basename="productquestion")
router.register(r"productanswer", ProductAnswerViewSet, basename="productanswer")
router.register(r"productreview", ProductReviewViewSet, basename="productreview")
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = [path("post-product/", postproduct, name="post-product")]
urlpatterns += router.urls

# urlpatterns = [
#     path('product/', ProductViewSet.as_view(), name='product'),
#     path('product-catalog/<str:url_slug>/',
#          CollectionViewSet.as_view(), name='product-catalog'),
#     path('product-category/', CategoryViewSet.as_view(),
#          name='product-category'),
#     path('product-questions/', ProductQuestionsViewSet.as_view(),
#          name='product-questions'),
#     path('product-answers/', ProductAnswersViewSet.as_view(), name='product-answers'),
#     path('product-reviews/', ProductReviewsViewSet.as_view(), name='product-reviews'),
# ]
