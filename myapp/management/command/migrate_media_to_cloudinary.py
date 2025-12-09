# myapp/management/commands/migrate_media_to_cloudinary.py

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from myapp.models import Blog, ExtraImage  # Add all models with image fields here

class Command(BaseCommand):
    help = "Upload existing local media files to Cloudinary and update model fields."

    def handle(self, *args, **options):
        total_uploaded = 0
        total_skipped = 0
        total_errors = 0

        # Helper function to process a queryset
        def migrate_queryset(queryset, field_name="image"):
            nonlocal total_uploaded, total_skipped, total_errors
            for obj in queryset:
                try:
                    img_field = getattr(obj, field_name, None)

                    if not img_field:
                        total_skipped += 1
                        self.stdout.write(self.style.NOTICE(f"Skipping (no image): {obj}"))
                        continue

                    # Skip if already a remote URL
                    if img_field.url and img_field.url.startswith("http"):
                        total_skipped += 1
                        self.stdout.write(self.style.NOTICE(f"Already remote, skipping: {obj} -> {img_field.url}"))
                        continue

                    local_path = getattr(img_field, "path", None)
                    if not local_path or not os.path.exists(local_path):
                        total_errors += 1
                        self.stdout.write(self.style.WARNING(f"Local file missing for {obj}: {local_path}"))
                        continue

                    # Upload to Cloudinary via default storage
                    with open(local_path, "rb") as f:
                        django_file = File(f)
                        name = os.path.basename(local_path)
                        img_field.save(name, django_file, save=True)

                    total_uploaded += 1
                    self.stdout.write(self.style.SUCCESS(f"Uploaded {obj} -> {img_field.url}"))

                except Exception as e:
                    total_errors += 1
                    self.stdout.write(self.style.ERROR(f"Failed {obj}: {e}"))

        # Migrate Blogs
        migrate_queryset(Blog.objects.all())

        # Migrate ExtraImages
        migrate_queryset(ExtraImage.objects.all())

        # Final summary
        self.stdout.write(self.style.SUCCESS(
            f"Migration complete. Uploaded: {total_uploaded}, Skipped: {total_skipped}, Errors: {total_errors}"
        ))
