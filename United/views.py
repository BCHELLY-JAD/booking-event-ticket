from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from django.urls import reverse
import sys
from datetime import datetime
import time
from .forms import DateForm, CommentForm
import random
from django.forms.models import model_to_dict
from .models import User, Event, Book, Comment, Bot, Ads
from django.db.models import Max

# Chatterbot imports 
from chatterbot.logic import LogicAdapter
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from django.views.decorators.csrf import csrf_exempt



def home(request):
    
    events = Event.objects.filter(is_active=True).order_by('date')

    if 'q' in request.GET: 
        q = request.GET['q']
        events = Event.objects.filter(artist_name__icontains=q, is_active=True).order_by('date')
    else: 
        events = Event.objects.filter(is_active=True).order_by('date')

        
    return render(request, "United/home.html", { 
        "events" : events,
        "not_active": Event.objects.filter(is_active=False),
        "check_booked" : Book.objects.all(),
        "check_events" : Event.objects.all()
    })


def register(request): 
    if request.method == 'POST': 
        username = request.POST['username']
        email = request.POST['email']

        # see if the passwords match
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation: 
            return render(request, 'United/register.html', { 
                'message': 'Passwords must match.'
            })

        # Attempt to create a new user 
        try: 
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, 'United/register.html', { 
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
        
    else: 
        return render(request, 'United/register.html')



def login_view(request):
    if request.method == "POST":

        # Attempt to sign the user in 
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authentication is successful
        if user is not None: 
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "United/login.html", { 
                "message": 'Invalid username and/or password.'
        })

    else: 
        return render(request, "United/login.html")



def logout_view(request): 
    logout(request)
    return HttpResponseRedirect(reverse('home'))
 
 
def createEvent(request):
    form = DateForm()
    if request.method == "POST": 
        user = request.user
        image = request.POST["image"]
        artist_name = request.POST["artist_name"]
        location = request.POST["location"]
        date = request.POST["date"]
        req_format = datetime.strptime(date, "%Y-%m-%d %H:%M")
        req = datetime.strftime(req_format, "%Y-%m-%d %H:%M")
        ticket_num = request.POST['ticket_num']
        ticket_price = request.POST['ticket_price']
        description = request.POST['description']
        information = Event.objects.create(image=image, artist_name=artist_name, event_creator=user ,location=location, date=req, ticket_num=ticket_num, ticket_price=ticket_price, description=description)
        information.save()
        return HttpResponseRedirect(reverse('home'))

    return render(request, "United/create.html", { 
        'form' : form
    })

def view(request, event_id):
    the_ad = False
    book = False
    displayAd = Ads.objects.all()
    maxValue = Ads.objects.all().aggregate(Max('bid'))['bid__max']
    if maxValue:
        the_ad = Ads.objects.get(bid=maxValue)
    else: 
        maxValue = 0

    form = CommentForm()
    list_comment = Comment.objects.filter(comment_list=event_id)
    this_event = Event.objects.get(pk = event_id)
    bookin = Book.objects.filter(reservations=event_id)
    for book in bookin: 
        if book: 
            book = book.ticket_booked

    return render(request, "United/view.html", { 
        'this_event': this_event,
        'form':form,
        'list_comment':list_comment,
        'book':book,
        'the_ad':the_ad,
    })
    
def add_comment(request, event_id): 
    if request.method == "POST": 
        form = CommentForm(request.POST)
        user = request.user
        event = Event.objects.get(pk=event_id)
        if form.is_valid(): 
            text = form.cleaned_data["text"]
            comment = Comment(comment=text, commenter=user, comment_list=event)
            comment.save()
        else: 
            form = CommentForm
        return HttpResponseRedirect(reverse('view', args=(event_id,)))

def book(request, id):
    error = False

    user = request.user
    get_event = Event.objects.get(pk=id)
    # print(get_event)
    price_of_ticket = get_event.ticket_price
    print(price_of_ticket)
    numb_of_ticket = get_event.ticket_num
    ticket_booked = request.POST.get("ticket_booked")
    print(ticket_booked)
    user_av_budget = user.budget
    print(user_av_budget)


    
    if request.method == "POST": 


        prev_book = Book.objects.filter(booker = user, reservations = get_event).exists()
        ## if it exists
        if prev_book:
            book = Book.objects.get(booker = user, reservations = get_event)
            book.ticket_booked += int(ticket_booked)
            book.save()
            return HttpResponseRedirect(reverse("reservation"))

        else: 
            if int(ticket_booked) > numb_of_ticket or price_of_ticket * int(ticket_booked) > user_av_budget: 
                error = "This amount of tickets isn't available or you don't have enough funds"
            else:   
                book = Book(booker = user, ticket_booked = ticket_booked, reservations = get_event)
                book.save()
                new_budget = user_av_budget - price_of_ticket * int(ticket_booked)
                the_user = request.user
                the_user.budget = new_budget
                the_user.save()
                return HttpResponseRedirect(reverse('reservation'))

    return render(request, "United/book.html", { 
        'error' : error,
        'get_event': get_event,
        'numb_of_ticket':numb_of_ticket
    })


def reservation(request):
            
    booked = Book.objects.all()
    events = Event.objects.all().order_by('date')

    return render(request, "United/reservations.html", { 
        'events': events,
        'booked':booked,
    })


def myevents(request):
    return render(request, "United/myevents.html", { 
        'myevents': Event.objects.filter(is_active=True).order_by('date'),
    })



def delete(request, event_id):

    deleted = False

    delete = Event.objects.filter(pk=event_id).update(is_active=False)
    if delete: 
        deleted = True
    return HttpResponseRedirect(reverse('home'))



def account(request, user_id):
    private = User.objects.get(pk=user_id)

    for i in range(1):
        n = random.randint(10,30)
        o = random.randint(10,30)
        p = random.randint(10,30)
        y = random.randint(2022, 2026)
        d = random.randint(1,12)

    return render(request, "United/account.html", { 
        'n':n,
        'o':o,
        'p':p,
        'y':y,
        'd':d,
        'private': private
    })



def like(request, comment_id): 
    if request.method == 'PUT':
        comment = Comment.objects.get(pk=comment_id) 
        print(comment)
        if request.user in comment.likes.all(): 
            print(request.user)
            comment.likes.remove(request.user)
        else: 
            print(request.user)
            comment.likes.add(request.user)
        comment.save()
        return HttpResponse(status=204)



# ChatterBot Section:

english_bot = ChatBot(
    'Mia',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
) 


trainer = ListTrainer(english_bot)

training_bot = open('United/training/train.txt').read().splitlines()
trainer.train(training_bot)
trainer_corpus = ChatterBotCorpusTrainer(english_bot)

trainer_corpus.train(
    'chatterbot.corpus.english'
)


def bot(request): 
    return render(request,"United/bot.html")
 
@csrf_exempt
def give_response(request): 
    if request.method == 'POST': 
        userText = request.POST.get('msg')
        response = str(english_bot.get_response(userText))
        store = Bot(person = request.user, questions = userText, answers = response)
        store.save()
        return JsonResponse(response, safe=False)

def advertise(request): 
    maxValue = False
    message = False
    messageprice = False
    error = False

    displayAd = Ads.objects.all()
    maxValue = Ads.objects.all().aggregate(Max('bid'))['bid__max']
    print(f'max value of all bids: {maxValue}')

    for getAd in displayAd: 
        current_bid = getAd.bid    #is the current bid of an Ad
        print(f'current bid: {current_bid}') 
        latest_bid = displayAd.last().bid   #is the last bid placed on an Ad
        print(f'latest bid: {latest_bid}')

    if request.method == "POST": 
        user = request.user 
        headline = request.POST["headline"]
        web_url = request.POST["web_url"]
        describe = request.POST["describe"] 
        callToAction = request.POST["callToAction"]
        bid = request.POST["bid"]  



        if maxValue is None: 
            maxValue = 0

            # comparing the two bids

        if int(bid) > maxValue:  # if the written bid is higher than the latest bid                       
            message = "Congrats, your Ad will be displayed!"  
            maxValue = int(bid)
            print(message)

        else:
            error = "The Bid must be bigger than the current one so your ad will be displayed"
            print(error)

        adverts = Ads.objects.create(headline = headline, web_url = web_url ,description = describe, advertiser = user, callToAction = callToAction, bid = bid)
        adverts.save()
        

    return render(request,"United/advertise.html", { 
        "message" : message, 
        "error" : error, 
        "maxValue": maxValue,


    })



