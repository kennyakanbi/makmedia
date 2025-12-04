import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

RAILWAY_PROJECT_ID = os.environ.get("RAILWAY_PROJECT_ID")
RAILWAY_VOLUME_ID = os.environ.get("RAILWAY_VOLUME_ID")
RAILWAY_API_TOKEN = os.environ.get("RAILWAY_API_TOKEN")  # from Railway account

LOCAL_MEDIA_DIR = settings.MEDIA_ROOT

class Command(BaseCommand):
    help = "Sync local media folder to Railway volume"

    def handle(self, *args, **kwargs):
        if not all([RAILWAY_PROJECT_ID, RAILWAY_VOLUME_ID, RAILWAY_API_TOKEN]):
            self.stderr.write("Missing Railway environment variables!")
            return

        # Loop through media folder
        for root, dirs, files in os.walk(LOCAL_MEDIA_DIR):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, LOCAL_MEDIA_DIR)

                self.stdout.write(f"Uploading {relative_path}...")

                url = f"https://backboard.railway.app/api/v1/projects/{RAILWAY_PROJECT_ID}/volumes/{RAILWAY_VOLUME_ID}/files/{relative_path}"
                
                with open(local_path, "rb") as f:
                    response = requests.put(
                        url,
                        headers={"Authorization": f"Bearer {RAILWAY_API_TOKEN}"},
                        files={"file": f}
                    )

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"Uploaded {relative_path}"))
                else:
                    self.stderr.write(self.style.ERROR(f"Failed {relative_path}: {response.text}"))
        
        self.stdout.write(self.style.SUCCESS("Sync complete!"))
