from rest_framework.routers import DefaultRouter
# from .views import CustomerList, CustomerCreate, CustomerRetrieve, user_list
from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views
# router = DefaultRouter()
# # router.register(r'user', UserViewSet, basename="user")
# router.register(r'customer', CustomerViewSet, basename='customer')
# router.register(r'merchant', MerchantViewSet, basename='merchant')

# urlpatterns = router.urls
# urlpatterns = [
#     path('retrive/<str:customer_id>/', CustomerRetrieve.as_view()),
#     path('test/', user_list),
#     path('create/', CustomerCreate.as_view()),
#     # path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

#     path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('', CustomerList.as_view()),
# ]

urlpatterns = [
    path('account-update/', user_update, name='user_update'),
    path('account-detail/', user_detail, name='user_detail'),
    path('delete-account/', user_delete, name='user_delete'),
    path('sign-up/', user_create, name='user_create'),
    path('list/', user_list, name='user_list'),
    path('password-change/', password_change, name='passwordchange'),
    path('password-rest/', user_password_reset, name='password-rest'),
    path('password-rest-confirm/',
         user_password_reset_confirm, name='passwordresetconfirm'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),

    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

]


api_urls = {
    'list': '/tast-list/',
    'Detailview': '/task-detail/<str:pk>/',
    'Create': '/task-create/',
    'update': '/task-update/',
    'Delete': '/task-delete/',
}
password = {
    'passwordChangeview',
    'passwordChangeDone',
    'passwordResetview',
    'passwordResetdoneView',
    'passwordResetconfirmview',
    'passwordResetCompleteView',


}
