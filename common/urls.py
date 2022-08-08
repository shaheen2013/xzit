from django.urls import path
from common import views


urlpatterns = [
    path('reason-list/', views.ReportReasonList.as_view(), name='report-reason')
]