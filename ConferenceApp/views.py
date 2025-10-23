from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import conferencemodel
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
    
class conferencecreate(CreateView):
    model = Conference
    template_name = "conference/conference_form.html"
    #fields="__all__"
    form_class=conferencemodel
    success_url=reverse_lazy("conference_liste")
    
class conferenceupdate(UpdateView):
    model = Conference
    template_name = "conference/conference_form.html"
    #fields="__all__"
    form_class=conferencemodel
    success_url=reverse_lazy("conference_liste")
    
class conferencedelete(DeleteView):
    model = Conference
    template_name = "conference/conference_confirm_delete.html"
    success_url=reverse_lazy("conference_liste")
    
    