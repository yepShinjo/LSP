from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserForm, auctionForm, MyUserCreationForm
from .models import User, auction, bid, komen, category
from django.db.models import Q
from django.db.models import Max




def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    auctions = auction.objects.filter(
        Q(auction_name__icontains=q) |
        Q(description__icontains=q)
    )

    context = {'auctions': auctions}

    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        


        # Check if authentication successful
        if user:
            login(request, user)
            return redirect('/')

        else:
            return HttpResponse('wait wat huh')

    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')

        else:
            messages.error(request, "username / password is sus")
            print(request, "susge")
    
    return render(request, 'auctions/register.html', {
        "form": MyUserCreationForm
    })

@login_required(login_url='login')
def createListing(request):

    user = request.user
    form = auctionForm()
    context = {'form': form}

    if request.method == "POST":
        form = auctionForm(request.POST, request.FILES) # request.FILES basically taking the enctype from our frontend, and process it so the user can submit the form
        print(request.POST)
        if form.is_valid():
            print('it is valid')
            auction = form.save(commit=False)
            auction.host = request.user
            auction.save()
        else:
            return HttpResponse('check ur image format. make sure its pog')

        return redirect('index')

    if request.method == "GET":
        return render(request, "auctions/createListing.html", context)

def auctionRoom(request, pk):

    thisAuction = auction.objects.get(id=pk) # the variabel name cannot be the same as the model name that's why im using "thisAuction" instead of just auction as the var name
    thisAuction_id = thisAuction.id
    thisAuction_host = thisAuction.host.name

    auction_name = thisAuction.auction_name
    image = thisAuction.images
    auction_category = thisAuction.category
    description = thisAuction.description

    participants_auction = thisAuction.participants.all()

    initial_price = thisAuction.initial_price

    comments = thisAuction.komen_set.all()
    
    statusLelang = thisAuction.auction_status
    # winner2 = thisAuction.bid_set.all().aggregate(Max('new_price'))
    # winner_name = winner2.user.name
    # winner = int(winner2['new_price__max'])


    #thisAuction.bid_set.all()
    #if auction.auction_status == True:
    if request.method == 'POST': 
        price = int(request.POST["price"])

        auction_prices = thisAuction.bid_set.all()
        
        highest_price2 = auction_prices.aggregate(Max('new_price'))
        
        try:
            highest_price = int(highest_price2['new_price__max'])
        except TypeError:
            highest_price = 0
        

        if price > initial_price:
            if price > highest_price:
                newbid = bid.objects.create(
                    user = request.user,
                    auction_in = thisAuction,
                    new_price = request.POST.get('price')
                )
                thisAuction.participants.add(request.user)

        else:
            messages.error(request, "ur bid is too smoll")

        return redirect('auctionRoom', pk=thisAuction.id)


    winner = None
    
    all_bid = thisAuction.bid_set.all().order_by('-new_price')
    if all_bid:
        winner = all_bid[0]
        

    context = {'thisAuctions': thisAuction, 'auction_name': auction_name, 'image': image, 'auction_category': auction_category, 
                'description': description, 'participants': participants_auction, 'initial_price': initial_price, 'update_price': all_bid, 
                'thisAuction_id': thisAuction_id, 'comments': comments, 'thisAuction_host': thisAuction_host, 'statusLelang': statusLelang,
                'winner': winner}

    return render(request, "auctions/auctionRoom.html", context)


@login_required(login_url='login')
def closeAuction(request, pk):
    thisAuction = auction.objects.get(id=pk)
    print(request.user)
    print(thisAuction.host)

    if request.user != thisAuction.host:
        return HttpResponse('ur not allowed todo this mate')

    if request.method == "POST":
        thisAuction.auction_status = False
        thisAuction.save()
        return redirect('auctionRoom', pk=thisAuction.id)

    context = {'thisAuction': thisAuction}

    return render(request, "auctions/closeAuction.html", context)


@login_required(login_url='login')
def yepcom(request, pk):
    thisAuction = auction.objects.get(id=pk)
    print(thisAuction.id)
    user = request.user

    if request.method == "POST":
        
    # add that message to the model
        comment = komen.objects.create(
            user = user,
            auction_in = thisAuction,
            body = request.POST.get('body')
        )
        return redirect('auctionRoom', pk=thisAuction.id)
    
    context = {'thisAuction': thisAuction}

    return render(request, "auctions/komenan.html", context)



@login_required(login_url='login')
def watchlist(request, pk):
    thisAuction = auction.objects.get(id=pk)
    print(thisAuction)
    user = request.user

    if request.method == "POST":


        if thisAuction in user.watchlist.all():
        #if thisAuction and user not in watchlist.auction_in and watchlist.user_in :

            user.watchlist.remove(thisAuction)
            print(user.watchlist.all())
            return redirect('index')
            
        
        if thisAuction not in user.watchlist.all():

            user.watchlist.add(thisAuction)
            print(user.watchlist.all())
            return redirect('index')

    context = {'obj': thisAuction}

    return render(request, "auctions/watchlist.html", context)

@login_required(login_url='login')
def myWatchlist(request):

    user = request.user
    user_watchlist = user.watchlist.all()
    #print()

    context = {'user_watchlist': user_watchlist}

    return render(request, "auctions/myWatchlist.html", context)

def allCategory(request):
    allCategory = category.objects.all()

    context = {'allCategory': allCategory}
    print(allCategory)

    return render(request, "auctions/allCategory.html", context)

def oneCategory(request, pk): # REMEMBER function name CANNOT be the same as model name
    oneCategory = category.objects.get(id=pk)
    categoryAuction = oneCategory.auction_set.all()

    context = {'oneCategory': oneCategory, 'categoryAuction': categoryAuction}

    return render(request, "auctions/category.html", context)