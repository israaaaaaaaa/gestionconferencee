from django.urls import path
from .views import *
from .import views
urlpatterns = [
    #path("liste/", views.all_conferences,name="conference_liste")
    path("liste/",conferencelist.as_view(),name="conference_liste"),
    path("details/<int:pk>",conferencedetails.as_view(),name="conference_details" ),
    path("form/",conferencecreate.as_view(),name="conference_add"),
    path("<int:pk>/edit/",conferenceupdate.as_view(),name="conference_edit" ),
    path("<int:pk>/delete/",conferencedelete.as_view(),name="conference_delete" ),


]
