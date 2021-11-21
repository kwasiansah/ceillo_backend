from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('account-update/', user_update, name='user_update'),
    path('account-details/', user_detail, name='user_detail'),
    path('delete-account/', user_delete, name='user_delete'),
    path('sign-up/', user_create, name='user_create'),
    path('list/', user_list, name='user_list'),
    path('password-change/', password_change, name='password-change'),
    path('password-reset/', user_password_reset, name='password-reset'),
    path('password-reset-confirm/<str:token>/',
         user_password_reset_confirm, name='password-reset-confirm'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]