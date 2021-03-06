from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser, models.Model):
    pass

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=69)
    description = models.CharField(max_length=69)
    starting_price = models.IntegerField(null=True)
    current_bid = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=69, null=True)
    active = models.BooleanField(default=True)
    datetime = models.CharField(max_length=69, null=True)
    img = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.seller}: {self.title} is ${self.current_bid}"

class Bid(models.Model):   #should I allow it to inherit
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bidder} places ${self.bid} on {self.item}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=69)

    def __str__(self):
        return f"{self.commenter}: {self.comment}"

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.item}"