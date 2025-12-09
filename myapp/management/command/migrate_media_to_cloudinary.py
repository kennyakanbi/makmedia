import os
from django.core.management.base import BaseCommand
from django.core.files import File
from myapp.models import Blog  # Import your models with media fields

class Command(BaseCommand):
    help = "Upload existing local media files referenced in ImageFields to Cloudinary and update model fields."

    def handle(self, *args, **options):
        count = 0
        skipped = 0
        errors = 0

        for post in Blog.objects.all():
            try:
                img_field = getattr(post, "image", None)
                if not img_field:
                    skipped += 1
                    self.stdout.write(self.style.NOTICE(f"Skipping (no image): Blog {post.pk}"))
                    continue

                # Skip if already remote
                url = getattr(img_field, "url", "")
                if url and url.startswith("http"):
                    skipped += 1
                    self.stdout.write(self.style.NOTICE(f"Already remote, skipping: Blog {post.pk} -> {url}"))
                    continue

                # Local path
                local_path = getattr(img_field, "path", None)
                if not local_path or not os.path.exists(local_path):
                    errors += 1
                    self.stdout.write(self.style.WARNING(f"Local file missing for Blog {post.pk}: {local_path}"))
                    continue

                with open(local_path, "rb") as f:
                    django_file = File(f)
                    name = os.path.basename(local_path)
                    post.image.save(name, django_file, save=True)

                count += 1
                self.stdout.write(self.style.SUCCESS(f"Uploaded Blog {post.pk} -> {post.image.url}"))

            except Exception as exc:
                errors += 1
                self.stdout.write(self.style.ERROR(f"Failed Blog {post.pk}: {exc}"))

        self.stdout.write(self.style.SUCCESS(
            f"Migration finished: {count} uploaded, {skipped} skipped, {errors} errors"
        ))
