from django.urls import path

from activity import views

urlpatterns = [
    path('posts/', views.PostListApiView.as_view()),
    path('posts/<int:id>/', views.PostUpdateDeleteApiView.as_view()),
    path('posts/interection/', views.PostInterectionCreateAPIView.as_view()),
    path('posts/comment/', views.PostCommentAPIView.as_view()),
    path('posts/<int:post_id>/comments/', views.PostCommentsAPIView.as_view()),
    path('stories/', views.StoryCreateAPIView.as_view()),
    path('stories/<int:id>/', views.StoryRetrieveUpdateDeleteAPIView.as_view())
]
