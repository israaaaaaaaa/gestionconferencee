from django import forms
from .models import Conference
class conferencemodel(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ("name","theme","description","location","start_date","end_date")
        labels={
            "name":"nom de la conference",
            "theme":"thematique",
            "description":"description",
            "start_date":"date debut de la conference",
            "end_date":"date fin de la conference", 
        }
        widgets={
            "start_date": forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de debut"
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':'date fin'
                }
            ),
            "name": forms.TextInput(
                attrs={
                    'placeholder':'nom'
                }
            )          
        }
