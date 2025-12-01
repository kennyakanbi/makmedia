from django.db import models
from django.utils.text import slugify


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
    description = models.TextField()
    content = models.TextField()
    author_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

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

# New model for multiple images
class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name="extra_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog_images/")
    caption = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.blog.title}"


class Internship(models.Model):
    fullname = models.CharField(max_length=60)
    usn = models.CharField(max_length=60, unique=True)
    email = models.EmailField(max_length=100)
    college_name = models.CharField(max_length=100)
    offer_status = models.CharField(max_length=60, choices=[
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    proj_report = models.TextField(blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ["-timeStamp"]
        verbose_name = "Internship"
        verbose_name_plural = "Internships"

    def __str__(self):
        return f"{self.fullname} ({self.usn})"
