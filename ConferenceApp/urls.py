from django.urls import path
from .views import *
from .import views
urlpatterns = [
    #path("liste/", views.all_conferences,name="conference_liste")
    path("liste/",conferencelist.as_view(),name="conference_liste"),
    path("details/<int:pk>",conferencedetails.as_view(),name="conference_details" )
]
