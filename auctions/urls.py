from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("login", views.login_view, name="login"),
    path("login/<int:listing_id>/", views.login_view, name = "forComment"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("listing/<int:listing_id>" , views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name = "editWatchlist"),
    path("categories", views.categories, name = "categories"),
    path("categories/<str:category>", views.categories, name = "category"),
    path("bid/<int:listing_id>", views.new_bid, name = "bid"),
    path("closed/<int:listing_id>", views.close_auction, name = "close")
    
]
