from django.urls import path, include
from rest_framework.routers import DefaultRouter
from commerce import views

router = DefaultRouter()
router.register(r'ad', views.AdApiView, basename='ad')
# router.register(r'ad/banner', views.AdBannerApiView, basename='ad_banner')

urlpatterns = [
    path('ad/invitaions/send/', views.SendAdInviteApiView.as_view()),
    path('ad/invitations/requests/', views.AdInvitationsListApiView.as_view()),
    path('ad/invitations/sended/', views.AdSendedInvitationListApiView.as_view()),
    path('ad/invitations/<int:id>/', views.AdInvitationUpdateApiView.as_view()),
    path('business-types/', views.GetBussinessTypeApiView.as_view()),
    path('business-types/<int:id>', views.SingleBusinessTypeApiView.as_view()),
    path('ad/report/', views.AdReportApiView.as_view()),
    path('reservations/request/', views.ReservationCreateApiView.as_view()),
    path('user/reservations/list/', views.UserReservationListApiView.as_view()),
    path('merchant/reservations/list', views.MerchantReservationListApiView.as_view()),
    path('reservations/<int:id>/', views.ReservationDetailApiView.as_view()),
    path('user/reservations/<int:id>/update/', views.ReservationUserUpdateApiView.as_view()),
    path('merchant/reservations/<int:id>/update/', views.ReservationMerchantUpdateApiView.as_view()),
    path('merchant/reservations/<int:id>/set_alt/', views.ReservationMerchantSetAlternative.as_view()),
    path('merchant/alt-reservations/<int:id>/approve/', views.AlternativeReservationMerchantStatus.as_view()),
    path('user/alt-reservations/<int:id>/approve/', views.AlternativeReservationUserStatus.as_view()),
    path('merchant/alt-reservations/list/', views.MerchantAltReservationListApiView.as_view()),
    path('user/alt-reservations/list/', views.UserAltReservationListApiView.as_view()),

    path('ad/images/', views.AdBannerImageCreateApiView.as_view()),
    path('', include(router.urls)),
    path('ad/comment/create/', views.AdCommentCreate.as_view()),
    path('ad/like/create/', views.AdLikeCreate.as_view()),
    path('ad/save/create/', views.AdSaveCreate.as_view()),
]
