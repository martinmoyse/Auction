from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Comment, Bidding, Watchlist
from .forms import ListingForm, CommentForm, BidForm


CATEGORIES = (
    ('Art', 'Art'),
    ('Automotive & Powersports', 'Automotive & Powersports'),
    ('Beauty', 'Beauty'),
    ('Books', 'Books'),
    ('Electronics', 'Electronics'),
    ('Musical instruments', 'Musical instruments'),
    ('Pet Supplies', 'Pet Supplies'),
    ('Software', 'Software'),
    ('Sports', 'Sports'),
    ('Tools', 'Tools'),
    ('Toys & Games', 'Toys & Games'),
    ('Watches', 'Watches'),
    ('Other', 'Other'),
)


def index(request):
    all_listings = reversed(Listing.objects.all())
    current_user = request.user
    n = len(Watchlist.objects.filter(account_id=current_user.id))
    context = {
        'all_listings': all_listings,
        'n': n
    }
    current_user = request.user
    return render(request, "auctions/index.html", context)



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

@login_required(redirect_field_name='', login_url='login')
def add_listing(request):
    form = ListingForm(request.POST or None, request.FILES)
    current_user = request.user
    n = len(Watchlist.objects.filter(account_id=current_user.id))
    context = {
        'form': form,
        'n': n
    }
    if request.method == "GET":
        return render(request, "auctions/add_listing.html", context)
    
    if request.method == "POST":   
        if form.is_valid():
            form.save()
            form = ListingForm
        return HttpResponseRedirect(reverse("index"))

def display_listing(request, listing):
    display = Listing.objects.get(pk=listing)
    comment_form = CommentForm(request.POST or None)
    bid_form = BidForm(request.POST or None)
    comments = reversed(Comment.objects.filter(listing_id=listing))
    current_user = request.user
    n = len(Watchlist.objects.filter(account_id=current_user.id))
    context = {
        'listing': display,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'comments': comments,
        'n': n
    }
    if request.method == "POST":
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.author = request.user
            instance.listing = Listing.objects.get(pk=listing)
            instance.save()
            

        if bid_form.is_valid():
            current = Listing.objects.get(pk=listing)
            bid_instance = bid_form.save(commit=False)
            bid_instance.bidder = request.user
            bid_instance.item = Listing.objects.get(pk=listing)
            current_user = request.user
            n = len(Watchlist.objects.filter(account_id=current_user.id))
            if bid_instance.amount > current.starting_bid and bid_instance.amount > current.current_bid:
                bid_instance.save()
                current.current_bid = bid_instance.amount
                current.save()
                context={
                    'bid': bid_instance,
                    'listing': current,
                    'n':n
                }
                return render(request,"auctions/bid_success.html", context)
            else:
                context={
                    'message': "Your bid must be higher than the current one.",
                    'n': n
                }
                return render(request,"auctions/bid_fail.html", context)
        return HttpResponseRedirect(reverse("display_listing", kwargs={'listing': listing}))
    return render(request,"auctions/listing.html", context)
    
def add_to_watchlist(request):
    if request.method == "POST":
        id = request.POST.getlist('id')
        acc = request.user
        watchlist = Watchlist.objects.all()
        for i in range(len(watchlist)):
            if int(id[0]) == watchlist[i].ids.id:
                if acc.id == watchlist[i].account.id:
                    messages.success(request, 'The current item is already in your watchlist.')
                    return HttpResponseRedirect(reverse("display_listing", kwargs={'listing': int(id[0])}))
        w = Watchlist(account=acc, ids=Listing.objects.get(pk=id[0]))
        w.save()
        messages.success(request, 'Item added to watchlist successfully.')
        return HttpResponseRedirect(reverse("display_listing", kwargs={'listing': int(id[0])}))

def watchlist(request):
    if request.method == "GET":
        current_user = request.user
        n = len(Watchlist.objects.filter(account_id=current_user.id))
        watch = Watchlist.objects.filter(account_id=current_user.id)
        keys = []
        values = []

        for i in range(len(watch)):
            keys.append(watch[i].ids.title)
            values.append(watch[i].ids.id)
        mylist = zip(keys, values)
        context = {
            'n': n,
            'list': mylist
        }
        return render(request, "auctions/watchlist.html", context)

def remove_from_watchlist(request):
    if request.method == "POST":
        item_id = request.POST.getlist('id')
        user_id = request.user
        user_id = user_id.id
        Watchlist.objects.get(account=user_id, ids=item_id[0]).delete()
        messages.success(request, 'Item removed successfully.')
        return HttpResponseRedirect(reverse("watchlist"))

def categories(request):
    current_user = request.user
    n = len(Watchlist.objects.filter(account_id=current_user.id))
    watch = Watchlist.objects.filter(account_id=current_user.id)

    categories_count = []

    categories_list = []
    for i in range(len(CATEGORIES)):
        categories_list.append(CATEGORIES[i][0])
        tmp = Listing.objects.all().filter(category=CATEGORIES[i][0])
        categories_count.append(len(tmp))
    selected = []
    categories = zip(categories_list, categories_count)

    context = {
        'n': n,
        'display': selected,
        'categories': categories
    }
    if request.method == "GET":
        return render(request, "auctions/categories.html", context)
    
def display_category(request, category):
    current_user = request.user
    n = len(Watchlist.objects.filter(account_id=current_user.id))
    watch = Watchlist.objects.filter(account_id=current_user.id)
    
    categories_count = []

    categories_list = []
    for i in range(len(CATEGORIES)):
        categories_list.append(CATEGORIES[i][0])
        tmp = Listing.objects.all().filter(category=CATEGORIES[i][0])
        categories_count.append(len(tmp))
    selected = []
    categories = zip(categories_list, categories_count)

    selected = Listing.objects.all().filter(category=category)
    context = {
        'n': n,
        'display': selected,
        'category': category,
        'categories': categories
    }
    return render(request, "auctions/categories.html", context)