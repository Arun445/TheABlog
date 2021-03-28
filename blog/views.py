from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post
from.forms import PostForm



# Create your views here.

def post_list(request):
    posts = Post.objects.filter(date__lte=timezone.now()).order_by('-date')
    return render(request, 'blog/post_list.html',{'posts': posts} )

@login_required
def post_draft_list(request, users_id):
    user = get_object_or_404(User, pk=users_id)
    posts = Post.objects.filter(user=user, published__isnull=True).order_by('-date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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