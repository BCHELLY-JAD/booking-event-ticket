from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    budget = models.IntegerField(blank = False, default = 1000)


class Event(models.Model): 
    image = models.URLField(blank=True, max_length=200)
    artist_name = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    ticket_num = models.IntegerField()
    ticket_price = models.IntegerField()
    event_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)


class Book(models.Model): 
    ticket_booked = models.IntegerField()
    booker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mytickets')
    reservations = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reserved")


class Comment(models.Model): 
    comment_list = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=250, blank=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="com_owner")
    time = models.DateTimeField(auto_now=True, auto_now_add=False)
    likes = models.ManyToManyField(User)

    def likes_count(self): 
        return self.likes.count()

    def serialize(self): 
        return { 
            "likes": self.liked
        }

class Bot(models.Model): 
    person = models.ForeignKey("User", on_delete=models.CASCADE, related_name="personal")
    questions = models.CharField(max_length = 255) 
    answers = models.CharField(max_length = 255)



class Ads(models.Model): 
    headline = models.CharField(max_length = 60)
    web_url = models.URLField(blank=False, max_length=200,null=True)
    description = models.CharField(max_length= 90)
    callToAction = models.CharField(max_length = 15) 
    advertiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advert')
    bid = models.IntegerField()