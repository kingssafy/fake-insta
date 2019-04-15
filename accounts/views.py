from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

def signup(request):
    if request.user.is_authenticated: return redirect('posts:list')
    if request.method == "POST":
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user = user.save()
            auth_login(request, user)
            return redirect('posts:list')
    context = {
        'form': UserCreationForm()
    }
    return render(request, 'accounts/create.html', context)
    

def login(request):
    if request.user.is_authenticated: return redirct('posts:list')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get("next") or 'posts:list')
    else:
        next = request.GET.get('next', '')
        form = AuthenticationForm()
        context = {
            'next': next,
            'form': form,
        }
        return render(request, 'accounts/login.html', context)
        
def logout(request):
    auth_logout(request)
    return redirect('posts:list')