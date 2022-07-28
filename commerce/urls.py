from django.urls import path, include
from rest_framework.routers import DefaultRouter
from commerce import views

router = DefaultRouter()
router.register(r'ad', views.AdApiView, basename='ad')
router.register(r'ad/banner', views.AdBannerApiView, basename='ad_banner')

urlpatterns = [
    path('ad/report/', views.AdReportApiView.as_view()),
    path('', include(router.urls)),
]
