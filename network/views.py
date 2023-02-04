from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from django.core.paginator import Paginator

from .models import User,Profile,Post
from django.contrib import messages
import pdb

from django.shortcuts import render
import json



class PostForm(forms.Form):
    content=forms.CharField(
        #required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Post content",
                "id": "new_content",
                "rows":5,
                "cols":25
            }
        ),
        error_messages = {
            'required':"Please type in your message!"
        }
    )

def index(request):
    form=PostForm()
    posts = Post.objects.filter(poster=request.user.id).order_by('-timestamp')
    paginator = Paginator(posts, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
                "form": form,
                'page_obj': page_obj
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
            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def addpost(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            poster=request.user
            
            newentry=Post(content=content,poster=poster)
            newentry.save()
            return HttpResponseRedirect(reverse("index"))
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "network/index.html", context)

    return HttpResponseRedirect(reverse("index"))

def allposts(request):
    
    try:
        #category_id=args
        posts = Post.objects.all().order_by('-timestamp')
        customposts=[]
        for p in posts:
            liketext=''
            if p.likes.filter(pk=request.user.id).exists()==True:
                liketext="Unlike"
            else:
                liketext="Like"
            record={"post":p,"liketext":liketext}
            customposts.append(record)
        paginator = Paginator(customposts, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except posts.DoesNotExist:
        raise Http404("Posts not found.")
    return render(request, "network/allposts.html", {'page_obj': page_obj})

def viewprofile(request,username):
    try:
       
        poster=User.objects.get(username=username)
        profile=Profile.objects.filter(user=poster).first()
        actiontext=None
        if(request.user.id!=profile.user.id):
            if(profile.followers.filter(pk=request.user.id).exists()):
                actiontext="Unfollow"
            else:
                actiontext="Follow"
        userprofile={}
        userprofile["userid"]=profile.user.id
        userprofile["name"]=profile.user.first_name+" "+profile.user.last_name+" "+profile.user.email
        userprofile["followers_count"]=profile.followers.count()
        userprofile["followees_count"]=profile.followees.count()
        userprofile["actiontext"]=actiontext
    except Profile.DoesNotExist or profile.DoesNotExist:
        raise Http404("Profile not found.")
    return render(request, "network/profile.html", {'profile': userprofile})

def editpost(request,postid):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        posttoedit=Post.objects.filter(pk=postid).first()
        if form.is_valid() and posttoedit!=None:
            content = form.cleaned_data["content"]
            posttoedit.content=content
            posttoedit.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            raise Http404("Post not found.")
    
    #return HttpResponseRedirect(reverse("index"))

def followaction(request,userid):
    try:
        usera=User.objects.get(pk=userid)
        profile=Profile.objects.filter(user=usera).first()
        currentuserprofile=Profile.objects.filter(user=request.user).first()
        if(profile.followers.filter(pk=request.user.id).exists()):
            profile.followers.remove(request.user)
            currentuserprofile.followees.remove(usera)
        else:
            profile.followers.add(request.user)
            currentuserprofile.followees.add(usera)
        profile.save()
        return HttpResponseRedirect(reverse("profile", args=(usera.username,)))
    except:
        raise HttpResponse(status=500)


def followingposts(request):
    currentprofile=Profile.objects.filter(user=request.user).first()
    influencers=currentprofile.followees.values_list(flat=True)
    posts = Post.objects.filter(poster_id__in=set(influencers)).order_by('-timestamp')
    paginator = Paginator(posts, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
                'page_obj': page_obj
            })

def likeaction(request,postid):
    try:
        usera=User.objects.get(pk=request.user.id)
        post=Post.objects.get(pk=postid)
        liketext='Like'
        lks=post.likes
        if(lks.filter(pk=request.user.id).exists()):
            lks.remove(request.user)
            liketext='Like'
        else:
            lks.add(request.user)
            liketext='Unlike'
        post.save()
        #return json.dumps({"likecount":lks.count(),"liketext":liketext})
        response = json.dumps({"likecount":lks.count(),"liketext":liketext},default=str) 
        
        return HttpResponse(response,content_type = "application/json")
    except:
        raise HttpResponse(status=500)