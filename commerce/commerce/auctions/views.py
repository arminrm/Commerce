from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *
from django import forms
from datetime import datetime

CATEGORIES = [
    ('Technology', 'Technology'),
    ('Fashion', 'Fashion'),
    ('Sports', 'Sports'),
    ('Toys', 'Toys'),
    ('Books', 'Books'),
    ('Music', 'Music'),
    ('Other', 'Other')
]

class CreateNewListing(forms.Form):
    title = forms.CharField(max_length=67)
    description = forms.CharField(max_length=67)
    category = forms.ChoiceField(choices=CATEGORIES)
    starting_price = forms.IntegerField(min_value=0)
    image = forms.ImageField()

class BidOnListing(forms.Form):
    place_bid = forms.IntegerField(min_value=0, required=False)

class CommentOnListing(forms.Form):
    comment = forms.CharField(max_length=67, required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def create(request):

    seller = User.objects.get(id= request.session['user'])

    if request.method == "POST":
        form = CreateNewListing(request.POST, request.FILES)
        time_created = str(datetime.now())
        if form.is_valid():
            Listing(seller= seller, title= form.cleaned_data["title"], description= form.cleaned_data["description"], category=form.cleaned_data["category"], starting_price= form.cleaned_data["starting_price"], datetime= time_created, img=form.cleaned_data["image"]).save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
                "form": CreateNewListing()
            })

    return render(request, "auctions/create.html", {
        "form": CreateNewListing()
    })

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bidder = User.objects.get(id= request.session['user'])
    watch_list = Watchlist.objects.filter(watcher= bidder, item= listing).exists()
    print(watch_list)

    if Comment.objects.filter(item= listing).exists():   
        comments = Comment.objects.filter(item= listing)
    else:
        comments = False

    if request.method == "POST":  # you could do this more efficiently using tags on forms...
        if bidder != listing.seller:
            if "bid" in request.POST: 
                action = BidOnListing(request.POST) 
                if action.is_valid():
                    if listing.current_bid != None and action.cleaned_data["place_bid"] > listing.current_bid:
                        listing.current_bid = action.cleaned_data["place_bid"]
                        listing.save()
                        Bid(bidder= bidder, item= listing, bid= action.cleaned_data["place_bid"] ).save()
                        if watch_list != True:
                            Watchlist(watcher= bidder, item=listing).save()
                    elif listing.current_bid != None and action.cleaned_data["place_bid"] <= listing.current_bid:
                        return render(request, "auctions/listing.html", {
                            "listing": listing,
                            "bid_action": action,
                            "comment_action": CommentOnListing(),
                            "message": "Bid must be higher than current price.", 
                            "comments": comments,
                            "bidder": bidder,
                            "watchlist": watch_list
                        })
                    elif listing.current_bid == None:
                        if action.cleaned_data["place_bid"] > listing.starting_price:
                            listing.current_bid = action.cleaned_data["place_bid"]
                            listing.save()
                            Bid(bidder= bidder, item= listing, bid= action.cleaned_data["place_bid"] ).save()
                            if watch_list != True:
                                Watchlist(watcher= bidder, item=listing).save() 
                        else:
                            return render(request, "auctions/listing.html", {
                                "listing": listing,
                                "bid_action": action,
                                "comment_action": CommentOnListing(),
                                "message": "Bid must be higher than current price.", 
                                "comments": comments,
                                "bidder": bidder,
                                "watchlist": watch_list
                            })
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "bid_action": action, 
                        "comment_action": CommentOnListing(),
                        "comments": comments,
                        "bidder": bidder,
                        "watchlist": watch_list
                    })

            elif "comment_action" in request.POST:
                action = CommentOnListing(request.POST)

                if action.is_valid():
                    Comment(commenter= bidder, item= listing, comment= action.cleaned_data["comment"]).save()
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "bid_action": BidOnListing(),
                        "comment_action": action, 
                        "comments": comments,
                        "bidder": bidder,
                        "watchlist": watch_list
                    })


            elif "watchlist" in request.POST:
                if watch_list == False:
                    Watchlist(watcher= bidder, item= listing).save()
            elif "remove-watchlist" in request.POST:
                Watchlist.objects.filter(watcher= bidder, item= listing).delete()

        else:

            listing.active = False
            listing.save()
  
            if Bid.objects.filter(item=listing).exists():
                Bid.objects.filter(item= listing).exclude(bid= listing.current_bid).delete()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_action": BidOnListing(),
        "comment_action": CommentOnListing(),
        "comments": comments,
        "bidder": bidder, 
        "exists": Bid.objects.filter(item= listing).exists(),
        "bids": Bid.objects.filter(item= listing),
        "watchlist": watch_list
    })

def watchlist(request):
    watch_list = Watchlist.objects.filter(watcher= User.objects.get(id= request.session["user"]))
    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_list
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=category),
        "category": category,
        "categories": CATEGORIES
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            request.session["user"] = user.id
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
        request.session["user"] = user.id
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")