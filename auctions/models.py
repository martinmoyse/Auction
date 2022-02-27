from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import int_list_validator
from django.db.models.enums import Choices
from django.db.models.fields.related import ForeignKey

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

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000, blank=True)
    starting_bid = models.DecimalField(max_digits=11, decimal_places=2, blank=False)
    current_bid = models.DecimalField(max_digits=11, default=0, decimal_places=2)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, blank=False)

class Comment(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

class Bidding(models.Model):
    bidder = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="")
    time = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    account = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    ids = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE)
