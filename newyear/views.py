from django.shortcuts import render
from datetime import datetime

def index(request):
    now = datetime.now()
    return render(request, "newyear/index.html",
                  {"newyear": now.month == 1 and now.day == 1})
