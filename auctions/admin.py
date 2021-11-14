from django.contrib import admin
from .models import User, Category, Listing, Watchlist, Bids, Comments
# Register your models here

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Comments)
