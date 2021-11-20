from rest_framework.routers import DefaultRouter
from .views import ProductCatalogViewSet, ProductCategoryViewSet,ProductViewSet, ProductQuestionViewSet, ProductAnswerViewSet,ProductReviewsViewSet

router = DefaultRouter()
router.register(r'productcatalog', ProductCatalogViewSet, basename='productcatalog')
router.register(r'productcategory', ProductCategoryViewSet, basename='productcategory')
router.register(r'productquestions',ProductQuestionViewSet, basename='productquestion')
router.register(r'productanswer', ProductAnswerViewSet, basename='productanswer')
router.register(r'productreview',ProductReviewsViewSet, basename='productreview')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = router.urls