"""Remember that each time you change anything in auctions/models.py, 

you will need to first run 

python manage.py makemigrations 

and then 

python manage.py migrate 

to migrate those changes to your database."""


from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): 
     name = models.CharField(max_length=200, null=True)
     email = models.EmailField(null=True, unique=True)
     bio = models.TextField(null=True)
     watchlist = models.ManyToManyField('auction', blank=True)
     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []

class category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class auction(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(category, on_delete=models.SET_NULL, null=True)
    auction_name = models.CharField(max_length=200)
    images = models.ImageField(null=True, default="Clueless.png")
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    initial_price = models.IntegerField()
    auction_status = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.auction_name


class bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_in = models.ForeignKey(auction, on_delete=models.CASCADE)
    new_price = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.new_price)
        

class komen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_in = models.ForeignKey(auction, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body