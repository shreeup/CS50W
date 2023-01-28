from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
import pdb
from django import forms
import re
from django.forms import ModelForm

from .models import User,Listing,Bid,Category,Comment

class NewEntryForm(forms.Form):
    messages=[]
    name = forms.CharField(
        required=True,
        label="Name",
        widget=forms.TextInput(
            attrs={"placeholder": "name", "class": "mb-4 form-control"}
        ),
    )
    description = forms.CharField(
        required=True,
        label="Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Description",
                "id": "new_content",
            }
        ),
    )
    price = forms.DecimalField(
        required=True,
        label="Price",
        widget=forms.TextInput(
            attrs={"placeholder": "price", "class": "mb-4 form-control"}
        ),
    )
    startingbid = forms.DecimalField(
        required=True,
        label="First Bid",
        widget=forms.TextInput(
            attrs={"placeholder": "firstbid", "class": "mb-4 form-control"}
        ),
    )
    category=forms.ChoiceField(required=True,label="Category",choices=[],widget=forms.Select(attrs={'class':'mb-4 form-control'}))
    img_url = forms.CharField(
        required=True,
        label="Image URL",
        widget=forms.TextInput(
            attrs={"placeholder": "image url", "class": "mb-4 form-control"}
        ),
    )
    # comment= forms.CharField(
    #     required=True,
    #     label="Comment",
    #     widget=forms.Textarea(
    #         attrs={
    #             "class": "form-control mb-4",
    #             "placeholder": "review",
    #             "id": "new_comment",
    #         }
    #     ),
    # )

    def __init__(self, *args, **kwargs):
        super(NewEntryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(x.pk, x.name) for x in Category.objects.all()]

class BidEntryForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['offer']

    # newprice = forms.CharField(
    #     required=True,
    #     label="new price",
    #     widget=forms.TextInput(
    #         attrs={"placeholder": "offer", "class": "mb-4 form-control"}
    #     ),
    # )


class CommentEntryForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
    

def index(request):
    #return render(request, "auctions/index.html")
    return render(request, "auctions/index.html", {
        "listing": Listing.objects.filter(isactive=True)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        iscreator=listing.creator==request.user
        ispurchaser=listing.purchaser==request.user
        comments=Comment.objects.filter(auction=listing)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {
        "listing": listing,
       "activewatcher":listing.watchers.filter(pk=request.user.id).exists(),
       "bidform":BidEntryForm(),
       "commentform":CommentEntryForm(),
       "iscreator":iscreator,
       "isbidder":ispurchaser,
       "reviews":comments
    })

def add(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            sbid=form.cleaned_data["startingbid"]
            category_id = form.cleaned_data["category"]
            cobj= Category.objects.get(id=category_id)
            image_url=form.cleaned_data["img_url"]
            creator=request.user
            
            newentry=Listing(name=name,description=description,price=price,isactive=True,
            startingbid=sbid,category=cobj,image_url=image_url,creator=creator)
            newentry.save()
            return HttpResponseRedirect(reverse("index"))
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/new.html", {
                "form": form
            })

    return render(request, "auctions/new.html", {
        "form": NewEntryForm()
    })




def categories(request,category_id=None):
    if(category_id==None):
        return render(request, "auctions/category.html", {
            "categories": Category.objects.all()
        })
    else:
        try:
            #category_id=args
            category = Category.objects.get(id=category_id)
            product=get_object_or_404(Listing,category=category)
        except category.DoesNotExist or product.DoesNotExist:
            raise Http404("Listing not found.")
        return render(request, "auctions/listing.html", {
            "listing": product
        })

def watchlist(request):
    if(request.user==None):
        return render(request, "auctions/login.html")
    else:
        #try:
            #watches = [p for p in Listing.objects.all() if request.user in p.watchers]
        listing=Listing.objects.all()
        # abc=list(filter(lambda x: request.user in x.watchers,listing))
        # watches=[]
        watches=Listing.objects.filter(watchers__id__icontains=request.user.id)
        # except watches.DoesNotExist:
        #     raise Http404("Watchlist not found.")
        return render(request, "auctions/watchlist.html", {
            "watchlist": watches
        })


def addwatch(request,listing_id):
    
    if(listing_id==None):
        return HttpResponseBadRequest()
    else:
        listing=Listing.objects.get(pk=listing_id)
        if(listing.watchers.filter(pk=request.user.id).exists()):
            listing.watchers.remove(request.user)
        else:
            listing.watchers.add(request.user)
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def addbid(request,listing_id):
    if(listing_id==None):
        return HttpResponseBadRequest()
    else:
        form = BidEntryForm(request.POST or None)
        listing=Listing.objects.get(pk=listing_id)
        if form.is_valid():
            newprice = form.cleaned_data["offer"]
            newbid = form.save(commit=False)
            currentbids=Bid.objects.filter(auction=listing_id)
            if(currentbids.count()>0 and currentbids.filter(offer__gt=newprice).exists()):
                #listing.watchers.remove(request.user)
                return HttpResponseBadRequest("Bid request rejected since there is another active bid")
            else:
                newbid.auction=listing
                newbid.bidder=request.user
                newbid.offer=newprice
                newbid.save()
                listing.purchaser=request.user
                listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "activewatcher":listing.watchers.filter(pk=request.user.id).exists(),
                "bidform":form,
                "commentform":CommentEntryForm()
            })

def addcomment(request,listing_id):
    if(listing_id==None):
        return HttpResponseBadRequest()
    else:
        form = CommentEntryForm(request.POST or None)
        listing=Listing.objects.get(pk=listing_id)
        if form.is_valid():
            newcomment = form.cleaned_data["comment"]
            newcomment = form.save(commit=False)
            currentcomments=Comment.objects.filter(auction=listing_id)
            
            newcomment.auction=listing
            newcomment.commentator=request.user
            newcomment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "activewatcher":listing.watchers.filter(pk=request.user.id).exists(),
                "bidform":BidEntryForm(),
                "commentform":form
            })

def deactivate(request,listing_id):
    if(listing_id==None):
        return HttpResponseBadRequest()
    else:
        listing=Listing.objects.get(pk=listing_id)
        listing.isactive=False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
       

  

