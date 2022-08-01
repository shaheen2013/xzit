from django.urls import path, include
from rest_framework.routers import DefaultRouter
from commerce import views

router = DefaultRouter()
# router.register(r'business-register', views.BusinessTypeApiView, basename="business_type")
router.register(r'ad', views.AdApiView, basename='ad')
router.register(r'ad/banner', views.AdBannerApiView, basename='ad_banner')

urlpatterns = [
    path('business-types/', views.GetBussinessTypeApiView.as_view()),
    path('business-types/<int:id>', views.SingleBusinessTypeApiView.as_view()),
    path('ad/report/', views.AdReportApiView.as_view()),
    path('', include(router.urls)),
]
