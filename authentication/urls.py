from django.urls import path, include
from authentication import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('user/signup/', views.UserRegisterApiView.as_view(), name='user_signup'),
    path('user/profile/<int:id>/', views.UserProfileApiView.as_view(), name='user_profile'),
    path('merchant/profile/<int:id>/', views.MerchantProfileApiView.as_view(), name='merchant_profile'),
    path('user/<int:id>/basic-info/', views.UserBasicInfoUpdateApiView.as_view(), name='user_basic_info'),
    path('business-type/<int:id>/save/', views.BusinessTypeSaveApiView.as_view()),
    path('business-sub-type/<int:id>/save/', views.BusinessSubTypeSaveApiView.as_view()),
    path('merchant/signup/', views.MerchantRegisterApiView.as_view(), name='user_signup'),
    path('merchant/<int:id>/basic-info/', views.MerchantBasicInfoUpdateApiView.as_view(), name='user_basic_info'),
    path('account-verify/', views.AccountVerifyApiView.as_view()),
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    path('password-reset/', views.PasswordResetAPIView.as_view(), name='password_reset'),
    path('password-reset-verify/', views.PasswordResetOtpVerfy.as_view(), name='password_reset_verify'),
    path('password-reset-confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_verify'),
    # path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('login/', views.Login.as_view(), name='login'),
    path('otp-verify/', views.OtpVerifyApiView.as_view(), name='resend_verify'),
    path('otp-resend/', views.OtpResendpApiView.as_view(), name='resend_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/report', views.UserReportApiView.as_view()),
    path('permissions/', views.PermissionAPIView.as_view(), name="permissions"),
    path('roles/', views.RolesCreateListApiView.as_view()),
    path('roles/<int:id>/', views.RolesRetriveUpdateDestroyAPIView.as_view()),
    path('user/check-username/<str:username>/', views.UsernameCheckAPIView.as_view(), name="check_username"),
    path('user/check-phone/', views.PhoneNumberCheck.as_view(), name="check_phone"),
]
