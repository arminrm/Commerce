from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser, models.Model):
    pass

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #why?
    title = models.CharField(max_length=69)
    description = models.CharField(max_length=69)
    current_bid = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.seller}: {self.title} is ${self.current_bid}"

class Bid(models.Model):
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

    

