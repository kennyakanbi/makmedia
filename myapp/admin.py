from django.contrib import admin
from .models import Contact, Blog, Internship, BlogImage

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "short_message", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = "Message"

# ================= Inline for extra blog images =================
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1  # shows one extra empty field

# ================= Blog Admin =================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name", "created_at")
    search_fields = ("title", "author_name")
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("title",)}  # auto-fill slug in admin
    inlines = [BlogImageInline]  # reference must be AFTER the class definition

# ================= Internship Admin =================
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
        "timestamp",
    )
    search_fields = ("fullname", "usn", "email", "college_name")
    list_filter = ("offer_status", "college_name", "timestamp")


def image_preview(self):
    if self.image:
        return mark_safe(f'<img src="{self.image.url}" width="100" />') # type: ignore
    return "-"
