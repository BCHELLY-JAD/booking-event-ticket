from django.contrib import admin

from .models import User, Event, Book, Comment, Bot, Ads
# Register your models here.


admin.site.register(User)
admin.site.register(Event)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Bot)
admin.site.register(Ads)
