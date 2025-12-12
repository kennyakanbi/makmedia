import os
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver

# =========================
# UTILITY FUNCTION FOR IMAGE UPLOAD
# =========================
def upload_to_original(instance, filename):
    """
    Preserve original filename without adding automatic timestamp.
    """
    return f"blog_images/{filename}"


# =========================
# CONTACT MODEL
# =========================
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.name} - {self.email}"


# =========================
# BLOG MODEL
# =========================
class Blog(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    content = models.TextField()
    author_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            try:
                if default_storage.exists(self.image.name):
                    return default_storage.url(self.image.name)
            except Exception:
                pass
            return static(f"media/{self.image.name}")
        return static("assets/img/default.jpg")


# =========================
# BLOG IMAGE MODEL
# =========================
class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name="extra_images", on_delete=models.CASCADE)
    caption = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=200, default="Untitled")
    image = models.ImageField(upload_to=upload_to_original, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.blog.title}"

    @property
    def url(self):
        if self.image and self.image.name:
            try:
                if default_storage.exists(self.image.name):
                    return default_storage.url(self.image.name)
            except Exception:
                pass
            return static(f"media/{self.image.name}")
        return static("assets/img/default.jpg")


# Automatically delete old files when replacing
@receiver(pre_save, sender=BlogImage)
def auto_delete_old_file(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_file = BlogImage.objects.get(pk=instance.pk).image
    except BlogImage.DoesNotExist:
        return
    new_file = instance.image
    if old_file and old_file != new_file and default_storage.exists(old_file.name):
        default_storage.delete(old_file.name)


# =========================
# INTERNSHIP MODEL
# =========================
class Internship(models.Model):
    fullname = models.CharField(max_length=60)
    usn = models.CharField(max_length=60, unique=True)
    email = models.EmailField(max_length=100)
    college_name = models.CharField(max_length=100)
    offer_status = models.CharField(
        max_length=60,
        choices=[("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")],
    )
    start_date = models.DateField()
    end_date = models.DateField()
    proj_report = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Internship"
        verbose_name_plural = "Internships"

    def __str__(self):
        return f"{self.fullname} ({self.usn})"
