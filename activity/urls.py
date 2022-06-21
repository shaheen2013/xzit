from django.urls import path

from activity.views import PostInterectionCreateAPIView, PostListApiView, PostUpdateDeleteApiView, StoryCreateListAPIView, StoryRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('posts/', PostListApiView.as_view()),
    path('posts/<int:id>/', PostUpdateDeleteApiView.as_view()),
    path('posts/interection/', PostInterectionCreateAPIView.as_view()),
    path('stories/', StoryCreateListAPIView.as_view()),
    path('stories/<int:id>/', StoryRetrieveUpdateDeleteAPIView.as_view())
]
