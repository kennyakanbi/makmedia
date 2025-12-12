from django.core.management.base import BaseCommand
from myapp.models import BlogImage
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = "Check BlogImage entries and report missing image files."

    def handle(self, *args, **kwargs):
        total = BlogImage.objects.count()
        missing = 0

        for img in BlogImage.objects.all():
            if not img.image or not default_storage.exists(img.image.name):
                self.stdout.write(f"Missing: {img.image.name if img.image else 'No file'}")
                missing += 1

        self.stdout.write(self.style.SUCCESS(
            f"Processed {total} BlogImage entries, found {missing} missing files."
        ))
