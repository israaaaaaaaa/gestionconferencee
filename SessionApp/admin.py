from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "conference", "session_day", "start_time", "end_time", "room")
    list_filter = ("conference", "session_day")
    search_fields = ("title", "topic", "room")
