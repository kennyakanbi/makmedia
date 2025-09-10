from django.contrib import admin
from .models import Contact, Blog, Internship

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "message", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name", "created_at")
    search_fields = ("title", "author_name")
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("title",)}  # auto-fill slug in admin


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = (
        "fullname",
        "usn",
        "email",
        "college_name",
        "offer_status",
        "start_date",
        "end_date",
        "timeStamp",
    )
    search_fields = ("fullname", "usn", "email", "college_name")
    list_filter = ("offer_status", "college_name", "timeStamp")
