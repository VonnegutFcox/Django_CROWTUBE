from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, Group, Follow

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html",
                  {"page": page, "group": group})


@login_required
def new_post(request):
    form = PostForm(request.POST) or None
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:index")
    return render(request, "posts/new.html",
                  {"form": form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = (
        request.user.is_authenticated and request.user.
        follower.filter(author=author).exists())
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {"author": author, "page": page,
                   "following": following})


def post_view(request, username, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post,
                             author__username=username,
                             id=post_id)
    comments = post.comments.all()
    author = post.author
    context = {
        'post': post,
        'author': author,
        'form': form,
        'comments': comments,
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect("posts:post",
                        username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("posts:post",
                        username=request.user.username,
                        post_id=post_id)

    return render(
        request, 'new.html', {'form': form, 'post': post},
    )


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post,
                             author__username=username,
                             id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post',
                        username=username,
                        post_id=post_id)
    return redirect('posts:post',
                    username=username,
                    post_id=post_id)


@login_required
def follow_index(request):
    following_posts = Post.objects.filter(
        author__following__user=request.user)
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user,
                          author=author).delete()
    return redirect('posts:profile', username=username)


def obtain_auth_token():
    return None