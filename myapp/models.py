import os
import uuid
from pathlib import Path
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Helper to store uploaded images under blog_images/ with a UUID filename
def upload_to_uuid(instance, filename):
    ext = filename.split(".")[-1] if "." in filename else ""
    new_filename = f"{uuid.uuid4().hex}{('.' + ext) if ext else ''}"
    return f"blog_images/{new_filename}"

# compatibility helper required by older migrations
def upload_to_original(instance, filename):
    """
    Kept for backwards-compatibility with older migrations that reference
    `myapp.models.upload_to_original`. Delegates to the UUID-based uploader so
    we avoid collisions while remaining importable for migrations.
    """
    ext = filename.split(".")[-1] if "." in filename else ""
    new_filename = f"{uuid.uuid4().hex}{('.' + ext) if ext else ''}"
    return f"blog_images/{new_filename}"


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
 

class Blog(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    author_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_to_uuid, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        base = slugify(self.title) or uuid.uuid4().hex[:8]
        slug_candidate = base
        counter = 1
        while Blog.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
            slug_candidate = f"{base}-{counter}"
            counter += 1
        return slug_candidate

    def save(self, *args, **kwargs):
        # Ensure unique slug on first save (or if slug cleared)
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


@property
def image_url(self):
    """
    Return a usable URL for the featured image.
    Works with MEDIA in dev/production. Falls back to a placeholder.
    """
    if self.image:
        try:
            return self.image.url  # This uses MEDIA_URL
        except Exception:
            pass
    return "/static/assets/img/default.jpg"



class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name="extra_images", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Untitled", blank=True)
    caption = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to=upload_to_uuid, blank=True, null=True)

    class Meta:
        verbose_name = "Blog Extra Image"
        verbose_name_plural = "Blog Extra Images"

    def __str__(self):
        return f"Image for {self.blog.title}"

@property
def url(self):
    """
    Return a usable URL for extra images.
    """
    if self.image:
        try:
            return self.image.url
        except Exception:
            pass
    return "/static/assets/img/default.jpg"


# Delete old files when replacing an image (Blog)
@receiver(pre_save, sender=Blog)
def auto_delete_old_blog_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Blog.objects.get(pk=instance.pk).image
    except Blog.DoesNotExist:
        return
    new = instance.image
    if old and old != new:
        try:
            if default_storage.exists(old.name):
                default_storage.delete(old.name)
        except Exception:
            # If storage deletion fails, ignore (we don't want crashes on save)
            pass


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

