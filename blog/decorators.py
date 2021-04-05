from django.http import HttpResponse
from django.shortcuts import redirect

from django.contrib.auth.models import User

from .models import Post, Comment

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post_list')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def user_authentication(view_func):
    def wrapper_func(request,pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        if request.user != user:
            return HttpResponse('you cant do that')
        else:
            return view_func(request,pk, *args, **kwargs)
    return wrapper_func

def post_authentication(view_func):
    def wrapper_func(request,pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        user = post.user
        if request.user != user:
            return HttpResponse('you cant do that')
        else:
            return view_func(request,pk, *args, **kwargs)
    return wrapper_func

def comment_authentication(view_func):
    def wrapper_func(request,pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        post_id = comment.post.id
        post = Post.objects.get(pk=post_id)
        post_user = post.user
        user = comment.author
        if request.user != user and request.user != post_user:
            return HttpResponse('you cant do that')
        else:
            return view_func(request,pk, *args, **kwargs)
    return wrapper_func