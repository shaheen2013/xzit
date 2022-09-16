from django.urls import path
from common import views


urlpatterns = [
    path('reason-list/', views.ReportReasonList.as_view(), name='report-reason'),
    # path('country-list/', views.CountryList.as_view(), name='country-list'),

    # path('city-list/', views.CityList.as_view(), name='city-list'),
    # path('city-list/<str:country>/<str:name>/',views.CityCheckAPIView.as_view(),name='city-list'),
    path('countries/',views.CountryListView.as_view()),
    path('countries/<str:name>/',views.CountryDetailsView.as_view()),
    # path('cities/', CityListView.as_view()),
    path('cities/<str:country>/', views.CitySearchView.as_view()),
    path('cities/<str:country>/<str:city>/', views.CityDetailsView.as_view()),
] 