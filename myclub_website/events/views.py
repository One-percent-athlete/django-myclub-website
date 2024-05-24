import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Event, Venue
from .forms import VenueForm, AdminEventForm, UserEventForm

def home(request):
    now = datetime.now()
    current_year = now.year
    return render(request, "events/home.html", {"current_year": current_year})


def calender(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)

    cal = HTMLCalendar().formatmonth(year, month_number)

    now = datetime.now()
    time = now.strftime('%Y-%m-%d %I:%M:%S %p')
    current_year = now.year

    events = Event.objects.filter(
        event_date__year = year, 
        event_date__month = month_number,

        )

    return render(request,
        "events/calender.html", {
        "year": year, 
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "time": time,
        "current_year": current_year,
        "events": events
        })

def all_events(request):
    event_list = Event.objects.all().order_by("event_date", "name")
    now = datetime.now()
    current_year = now.year

    return render(request,
        "events/events.html", {
        "event_list": event_list,
        "current_year": current_year
        })

def search_events(request):
    now = datetime.now()
    current_year = now.year

    if request.method == "POST":
        searched = request.POST['searched']
        events =Event.objects.filter(description__contains=searched)
        return render(request, 
            "events/search_events.html", {
            "current_year": current_year, 
            "searched":searched,
            "events": events 
            })
    else: 
        return render(request, 
            "events/search_events.html", {
            "current_year": current_year, 
            })    

def my_events(request):
    now = datetime.now()
    current_year = now.year
    if request.user.is_authenticated:
        events = Event.objects.filter(attendees=request.user.id)

        return render(request,
            "events/my_events.html", {
            "events": events,
            "current_year": current_year
            })
    else:
        messages.success(request, ("You Are Not Authorised To View This Page..."))
        return redirect("home")


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = AdminEventForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")

        else:
            form = UserEventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect("/add_event?submitted=True")
    else:
        if request.user.is_superuser:
            form = AdminEventForm()
        else:
            form = UserEventForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, 
        "events/add_event.html", {
        "form": form,
        "submitted": submitted
        })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = AdminEventForm(request.POST or None, instance=event)
    else:
        form = UserEventForm(request.POST or None, instance=event)
    
    if form.is_valid():
        form.save()
        return redirect('events')
    now = datetime.now()
    current_year = now.year

    return render(request,
        "events/update_event.html", {
        "event": event,
        "form": form,
        "current_year": current_year
        })

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event Deleted Successfully.")
        return redirect('events')
    else:
        messages.success(request, "You Are Not Authorised To Delete This Event.")
        return redirect('events')


def all_venues(request):
    # venue_list = Venue.objects.all().order_by("name")
    venue_list = Venue.objects.all()

    p = Paginator(venue_list, 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "n" * venues.paginator.num_pages

    now = datetime.now()
    current_year = now.year

    return render(request,
        "events/venues.html", {
        "venue_list": venue_list,
        "venues": venues,
        "nums": nums,
        "current_year": current_year
        })

def search_venues(request):
        now = datetime.now()
        current_year = now.year
        if request.method == "POST":
            searched = request.POST['searched']
            venues =Venue.objects.filter(name__contains=searched)
            return render(request, 
                "events/search_venues.html", {
                "current_year": current_year, 
                "searched":searched,
                "venues": venues 
                })
        else: 
            return render(request, 
                "events/search_venues.html", {
                "current_year": current_year, 
                # "searched":searched
                })    

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    now = datetime.now()
    current_year = now.year

    return render(request,
        "events/show_venue.html", {
        "venue": venue,
        "venue_owner": venue_owner,
        "current_year": current_year
        })

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()

            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm
        if "submitted" in request.GET:
            submitted = True
    return render(request, 
        "events/add_venue.html", {
        "form": form,
        "submitted": submitted
        })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venues')
    now = datetime.now()
    current_year = now.year

    return render(request,
        "events/update_venue.html", {
        "venue": venue,
        "form": form,
        "current_year": current_year
        })

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venues')

def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=venues.txt"

    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.email_address}\n{venue.web}\n\n\n')

    response.writelines(lines)
    return response

def venue_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=venues.csv"

    venues = Venue.objects.all()

    writer = csv.writer(response)

    writer.writerow(["Venue Name","Zipcode","Address","Phone","Email","Website",])

    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.email_address,venue.web])

    return response

def venue_pdf(request):
    #create Bystream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    #add lines of text
    venues = Venue.objects.all()
    lines = []

    for venue in venues:
        lines.append(f'Venue Name: {venue.name}')
        lines.append(f'Zipcode: {venue.zip_code}')
        lines.append(f'Address: {venue.address}')
        lines.append(f'Phone: {venue.phone}')
        lines.append(f'Email: {venue.email_address}')
        lines.append(f'Website: {venue.web}')
        lines.append("  ")

    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="venue.pdf")
    

def search_keywords(request):
    now = datetime.now()
    current_year = now.year
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        events = Event.objects.filter(description__contains=searched)
        return render(request, 
            "events/search_keywords.html", {
            "current_year": current_year, 
            "searched":searched,
            "venues": venues,
            "events": events 
            })
    else: 
        return render(request, 
            "events/search_keywords.html", {
            "current_year": current_year, 
            "searched":searched
            })    
    