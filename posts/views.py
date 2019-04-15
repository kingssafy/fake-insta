from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, Comment
from .form import PostForm, ImageForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Create your views here.

def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    comment_form = CommentForm()
    context = dict(posts=posts, 
    comment_form=comment_form)
    return render(request, 'posts/list.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
    context = dict(post_form = post_form, image_form = ImageForm())
    return render(request, 'posts/form.html', context)
    
def update(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if request.method == 'POST' and post.user == request.user:
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
    context = dict(post_form = post_form)
    return render(request, 'posts/form.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
    return redirect('posts:list')
    
@login_required    
@require_POST
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.post_id = post_pk
        form.save()
        return redirect('posts:list')

@login_required
@require_POST
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, id=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:list')