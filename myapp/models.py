import uuid
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.templatetags.static import static
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_delete
from cloudinary.uploader import destroy

class Blog(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    author_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    image = CloudinaryField(
        "image",
        folder="blog_images",
        blank=True,
        null=True
    )

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
        if self.image:
            return self.image.url
        return static("assets/img/default.jpg")


class BlogImage(models.Model):
    blog = models.ForeignKey(
        Blog,
        related_name="extra_images",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=150, blank=True)

    image = CloudinaryField(
        "image",
        folder="blog_images",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Blog Extra Image"
        verbose_name_plural = "Blog Extra Images"

    def __str__(self):
        return f"Image for {self.blog.title}"

    @property
    def url(self):
        if self.image:
            return self.image.url
        return static("assets/img/default.jpg")


@receiver(post_delete, sender=Blog)
def delete_blog_image(sender, instance, **kwargs):
    if instance.image:
        destroy(instance.image.public_id)


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
