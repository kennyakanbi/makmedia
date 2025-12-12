import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from myapp.models import BlogImage
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = "Check BlogImage files and migrate/re-upload missing images"

    def handle(self, *args, **kwargs):
        processed = 0
        missing = 0

        for img in BlogImage.objects.all():
            processed += 1
            if not img.image or not default_storage.exists(img.image.name):
                missing += 1
                self.stdout.write(
                    self.style.WARNING(f"Missing file: {img.image.name if img.image else 'None'} (ID: {img.pk})")
                )
                # Optionally, you could re-upload from a backup folder like this:
                # backup_path = os.path.join(settings.BASE_DIR, 'backup_blog_images', os.path.basename(img.image.name))
                # if os.path.exists(backup_path):
                #     with open(backup_path, 'rb') as f:
                #         img.image.save(os.path.basename(backup_path), File(f))
                #         img.save()
                #         self.stdout.write(self.style.SUCCESS(f"Re-uploaded: {img.image.name}"))

        self.stdout.write(self.style.SUCCESS(
            f"Processed {processed} BlogImage entries. Missing files: {missing}"
        ))
