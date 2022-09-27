from django.urls import path
from common import views


urlpatterns = [
    path('reason-list/', views.ReportReasonList.as_view(), name='report-reason'),
    
    path('friend-list-func/', views.FriendListFunc, name='friend-list-func'),
    path('friend-block/', views.BlockList, name='friend-block'),
]