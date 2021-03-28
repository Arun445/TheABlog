from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User

from .forms import SignUpForm
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form':form})

def profile(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'user/profile.html', {'user': user})











