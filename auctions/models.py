from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class AuctionListing(models.Model):
#    # seller = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "auctions")
#     item = models.CharField(max_length=500, default="") 
#     descript = models.TextField() 
#     file_path = models.ImageField(upload_to = 'imgaes/',null=True, verbose_name="") 
#     #blank allows the passing of null values: form validation will allow entry of an empty value,
#     # null allows the db to accept null values: that means it has two possible values for “no data”: NULL
#     def __str__(self):
#         return self.item + ": " + str(self.file_path)
#         # return "Product: {} ".format(self.item)
class Category(models.Model):
    category = models.CharField(max_length = 500)
    def __str__(self):
        return "this category is " + self.category + "."
class Listing(models.Model):
    seller = models.ForeignKey("User",
                                on_delete = models.CASCADE,
                                related_name = "auctions")
    item = models.CharField(max_length = 500,default = "")
    descript = models.TextField() 
    category = models.ForeignKey(Category,
                                 on_delete = models.PROTECT,
                                 null=True,
                                 blank=True)
    file_path = models.ImageField(upload_to = 'imgaes/', default = 'imgaes/default.jpeg', verbose_name="")
    closed = models.BooleanField(default = False)
    def __str__(self):
        return "{}".format(self.item)

class Bids(models.Model):
    Bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bids", blank = True, null=True)
    auction_listing = models.ForeignKey(
        Listing,
        on_delete = models.CASCADE,
        related_name = "bids_on_product"
    )
    bid = models.IntegerField()
    won = models.BooleanField(default = False)
    def __str__(self):
        return "{}: bids at {}".format(self.auction_listing.item, self.bid )
        #return "bids at {}".format(self.bid)
    
class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        primary_key = True,
        unique = True,
        on_delete = models.CASCADE,
        related_name = "user_watchlist"
    )
    watching = models.ManyToManyField(Listing)
    def __str__(self):
        return "{} is watching these auctions: {}".format(self.user, self.watching.all())
        #return "{} is watching these auctions: ".format(self.username)

class Comments(models.Model):
    comment = models.TextField()
    product = models.ForeignKey(
        Listing,
        on_delete = models.CASCADE,
        related_name = "comments_on_product"
    )
