from django.urls import path
from common import views


urlpatterns = [
    path('reason-list/', views.ReportReasonList.as_view(), name='report-reason'),
    path('country-list/', views.CountryList.as_view(), name='country-list'),
    path('^country-list/(?P<name>.+)/$',views.CountryListSearch.as_view(),name='country-list'),
    path('city-list/', views.CityList.as_view(), name='city-list')
]