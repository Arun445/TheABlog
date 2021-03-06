from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from .decorators import unauthenticated_user, user_authentication, post_authentication, comment_authentication


# Create your views here.

#Shows published posts from all users with pagination
def post_list(request):
    posts = Post.objects.filter(published__isnull=False).order_by('-published')

    #Pagination functions
    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #Add comment to post form
    p_form = CommentForm(request.POST or None)

    context = {'posts': posts,'p_form': p_form, 'page_obj':page_obj}

    #Dosent let not registered users like
    if request.user.is_authenticated:
        profile = User.objects.get(id=request.user.id)
        context['profile'] = profile

    #Comment form lets you comment on a specific post in the post list page
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.post = Post.objects.get(pk=request.POST.get('post_id'))
            if len(instance.text) > 100:
                instance.approved = False
            else:
                instance.approved = True
            instance.save()
            return redirect('post_list')

    return render(request, 'blog/post_list.html',context )

#Specific users profile (public). Shows how many posts this user has and filters them by the amount of likes on the post.
def users_posts(request, users_id):
    users = User.objects.get(pk=users_id)
    posts = Post.objects.filter(user=users, published__isnull=False).order_by('-likes')
    user_post_count = posts.count()
    #pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'posts': posts, 'users': users, 'user_post_count': user_post_count, 'page_obj':page_obj}

    return render(request, 'blog/users_posts.html',context )

#Not published posts, only accessisble to the user.
@login_required
@user_authentication
def post_draft_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(user=user, published__isnull=True).order_by('-created')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

#Shows a specific post and its comments.
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post.pk)
    context = {
        'post': post,
        'comments': comments
    }

    return render(request, 'blog/post_detail.html', context)

#If you are logged in you can create a new post.
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

#Lets you update your specific post.
@login_required
@post_authentication
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

#Deletes users posts.
@login_required
@post_authentication
def post_delete(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

#Publishes a users post to the public
@login_required
@post_authentication
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.publish()
    return redirect('post_detail', pk=pk)

#def post_likes(request, pk):
  #  post = get_object_or_404(Post, pk=pk)
   # post.likes.add(request.user)
    #return redirect('post_list')

#Like on posts functionality.
@login_required
def like_unlike_post(request):
    current_site_address = request.META['HTTP_REFERER']
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
    #Checks on which url user is on
    if current_site_address == 'http://127.0.0.1:8000/':

        return redirect('post_list')
    else:

        return redirect('post_detail', pk=post_id)

#Creates a comment on a post
@login_required
def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            #if the comment is long enough, it needs to be approved by the superuser or the posts author
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

#comment delete, allowed by the user who wrote a comment, a superuser or the posts author
@login_required
@comment_authentication
def comment_delete(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.id)

#comment update function
@login_required
@comment_authentication
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
    comment = Comment.objects.get(pk=pk)
    post_id = comment.post.id
    post = Post.objects.get(pk=post_id)
    post_user = post.user
    #Checks if the user who wants to approve a comment is the posts author
    if post_user == request.user:
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
    else:
        return HttpResponse('sorry')
    return redirect('post_detail', pk=comment.post.pk)

