import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Copy committed media files from repo (project/media) into MEDIA_ROOT (e.g. /app/media)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing files in MEDIA_ROOT.",
        )
        parser.add_argument(
            "--src",
            type=str,
            default=None,
            help="Optional source folder to copy from (defaults to project/media).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        src_override = options["src"]

        repo_media = Path(src_override) if src_override else (Path(settings.BASE_DIR) / "media")
        dest = Path(settings.MEDIA_ROOT)

        self.stdout.write(f"Source: {repo_media}")
        self.stdout.write(f"Destination (MEDIA_ROOT): {dest}")

        if not repo_media.exists():
            self.stderr.write("Source folder does not exist. Nothing to copy.")
            return

        files_copied = 0
        files_skipped = 0

        for root, dirs, files in os.walk(repo_media):
            rel_root = Path(root).relative_to(repo_media)
            target_root = dest.joinpath(rel_root)
            target_root.mkdir(parents=True, exist_ok=True)

            for f in files:
                src_file = Path(root) / f
                dest_file = target_root / f

                if dest_file.exists():
                    if force:
                        shutil.copy2(src_file, dest_file)
                        files_copied += 1
                        self.stdout.write(f"Overwritten: {dest_file}")
                    else:
                        files_skipped += 1
                        self.stdout.write(f"Skipped (exists): {dest_file}")
                else:
                    shutil.copy2(src_file, dest_file)
                    files_copied += 1
                    self.stdout.write(f"Copied: {dest_file}")

        self.stdout.write(self.style.SUCCESS(f"Done. copied={files_copied} skipped={files_skipped}"))
