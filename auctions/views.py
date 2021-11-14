from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Avg, Max, Min
from .models import User, Category, Listing, Bids, Comments, Watchlist

from .forms import ImageForm


def index(request):
    if request.method == "POST":
        item = request.POST["item"]
        descript = request.POST["descript"]
        bid = request.POST["bid"]
        #print(file_path)
        #user = User.objects.get(username = requets.)
        if "file_path" in request.FILES:
            if "category" in request.POST:
                cate = Category.objects.get(id = request.POST["category"])
                listing = Listing.objects.create(seller = request.user, item = item, descript = descript, file_path = request.FILES["file_path"], category = cate)
            else:
              listing = Listing.objects.create(seller = request.user, item = item, descript = descript, file_path = request.FILES["file_path"])  
        else:
            if "category" in request.POST:
                cate = Category.objects.get(id = request.POST["category"])
                listing = Listing.objects.create(seller = request.user, item = item, descript = descript, category = cate)
            else:
              listing = Listing.objects.create(seller = request.user, item = item, descript = descript)  
        listing.save()
    
        #print(listing + '\n' + listing.item)
        bid = Bids.objects.create(auction_listing = listing, bid = bid) # 
        #print(Bids + '\n' + listing.product)
       
        bid.save()
       
        return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all(),
        "header": "Active Listings"
        })
    else:
        return render(request, "auctions/index.html", { 
        "listings" : Listing.objects.all(),
        "header": "Active Listings"
        })

def login_view(request, listing_id = None):
    if request.method == "POST":
    
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if listing_id is not None:
                listing = Listing.objects.get( id = listing_id )
                max_bid = listing.bids_on_product.aggregate(max_bid = Max('bid'))['max_bid']
                bid = Bids.objects.get(auction_listing = listing_id, bid = int(max_bid))
                if listing.closed and request.user == bid.Bidder:
                     messages.info(request, 'You Won The Auction')
                return render(request,"auctions/page.html",{
                     "listing" : listing,
                     "bid" : max_bid
                     })
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "u"
            })
    else:
        if listing_id is not None:
            return render(request, "auctions/login.html",
            { "listing_id" : listing_id })   

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
def create(request):
    form = ImageForm
    return render(request, "auctions/create.html",
    {"form": form}
    )

def listing(request, listing_id):
    
    auction = Listing.objects.get(id = listing_id)
    max_bid = auction.bids_on_product.aggregate(max_bid = Max('bid'))['max_bid']
    if request.method == "POST":
        text = request.POST["comment-text"]
        newComment = Comments.objects.create(product = auction, comment = text)
        newComment.save()
# error might be produced because the page needs an id 
# return HttpResponseRedirect(reverse("listing"))
        bid = Bids.objects.get(auction_listing = listing, bid = int(max_bid))
        if listing.closed and request.user == bid.Bidder:
            messages.info(request, 'You Won The Auction')
        return render(request, "auctions/page.html", { 
        "listing" : auction,
        "bid": max_bid
        })
    else:
        bid = Bids.objects.get(auction_listing = listing_id, bid = int(max_bid))
        if auction.closed and request.user == bid.Bidder:
            messages.info(request, 'You Won The Auction')
        return render(request, "auctions/page.html", { 
        "listing" : auction,
        "bid": max_bid
        })
   
def watchlist(request, listing_id = None):
    if request.method == "POST" and listing_id is not None:
        listing = Listing.objects.get(id = listing_id)
        max_bid = listing.bids_on_product.aggregate(max_bid = Max('bid'))["max_bid"]
        # added = request.POST.get("added", False)
        # removed = request.POST.get("removed", False) 
        if "added" in request.POST:
            if request.user.user_watchlist.first() is None:
                wl = Watchlist(user = request.user)
                wl.save()
            else:
                wl = request.user.user_watchlist.first()
            #print("The Auction Listing is " + str(wl))
            wl.watching.add(listing)
            #request.POST.pop("added")
            #wl.save()
            #print("The Auction Listing is " + str(wl))print() 
            
        elif "removed" in request.POST:
            wl = request.user.user_watchlist.first()
            wl.watching.remove(listing)
            #request.POST.pop("removed")
            #print("Hi What's Up??")
        print("GOT TO THE FUNCTION NEW_BID")
        return render(request, "auctions/page.html", { 
        "listing" : listing,
        "bid": max_bid
        })

    else:
        wl = Watchlist.objects.get( user = request.user )
    
        return render( request, "auctions/index.html",{
        "listings" : wl.watching.all(),
        "header": "Watchlist"
        })
def categories(request, category = None):
    if category is not None:
        cat = Category.objects.get(category = category)
        listings = Listing.objects.filter(category = cat)
        return render( request, "auctions/index.html",{
        "listings" : listings,
        "header": category
        })
    else:
        categories = Category.objects.all()
        return render(request, "auctions/categories.html", {
        "categories" : categories
    })
def new_bid(request, listing_id):
    print("GOT TO THE FUNCTION NEW_BID")
    bid = request.POST["bid"] 
    listing = Listing.objects.get(id = listing_id)
    max_bid = listing.bids_on_product.aggregate(max_bid = Max('bid'))['max_bid']
    if int(bid) > max_bid:
        print("NEW BID")
        new_bid = Bids.objects.create(Bidder = request.user, auction_listing = listing, bid = bid)
        new_bid.save()
        return render(request,"auctions/page.html",{
            "listing" : listing,
            "bid": new_bid.bid

        })
    else:
        print(" NO NEW BID")
        messages.error(request, 'Bid too Low')
        return render(request,"auctions/page.html",{
            "listing" : listing,
            "bid": max_bid

        })
def close_auction(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    listing.closed = True
    listing.save()
    winning_bid = listing.bids_on_product.order_by('bid').last()
    winning_bid.won = True
    winning_bid.save()
    if listing.closed and request.user == winning_bid.Bidder:
        messages.info(request, 'You Won The Auction')
    return render(request,"auctions/page.html",{
            "listing" : listing

        })


    