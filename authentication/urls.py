from django.urls import path, include

from authentication import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('user/signup/', views.UserRegisterApiView.as_view(), name='user_signup'),
    path('user/<int:id>/basic-info/', views.UserBasicInfoUpdateApiView.as_view(), name='user_basic_info'),
    
    path('merchant/signup/', views.MerchantRegisterApiView.as_view(), name='user_signup'),
    path('merchant/<int:id>/basic-info/', views.MerchantBasicInfoUpdateApiView.as_view(), name='user_basic_info'),
    
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
     
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
