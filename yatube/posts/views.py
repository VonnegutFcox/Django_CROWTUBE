from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post, Group


def index(request):
    # latest = Post.objects.order_by("-pub_date")[:11]
    latest = Post.objects.all()[:11]
    return render(request, "index.html", {"posts": latest})


# view-функция для страницы сообщества
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    # posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    form = PostForm(request.POST) or None
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:index")
    return render(request, "posts/new.html", {"form": form})
