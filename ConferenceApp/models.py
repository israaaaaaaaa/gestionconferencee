from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date
import uuid

# -------------------- Validators --------------------

title_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÿ\s]+$',
    message="The conference title must contain only letters and spaces."
)

def validate_dates(start_date, end_date):
    if start_date >= end_date:
        raise ValidationError("The start date must be before the end date.")

def generate_submission_id():
    return "SUB" + uuid.uuid4().hex[:8].upper()

def validate_keywords(value):
    words = [w.strip() for w in value.split(",") if w.strip()]
    if len(words) > 10:
        raise ValidationError("You can specify a maximum of 10 keywords.")

# -------------------- Conference --------------------
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, validators=[title_validator])
    description = models.TextField(validators=[MinLengthValidator(30)])
    location = models.CharField(max_length=255)

    THEME_CHOICES = [
        ("CS and IA", "Computer Science and IA"),
        ("SS", "Social Science"),
        ("SE", "Science and Engineering"),
    ]
    theme = models.CharField(max_length=255, choices=THEME_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        validate_dates(self.start_date, self.end_date)

    def __str__(self):
        return self.name


# -------------------- Submission --------------------
class Submission(models.Model):
    submission_id = models.CharField(primary_key=True, max_length=20, editable=False)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="submissions")
    conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE, related_name="submissions")
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    paper = models.FileField(upload_to="papers/", validators=[FileExtensionValidator(["pdf"])])

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    payed = models.BooleanField(default=False)
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.submission_id:
            self.submission_id = generate_submission_id()
        super().save(*args, **kwargs)

    def clean(self):
        # Conference must be in the future
        if self.conference and self.conference.start_date <= date.today():
            raise ValidationError("Submissions are only allowed for upcoming conferences.")

        # User can submit max 3 per day
        if self.user:
            same_day_count = Submission.objects.filter(
                user=self.user,
                submission_date=date.today()
            ).count()
            if same_day_count >= 3:
                raise ValidationError("You can only submit up to 3 submissions per day.")

    def __str__(self):
        return self.title
