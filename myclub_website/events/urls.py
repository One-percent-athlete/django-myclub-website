from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('calender', views.calender, name="calender"),
    path('calender/<int:year>/<str:month>/', views.calender, name="calender"),
    path('dashboard', views.dashboard, name="dashboard"),

    path('events', views.all_events, name="events"),
    path('add_event', views.add_event, name="add_event"),
    path('my_events', views.my_events, name="my_events"),
    path('search_events', views.search_events, name="search_events"),
    path('show_event/<event_id>', views.show_event, name="show_event"),
    path('update_event/<event_id>', views.update_event, name="update_event"),
    path('delete_event/<event_id>', views.delete_event, name="delete_event"),
    
    path('venues', views.all_venues, name="venues"),
    path('add_venue', views.add_venue, name="add_venue"),
    path('search_venues', views.search_venues, name="search_venues"),
    path('show_venue/<venue_id>', views.show_venue, name="show_venue"),
    path('update_venue/<venue_id>', views.update_venue, name="update_venue"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete_venue"),
    path('venue_text', views.venue_text, name="venue_text"),
    path('venue_csv', views.venue_csv, name="venue_csv"),
    path('venue_pdf', views.venue_pdf, name="venue_pdf"),

    path('venue_events/<venue_id>', views.venue_events, name="venue_events"),
    path('search_keywords', views.search_keywords, name="search_keywords"),
]