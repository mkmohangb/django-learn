from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Flight, Passenger


def index(request):
    print("status of user auth: ", request.user.is_authenticated)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "flights/index.html",
                  {"flights": Flight.objects.all()})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username,
                            password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flights/login.html",
                          {"message": "Invalid Credentials"})

    return render(request, "flights/login.html")

def logout_view(request):
    logout(request)
    return render(request, "flights/login.html",
                  {"message": "Logged out"})

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html",
                  {"flight": flight,
                   "passengers": passengers,
                   "non_passengers": non_passengers})

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))


