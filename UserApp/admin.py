from django.contrib import admin
from .models import User, OrganizingCommittee

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "email", "first_name", "last_name", "role", "affiliation", "nationality")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("role", "nationality")
    readonly_fields = ("user_id",)

@admin.register(OrganizingCommittee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ("user", "conference", "committee_role", "date_join")
    list_filter = ("committee_role", "conference")
