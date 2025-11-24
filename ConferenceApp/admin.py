from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header="Conference Management admin 25/26"
admin.site.site_title="Conference dashboard"
admin.site.index_title="Conference management"
#admin.site.register(Conference)
class SubmissionInline(admin.StackedInline):
    model=submission
    extra=1
    readonly_fields =("submission_id",)
     # Champs à afficher
    fields = ('title', 'status', 'payed', 'user')

@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display =("name","theme","location","start_date","end_date","duration")
    ordering= ("start_date",)
    list_filter =("theme","location","end_date")
    search_fields =("name",)
    fieldsets = (
            ("Information General",{
                "fields": ("conference_id","name", "theme","description")
            }),

            ("Logistics" , {
                "fields": ("location","start_date","end_date")
            }),
    )
    readonly_fields= ("conference_id",)
    date_hierarchy = "start_date"
    inlines = [SubmissionInline]
    def duration(self,objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date-objet.start_date).days
        return "RAS"
    duration.short_description="Duration (days)"
@admin.register(submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'title', 'user', 'conference', 'status', 'payed', 'submission_date')
    list_filter = ('status', 'payed', 'conference', 'submission_date')
    search_fields = ('submission_id', 'title', 'author__first_name', 'author__last_name', 'conference__name')
    readonly_fields = ('submission_id', 'submission_date')
    date_hierarchy = 'submission_date'
    autocomplete_fields = ['user', 'conference']
    actions = ['mark_as_paid', 'accept_submissions']
    def mark_as_paid(self, request, queryset):
        """Mark selected submissions as paid."""
        queryset.update(payed=True)
    mark_as_paid.short_description = "Mark selected submissions as paid"

    def accept_submissions(self, request, queryset):
        """Accept selected submissions."""
        queryset.update(status='accepted')
    accept_submissions.short_description = "Accept selected submissions"
    def is_valid_registration(self, obj):
        """Indique si l'inscription est valide"""
        return obj.is_registration_valid
    is_valid_registration.short_description = "Inscription valide"
    is_valid_registration.boolean = True  # Affiche une icône vrai/faux