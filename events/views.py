from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm

def events(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'events.html', context)

def eventPage(request,id):
    event = get_object_or_404(Event, id=id)
    context = {'event':event}
    return render(request, 'eventpage.html', context)



@login_required
def save_event(request):
    if request.method == 'POST':
        print('HELLOOOO')
        id = request.POST.get('id','')
        event = get_object_or_404(Event, id=id)
        if request.user.account not in event.saved_by.all():
            event.saved_by.add(request.user.account)
            msg = 'added'
        else:
            event.saved_by.remove(request.user.account)
            msg = 'removed'

        event.save()
        return HttpResponse(msg)

    return HttpResponseBadRequest()

@login_required
def interested_event(request):
    if request.method == 'POST':
        id = request.POST.get('id','')
        event = get_object_or_404(Event, id=id)
        if request.user.account not in event.interested_users.all():
            event.interested_users.add(request.user.account)
            msg = 'added'
        else:
            event.interested_users.remove(request.user.account)
            msg = 'removed'

        event.save()
        return HttpResponse(msg)

    return HttpResponseBadRequest()



def delete_event(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            event = get_object_or_404(Event, id=id)
            if request.user.is_staff:
                event.delete()
                return HttpResponse("success")
        return HttpResponseNotAllowed("Unauthorized")
    return HttpResponseBadRequest("Use GET Method")


def create_edit_event(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        if request.GET.get('id',None)!=None:
            event_obj = get_object_or_404(Event,id=request.GET.get('id'))
            form = EventForm(request.POST, request.FILES, instance=event_obj)
        else:
            form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/admin/events/')
    return HttpResponse('Bad Request',status=400)