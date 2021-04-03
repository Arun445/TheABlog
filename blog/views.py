from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.http import JsonResponse

from .models import Post, Like, Comment
from.forms import PostForm, CommentForm



# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published__isnull=False).order_by('-published')
    context = {'posts': posts,}
    if request.user.is_authenticated:
        profile = User.objects.get(id=request.user.id)
        context['profile'] = profile

    return render(request, 'blog/post_list.html',context )


def users_posts(request, users_id):
    users = User.objects.get(pk=users_id)
    posts = Post.objects.filter(user=users, published__isnull=False).order_by('-published')
    context = {'posts': posts, 'users':users,}

    return render(request, 'blog/users_posts.html',context )

@login_required
def post_draft_list(request, users_id):
    user = get_object_or_404(User, pk=users_id)
    posts = Post.objects.filter(user=user, published__isnull=True).order_by('-created')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post.pk)
    context = {
        'post': post,
        'comments': comments
    }

    return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)


    else:
        form = PostForm()


    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_delete(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

#def post_likes(request, pk):
  #  post = get_object_or_404(Post, pk=pk)
   # post.likes.add(request.user)
    #return redirect('post_list')

def like_unlike_post(request):
    current_site_adress = request.META['HTTP_REFERER']
    user = request.user
    profile = User.objects.get(id=user.id)
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = User.objects.get(id=user.id)

        if profile in post.likes.all():
            post.likes.remove(profile)
        else:
            post.likes.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value='Like'
            post.save()
            like.save()

    if current_site_adress == 'http://127.0.0.1:8000/':

        return redirect('post_list')
    else:

        return redirect('post_detail', pk=post_id)


def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            if len(comment.text) > 100:
                comment.approved = False
            else:
                comment.approved = True
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form=CommentForm()
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/comment_new.html', context)

def comment_delete(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.id)

def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment_update = form.save(commit=False)
            comment_update.updated = timezone.now()
            comment_update.save()
            return redirect('post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_new.html', {'comment': comment, 'form':form})

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

