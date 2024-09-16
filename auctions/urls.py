from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("auction/<str:pk>/", views.auctionRoom, name="auctionRoom"),
    
    path("createListing", views.createListing, name="createListing"),
    #path("auctionRoom/<str:pk>/", views.auctionRoom, name="auctionRoom"),
    path("watchlist/<str:pk>/", views.watchlist, name="watchlist"),
    path("myWatchlist", views.myWatchlist, name="myWatchlist"),

    path("allCategory", views.allCategory, name="allCategory"),
    path("category/<str:pk>", views.oneCategory, name="category"),

    path("komenan/<str:pk>/", views.yepcom, name="yepcom"),

    path("closeAuction/<str:pk>/", views.closeAuction, name="closeAuction")
]
