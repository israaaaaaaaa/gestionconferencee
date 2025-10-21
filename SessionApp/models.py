from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

room_validator = RegexValidator(
    regex=r'^[A-Za-z0-9\s]+$',
    message="Room name must contain only letters and digits."
)

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=255, validators=[room_validator])

    conference = models.ForeignKey(
        "ConferenceApp.Conference",
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def clean(self):
    # Only validate if conference exists
    if self.conference and self.session_day:
        if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
            raise ValidationError({"session_day": "Session day must fall within the conference duration."})

    # Check start_time < end_time
    if self.start_time and self.end_time:
        if self.end_time <= self.start_time:
            raise ValidationError({"end_time": "End time must be after start time."})

    def __str__(self):
        return f"{self.title} ({self.conference.name})"
