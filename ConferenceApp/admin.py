from django.contrib import admin
from .models import Conference, Submission

# ---------- Custom Admin Header ----------
admin.site.site_header = "Conference Management Dashboard"
admin.site.site_title = "Conference Admin"
admin.site.index_title = "Welcome to the Conference Administration Panel"


# ---------- Inline Configurations ----------

# ✅ Stacked Inline version (vertical display)
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 0
    fields = ("submission_id", "title", "abstract", "status", "payed", "user", "submission_date")
    readonly_fields = ("submission_id", "submission_date")  # these cannot be edited
    can_delete = False


# ✅ Tabular Inline version (table display)
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 0
    fields = ("title", "status", "user", "payed")


# ---------- Conference Admin ----------
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # columns shown in the admin list view
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")

    # filters on the right side
    list_filter = ("theme", "location", "start_date")

    # search bar fields
    search_fields = ("name", "description", "location")

    # field organization in edit form
    fieldsets = (
        ("General Information", {"fields": ("name", "theme", "description")}),
        ("Logistics", {"fields": ("location", "start_date", "end_date")}),
    )

    ordering = ("start_date",)
    date_hierarchy = "start_date"

    # Inline display of related submissions
    inlines = [SubmissionStackedInline]  # Try TabularInline if you prefer table style

    def duration(self, obj):
        """Calculate duration between start and end dates."""
        return (obj.end_date - obj.start_date).days
    duration.short_description = "Duration (days)"


# ---------- Submission Admin ----------
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # columns shown in the admin list view
    list_display = ("title", "status", "user", "conference", "short_abstract", "submission_date", "payed")

    # make 'status' and 'payed' editable directly in list view
    list_editable = ("status", "payed")

    # filters on the right
    list_filter = ("status", "payed", "conference", "submission_date")

    # enable search bar
    search_fields = ("title", "keywords", "user__username")

    # organize fields in edit form
    fieldsets = (
        ("General Info", {"fields": ("submission_id", "title", "abstract", "keywords")}),
        ("File & Conference", {"fields": ("paper", "conference")}),
        ("Tracking", {"fields": ("status", "payed", "submission_date", "user")}),
    )

    readonly_fields = ("submission_id", "submission_date")

    # ---------- Custom actions ----------
    @admin.action(description="Mark selected submissions as Paid")
    def mark_as_payed(self, request, queryset):
        queryset.update(payed=True)

    @admin.action(description="Accept selected submissions")
    def accept_submissions(self, request, queryset):
        queryset.update(status="accepted")

    actions = [mark_as_payed, accept_submissions]

    # helper for short abstract display
    def short_abstract(self, obj):
        return (obj.abstract[:50] + "...") if len(obj.abstract) > 50 else obj.abstract
    short_abstract.short_description = "Abstract (preview)"
