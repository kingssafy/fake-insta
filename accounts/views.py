from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from .form import CustomUserChangeForm
from .form import CustomUserCreationForm as UserCreationForm
from django.contrib.auth.decorators import login_required

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
    
    
def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = dict(people=people)
    return render(request, 'accounts/people.html', context);
@login_required 
def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('people', request.user.username)
    form = CustomUserChangeForm(instance=request.user)
    context = dict(form=form)
    return render(request, 'accounts/create.html', context)
    
@login_required
def delete(request):
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        user.delete()
    return redirect('posts:list')
    
    
@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', request.user.username)
    context = dict(password_change_form = PasswordChangeForm(request.user))
    return render(request, 'accounts/password_form.html', context)