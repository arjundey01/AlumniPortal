from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from .models import Event

def events(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'events.html', context)

def eventPage(request):
    context = {
        
    }
    return render(request, 'eventpage.html', context)
