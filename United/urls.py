from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"), 
    path("logout", views.logout_view, name="logout"),
    path("create", views.createEvent, name="create"),
    path("event/<int:event_id>", views.view, name="view"),
    path("event/<int:id>/book", views.book, name="book"),
    path("Myevents", views.myevents, name="myevents"),
    path("reservations", views.reservation, name="reservation"),
    path("deleted/event/<int:event_id>", views.delete, name="delete"),
    path("account/<int:user_id>", views.account, name="account"),
    path("event/comment/<int:event_id>", views.add_comment, name="add"), 
    path("like/<int:comment_id>", views.like, name="like"),
    path("bot", views.bot, name="bot"),
    path("get", views.give_response, name="response"),
    path("Ads", views.advertise, name="advertise"),

]