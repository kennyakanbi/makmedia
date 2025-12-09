import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.storage import default_storage

from myapp.models import Blog, BlogImage

class Command(BaseCommand):
    help = "Upload local media files referenced in ImageFields to the default storage (Cloudinary in prod)."

    def handle(self, *args, **options):
        total = 0
        skipped = 0
        errors = 0

        self.stdout.write(self.style.NOTICE("Starting media migration..."))

        def process_field(obj, field_name):
            nonlocal total, skipped, errors
            try:
                field = getattr(obj, field_name, None)
                if not field:
                    skipped += 1
                    self.stdout.write(f"SKIP: no field `{field_name}` on {obj}")
                    return

                name = getattr(field, "name", None)
                if not name:
                    skipped += 1
                    self.stdout.write(f"SKIP: empty file for {obj}.{field_name}")
                    return

                # If URL already remote (http/https), skip
                try:
                    url = field.url
                except Exception:
                    url = None

                if url and (url.startswith("http://") or url.startswith("https://")):
                    skipped += 1
                    self.stdout.write(f"SKIP: already remote -> {url}")
                    return

                # Try to use field.path if available (local filesystem)
                local_path = getattr(field, "path", None)
                if local_path and os.path.exists(local_path):
                    with open(local_path, "rb") as f:
                        field.save(os.path.basename(name), File(f), save=True)
                        total += 1
                        self.stdout.write(self.style.SUCCESS(f"UPLOADED (path): {obj} -> {field.url}"))
                        return

                # Try default_storage.open (works if media is in MEDIA_ROOT)
                if default_storage.exists(name):
                    try:
                        with default_storage.open(name, "rb") as f:
                            field.save(os.path.basename(name), File(f), save=True)
                            total += 1
                            self.stdout.write(self.style.SUCCESS(f"UPLOADED (storage.open): {obj} -> {field.url}"))
                            return
                    except Exception as ex:
                        self.stdout.write(self.style.WARNING(f"warning opening via default_storage for {name}: {ex}"))

                errors += 1
                self.stdout.write(self.style.ERROR(f"ERROR: Could not find local file for {obj}: '{name}'"))

            except Exception as exc:
                errors += 1
                self.stdout.write(self.style.ERROR(f"ERROR processing {obj}: {exc}"))

        # Process Blog.image
        self.stdout.write(self.style.NOTICE("Processing Blog.image fields..."))
        for b in Blog.objects.all():
            process_field(b, "image")

        # Process BlogImage.image (extra images)
        self.stdout.write(self.style.NOTICE("Processing BlogImage.image fields..."))
        for bi in BlogImage.objects.all():
            process_field(bi, "image")

        # Summary
        self.stdout.write(self.style.SUCCESS("Migration complete."))
        self.stdout.write(f"Total uploaded: {total}")
        self.stdout.write(f"Total skipped:  {skipped}")
        self.stdout.write(f"Total errors:   {errors}")

