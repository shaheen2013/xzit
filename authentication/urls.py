from django.urls import path

from authentication.views import RegistrationView

urlpatterns = [
    path('signup/', RegistrationView.as_view())
]
