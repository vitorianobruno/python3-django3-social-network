import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from itertools import chain
import logging
logger = logging.getLogger(__name__)

from .models import *

def index(request):
    
    logger.error("Entering 'INDEX' function..")
    
    results = Post.objects.all().order_by("-datetime")
    paginator = Paginator(results, 10)
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts
    })


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

#######################################################################

@login_required
def post(request):
    """
    Function that allows create a NEW post.
    """
    logger.error("Entering 'POST' function..")
    
    try:
        if request.method == "POST":
         
            message = request.POST.get("message")          
            user_id = request.user.id
            obj_user = User.objects.get(id=user_id)
            
            post = Post(user=obj_user, message=message, total_like=0)
            post.save()
            
            posts = Post.objects.all().order_by("-datetime")

            return render(request, 'network/index.html', {
                'posts': posts
            })
    except KeyError:
        return index(request)


@csrf_exempt
@login_required
def edit(request, post_id):
    """
    Return the message from a specific post in JSON object. 
    """
    logger.error("Entering 'EDIT' function..")
    
    # Query for requested post
    obj_post =  Post.objects.get(pk=post_id)
    
    if request.method == "GET":
        return JsonResponse({
            "message": f"{obj_post.message}"
        }, status=200)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


@csrf_exempt
@login_required
def save(request, post_id):
    """
    Save an edited post 
    """
    logger.error("Entering 'SAVE' function..")
    
    obj_post = Post.objects.get(pk=post_id)
    
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("message") is not None:
            obj_post.message = data["message"]
            
        obj_post.save()
        
        #new_post = Post.objects.get(pk=post_id)
        return JsonResponse({
            "message": f"{obj_post.message}"
        }, status=200)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)


@login_required
def profile(request):
    """
    Return a list of all user posts + following / followers number.
    """ 
    logger.error("Entering 'PROFILE' function..")
    
    user_id = request.user.id
    obj_user = User.objects.get(id=user_id)
    
    following = Following.objects.filter(user=user_id).count()
    followers = Following.objects.filter(following_id=user_id).count()
    
    posts = Post.objects.filter(user=user_id).order_by("-datetime")
    
    users = User.objects.all()

    for user in users:
        if user.id != user_id:
            follow = Following.objects.filter(user=obj_user, following_id=user.id)
            if follow:
                user.is_active = True 
            else:
                user.is_active = False
    

    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'network/profile.html', {
        'following': following,
        'followers': followers,
        'posts': posts,
        'users': users
    })


@csrf_exempt
@login_required
def profile_refresh(request):
    """
    Refresh 'Following/Followers' count and user followed state.
    """
    logger.error("Entering 'REFRESH_PROFILE' function..")
    
    user_id = request.user.id
    obj_user = User.objects.get(id=user_id)
    
    if request.method == "GET":
    
        following = Following.objects.filter(user=user_id).count()
        followers = Following.objects.filter(following_id=user_id).count()
    
        users = User.objects.all()

        for user in users:
            #if user.id != user_id:
                follow = Following.objects.filter(user=obj_user, following_id=user.id)
                if follow:
                    user.is_active = True
                else:
                    user.is_active = False

        serialized_users = serializers.serialize("json", users,  fields=('username', 'is_active'))

        return JsonResponse({
                "following": following,
                "followers": followers,
                "users": serialized_users,
                "request_user_id": request.user.id
        }, status=200)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


@csrf_exempt
@login_required 
def profile_following(request, following_id):
    """
    ADD or REMOVE a 'Following' to the user.
    """
    if request.method == "PUT":
        logger.error("Entering 'FOLLOWING' method..")
        
        user = request.user.id
        obj_user = User.objects.get(id=user)
        
        follow = Following.objects.filter(user=obj_user, following_id=following_id)

        if not follow:
            logger.error("ADD Following")
            
            # Add followed user
            obj = Following()
            obj.user = obj_user
            obj.following_id = following_id
            obj.save()
            return HttpResponse(status=204)
        else:
            logger.error("REMOVE Following")
            # Remove followed user
            follow.delete()
            return HttpResponse(status=204)
    
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@login_required
def following(request):
    
    logger.error("Entering 'Following' function..")
    
    user = request.user.id
    obj_user = User.objects.get(id=user)
    following = Following.objects.filter(user=obj_user)
    
    posts = Post.objects.none()
    for follow in following:
        #user = User.objects.get(id=follow.following_id)
        a = Post.objects.filter(user=follow.following_id)
        posts = list(chain(posts, a))
    
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "posts": posts
    })


@csrf_exempt
@login_required 
def like(request, post_id):
    """
    ADD or REMOVE a 'like' to the current post.
    """
    if request.method == "PUT":
        logger.error("Entering 'LIKE' method..")
        
        user = request.user.id
        obj_user = User.objects.get(id=user)
        obj_post = Post.objects.get(pk=post_id)
        
        #if obj_post.user.id != user:
        
        like = Likes.objects.filter(post_id=post_id, user_id=obj_user)

        if not like:
            logger.error("ADD Like")
            
            # Add 1 more "Like" to total
            obj_post.total_like += 1
            obj_post.save()
            
            # Add the relation Post/User/Like to Likes table
            obj_like = Likes()
            obj_like.post_id = obj_post
            obj_like.user_id = obj_user
            obj_like.liked = True
            obj_like.save()
            return HttpResponse(status=204)
        else:
            logger.error("REMOVE Like")
            
            # Remove 1 "Like" from total.
            obj_post.total_like = obj_post.total_like - 1
            obj_post.save()
            
            # Remove "Like" from the Likes table
            like.delete()
            return HttpResponse(status=204)
    
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def like_refresh(request, post_id):
    """
    Refresh 'Likes' in a specific post. 
    """
    logger.error("Entering 'REFRESH' function..")
    
    # Query for requested post
    obj_post =  Post.objects.get(pk=post_id)
    
    if request.method == "GET":
        try:
            like = Likes.objects.get(post_id=post_id, user_id=request.user)
        except Likes.DoesNotExist:
            return JsonResponse({
                    "like": "False",
                    "total": f"{obj_post.total_like}"
                }, status=200)

        return JsonResponse({
            "like": "True",
            "total": f"{obj_post.total_like}"
        }, status=200)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
