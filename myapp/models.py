import uuid
from django.db import models
from django.utils.text import slugify
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver


def upload_to_uuid(instance, filename):
    ext = filename.split(".")[-1] if "." in filename else ""
    return f"blog_images/{uuid.uuid4().hex}.{ext}"


def upload_to_original(instance, filename):
    return upload_to_uuid(instance, filename)


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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or uuid.uuid4().hex[:8]
            slug = base
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image and default_storage.exists(self.image.name):
            return self.image.url
        return static("assets/img/default.jpg")


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name="extra_images", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Untitled", blank=True)
    caption = models.CharField(max_length=150, blank=True, default="")
    image = models.ImageField(upload_to=upload_to_uuid, blank=True, null=True)

    class Meta:
        verbose_name = "Blog Extra Image"
        verbose_name_plural = "Blog Extra Images"

    def __str__(self):
        return f"Image for {self.blog.title}"

    @property
    def url(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        return "/static/assets/img/default.jpg"


@receiver(pre_save, sender=Blog)
def auto_delete_old_blog_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Blog.objects.get(pk=instance.pk).image
        if old and old != instance.image:
            if default_storage.exists(old.name):
                default_storage.delete(old.name)
    except Blog.DoesNotExist:
        pass


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Internship(models.Model):
    fullname = models.CharField(max_length=60)
    usn = models.CharField(max_length=60, unique=True)
    email = models.EmailField()
    college_name = models.CharField(max_length=100)
    offer_status = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    proj_report = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname
