from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/update', views.post_update, name='post_update'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'),
    path('user/<int:users_id>', views.users_posts, name='users_posts'),
    path('post/draft_list/<int:users_id>', views.post_draft_list, name='post_draft_list'),
    path('post/liked', views.like_unlike_post, name='post_likes'),
    path('comment/<int:pk>/new', views.comment_new, name='comment_new'),
    path('comment/<int:pk>/delete', views.comment_delete, name='comment_delete'),
    path('comment/<int:pk>/update', views.comment_update, name='comment_update'),
    path('comment/<int:pk>/approve', views.comment_approve, name='comment_approve'),



]