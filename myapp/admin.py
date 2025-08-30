from django.contrib import admin
from .models import Contact, Blog, Internship


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phonenumber")
    search_fields = ("name", "email", "phonenumber")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name", "created_at")  # fixed
    search_fields = ("title", "author_name")  # fixed
    list_filter = ("created_at",)  # fixed


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
    search_fields = ("fullname", "usn", "email", "college_name")  # more useful
    list_filter = ("offer_status", "college_name", "timeStamp")  # cleaned up
