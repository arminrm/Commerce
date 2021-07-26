from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms


class CreateNewListing(forms.Form):
    title = forms.CharField(max_length=67)
    description = forms.CharField(max_length=67)
    price = forms.IntegerField()

class ActionOnListing(forms.Form):
    place_bid = forms.IntegerField(required=False)
    comment = forms.CharField(max_length=67, required=False)

def index(request):
    #for listing in Listing.objects.all():  
        #bid_price = Bid.objects.filter(item=listing)
        #for price in bid_price:
            #if price.bid > listing.current_price:
                #listing.current_price = price.bid
                #listing.save()

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def create(request):

    seller = User.objects.get(id= request.session['user'])

    if request.method == "POST":
        form = CreateNewListing(request.POST)
        if form.is_valid():
            Listing(seller= seller, title= form.cleaned_data["title"], description= form.cleaned_data["description"], current_bid= form.cleaned_data["price"]).save()
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

    if Comment.objects.filter(item= listing).count() > 0:   #we could also use queryset...
        comments = Comment.objects.filter(item= listing)
    else:
        comments = False

    if request.method == "POST":
        if bidder != listing.seller:
            action = ActionOnListing(request.POST)
            if action.is_valid(): #let user know that bid must be higher than current price...? #create sep class for bid and listing
                if action.cleaned_data["place_bid"] != None and action.cleaned_data["place_bid"] > listing.current_bid:
                    listing.current_bid = action.cleaned_data["place_bid"]
                    listing.save()
                    Bid(bidder= bidder, item= listing, bid= action.cleaned_data["place_bid"] ).save()
                elif action.cleaned_data["place_bid"] != None and action.cleaned_data["place_bid"] <= listing.current_bid:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "form": action,
                        "message": "Bid must be higher than current price.", 
                        "comments": comments,
                        "bidder": bidder
                    })

                if action.cleaned_data["comment"] != "":
                    Comment(commenter= bidder, item= listing, comment= action.cleaned_data["comment"]).save()

            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": action, 
                    "comments": comments,
                    "bidder": bidder
                })
       # else:
            #if Bid.objects.filter(bid= listing.current_bid)
                #buyer = Bid.objects.get(bid= listing.current_bid)
                #print(f"{buyer.bidder} wins!")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": ActionOnListing(),
        "comments": comments,
        "bidder": bidder
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