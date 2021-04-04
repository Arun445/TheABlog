from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User

from blog.models import Post
from user.models import UserProfile
from .forms import UserRegisterForm, EmailChangeForm, ProfileChangeForm
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')

    else:
        form = UserRegisterForm()
    return render(request, 'user/signup.html', {'form':form})

def profile(request, pk):
    users = User.objects.get(pk=pk)
    print(users.email)
    post = Post.objects.filter(user=pk)
    if request.method == "POST":
        e_form = EmailChangeForm(request.POST, instance=users)
        p_form = ProfileChangeForm(request.POST, request.FILES, instance=users.userprofile)
        if e_form.is_valid() and p_form.is_valid():
            e_form.save()
            p_form.save()
            return redirect('profile', pk=pk)
    else:
        e_form = EmailChangeForm(instance=users)
        p_form = ProfileChangeForm(instance=users.userprofile)

    context = {
        'users': users,
        'post': post,
        'e_form': e_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile.html', context)











