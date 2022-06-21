from django.urls import path

from activity.views import PostInterectionCreateAPIView, PostListApiView, PostUpdateDeleteApiView

urlpatterns = [
    path('posts/', PostListApiView.as_view()),
    path('posts/<int:id>/', PostUpdateDeleteApiView.as_view()),
    path('posts/interection/', PostInterectionCreateAPIView.as_view())
]
