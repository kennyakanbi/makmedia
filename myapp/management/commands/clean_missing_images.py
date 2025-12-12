import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import BlogImage

class Command(BaseCommand):
    help = "Clear BlogImage entries whose files are missing in MEDIA_ROOT"

    def handle(self, *args, **options):
        total = 0
        removed = 0

        for bi in BlogImage.objects.all():
            total += 1
            if not bi.image:
                continue  # skip empty fields

            local_path = os.path.join(settings.MEDIA_ROOT, bi.image.name)
            if not os.path.exists(local_path):
                self.stdout.write(f"File missing for BlogImage {bi.pk}, clearing field...")
                bi.image = ''
                bi.save(update_fields=['image'])
                removed += 1

        self.stdout.write(self.style.SUCCESS(
            f"Processed {total} BlogImage entries, cleared {removed} missing files."
        ))
