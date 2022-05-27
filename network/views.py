import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, User
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib import messages


def index(request):
    # Return posts in reverse chronological order
    posts = Post.objects.order_by("-created_date").all()
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'posts': posts,
        'page_obj': page_obj
    })


@login_required
def following_posts(request):
    follower_list = request.user.following.all()
    posts = Post.objects.filter(user__in=follower_list).order_by("-created_date")

    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'posts': posts,
        'page_obj': page_obj
    })


@login_required
def write_post(request):
    post_form = PostForm()
    return render(request, 'network/write_post.html', {
        "post_form": post_form
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit= False)
            post.user = request.user 
            post.save()
            messages.success (request,'Posted!')
            return HttpResponseRedirect(reverse('index'))
        
    messages.warning(request, "Something's wrong...")

    return render(request, 'network/write_post.html')


@csrf_exempt
@login_required
def posts(request, post_id):
    # Query for requested post
    post = Post.objects.get(pk=post_id)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Retrive post data
    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("content") is not None:
            post.content = data["content"]
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)


def profile(request, user_id, username):
    user_profile = User.objects.get(id=user_id)

    posts = Post.objects.filter(user=user_id).order_by("-created_date")

    return render(request, "network/profile.html", {
        'user_posts': posts,
        'user_profile': user_profile 
    })


def follow(request, user_to_follow_id, toFollow = 1): # 1 = True, 0 = False
    if request.method == 'POST':
        user_to_follow = User.objects.get(id=user_to_follow_id)
        if toFollow:
            request.user.following.add(user_to_follow)
        else:
            request.user.following.remove(user_to_follow)

    username = user_to_follow.username
    return redirect('profile', user_id=user_to_follow_id, username=username)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
