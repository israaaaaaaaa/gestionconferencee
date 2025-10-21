from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView
# Create your views here.
def all_conferences(req):
    conferences=Conference.objects.all()
    return render(req,'conference/liste.html',{"liste":conferences})

class conferencelist(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="conference/liste.html"

class conferencedetails(DetailView):
    model=Conference
    template_name="conference/details.html"
    context_object_name="conference"
    