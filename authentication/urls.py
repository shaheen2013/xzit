from django.urls import path

from authentication import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('user/signup/', views.UserRegisterApiView.as_view(), name='user_signup'),
    path('user/<int:pk>/basic-info/', views.UserBasicInfoUpdateApiView.as_view(), name='user_basic_info'),
    
    path('merchant/signup/', views.MerchantRegisterApiView.as_view(), name='user_signup'),
    path('merchant/<int:pk>/basic-info/', views.MerchantBasicInfoUpdateApiView.as_view(), name='user_basic_info'),
    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
