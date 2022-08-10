from django.urls import path

from activity import views

urlpatterns = [
    path('posts/', views.PostCreateApiView.as_view()),
    path('posts/feeds/', views.PostFeedListApiView.as_view()),
    path('posts/<int:id>/', views.PostUpdateApiView.as_view()),
    path('posts/<int:id>/delete/', views.PostDeleteApiView.as_view()),
    path('posts/<int:id>/show/', views.PostDetailsApiView.as_view()),
    path('posts/interection/', views.PostInterectionCreateAPIView.as_view()),
    path('posts/comment/', views.PostCommentAPIView.as_view()),
    path('posts/<int:post_id>/comments/', views.PostCommentsAPIView.as_view()),
    path('posts/report', views.PostReportApiView.as_view()),
    path('stories/', views.StoryListCreateAPIView.as_view()),
    path('stories/<int:id>/', views.StoryRetrieveUpdateDeleteAPIView.as_view()),
    path('stories/report', views.StoryReportApiView.as_view()),


    path('posts/images/', views.PostImageAPIView.as_view()),
]
