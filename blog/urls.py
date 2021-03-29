from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/update', views.post_update, name='post_update'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/draft_list/<int:users_id>', views.post_draft_list, name='post_draft_list'),
   # path('post/<int:pk>/like', views.post_likes, name='post_likes'),
    path('post/liked', views.like_unlike_post, name='post_likes'),

]