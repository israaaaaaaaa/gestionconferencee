from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid

# -------------------- Custom Functions --------------------

def generate_userid():
    """Generate a user ID in format USERXXXX (8 characters)."""
    return "USER" + uuid.uuid4().hex[:4].upper()

def verify_email(value):
    """Ensure the email belongs to a valid university domain."""
    allowed_domains = ["esprit.tn", "sesame.com", "tek.tn", "central.com"]
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError("Email must belong to an academic domain (e.g., @esprit.tn).")

name_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÿ\s-]+$',
    message="This field must contain only letters, spaces or hyphens."
)

# -------------------- User --------------------
class User(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    email = models.EmailField(validators=[verify_email])
    affiliation = models.CharField(max_length=250)
    nationality = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])

    ROLE_CHOICES = [
        ("participant", "Participant"),
        ("committee", "Organizing Committee Member"),
    ]
    role = models.CharField(max_length=250, choices=ROLE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            new_id = generate_userid()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_userid()
            self.user_id = new_id
        super().save(*args, **kwargs)


# -------------------- Organizing Committee --------------------
class OrganizingCommittee(models.Model):
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="committees")
    conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE, related_name="committees")

    ROLE_CHOICES = [
        ("chair", "Chair"),
        ("co-chair", "Co-chair"),
        ("member", "Member"),
    ]
    committee_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    date_join = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
