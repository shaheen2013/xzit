from django.urls import path

from activity.views import PostApiView

urlpatterns = [
    path('posts/', PostApiView.as_view()),
    path('post/<int:id>/', PostApiView.as_view()),
]
