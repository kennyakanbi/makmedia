# myapp/management/commands/migrate_media_to_cloudinary.py
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from myapp.models import Blog
# If you have a related extra image model, import it too:
# from myapp.models import ExtraImage

class Command(BaseCommand):
    help = "Upload existing local media files referenced in ImageFields to Cloudinary and update model fields."

    def handle(self, *args, **options):
        count = 0
        skipped = 0
        errors = 0

        # Migrate Blog.image
        for post in Blog.objects.all():
            try:
                img_field = getattr(post, "image", None)
                if not img_field:
                    skipped += 1
                    self.stdout.write(self.style.NOTICE(f"Skipping (no image): Blog {post.pk}"))
                    continue

                # If already a remote URL (starts with http), skip
                url = getattr(img_field, "url", "")
                if url and url.startswith("http"):
                    skipped += 1
                    self.stdout.write(self.style.NOTICE(f"Already remote, skipping: Blog {post.pk} -> {url}"))
                    continue

                # Local path to file
                local_path = getattr(img_field, "path", None)
                if not local_path or not os.path.exists(local_path):
                    errors += 1
                    self.stdout.write(self.style.WARNING(f"Local file missing for Blog {post.pk}: {local_path}"))
                    continue

                with open(local_path, "rb") as f:
                    django_file = File(f)
                    name = os.path.basename(local_path)
                    # saving the field triggers upload via DEFAULT_FILE_STORAGE
                    post.image.save(name, django_file, save=True)

                count += 1
                self.stdout.write(self.style.SUCCESS(f"Uploaded Blog {post.pk} -> {post.image.url}"))

            except Exception as exc:
                errors += 1
                self.stdout.write(self.style.ERROR(f"Failed Blog {post.pk}: {exc}"))

        # If you have a related ExtraImage model, migrate them similarly.
        # Uncomment and adapt the code below if needed:
        #
        # for extra in ExtraImage.objects.all():
        #     try:
        #         img_field = getattr(extra, "image", None)
        #         if not img_field:
        #             continue
        #         url = getattr(img_field, "url", "")
        #         if url and url.startswith("http"):
        #             continue
        #         local_path = getattr(img_field, "path", None)
        #         if not local_path or not os.path.exists(local_path):
        #             self.stdout.write(self.style.WARNING(f"Local file missing for ExtraImage {extra.pk}: {local_path}"))
        #             continue
        #         with open(local_path, "rb") as f:
        #             django_file = File(f)
        #             name = os.path.basename(local_path)
        #             extra.image.save(name, django_file, save=True)
        #         self.stdout.write(self.style.SUCCESS(f"Uploaded ExtraImage {extra.pk} -> {extra.image.url}"))
        #     except Exception as exc:
        #         self.stdout.write(self.style.ERROR(f"Failed ExtraImage {extra.pk}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Uploaded: {count}. Skipped: {skipped}. Errors: {errors}"))
