# upload_media_to_cloudinary.py
import os
import django
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from myapp.models import Blog, BlogImage
from django.core.files.storage import default_storage

MEDIA_ROOT = os.path.join(os.getcwd(), "media")

def upload_field(obj, field_name):
    field = getattr(obj, field_name, None)
    if not field:
        return False, "no-field"
    name = getattr(field, "name", None)
    if not name:
        return False, "empty-name"
    # if already remote, skip
    try:
        url = field.url
    except Exception:
        url = None
    if url and (url.startswith("http://") or url.startswith("https://")):
        return False, "already-remote"

    # try local path first
    local_path = getattr(field, "path", None)
    if local_path and os.path.exists(local_path):
        with open(local_path, "rb") as f:
            field.save(os.path.basename(name), File(f), save=True)
        return True, field.url

    # else try MEDIA_ROOT + name
    candidate = os.path.join(MEDIA_ROOT, name.replace("/", os.sep))
    if os.path.exists(candidate):
        with open(candidate, "rb") as f:
            field.save(os.path.basename(name), File(f), save=True)
        return True, field.url

    # fallback: default_storage.open if exists
    try:
        if default_storage.exists(name):
            with default_storage.open(name, "rb") as f:
                field.save(os.path.basename(name), File(f), save=True)
            return True, field.url
    except Exception:
        pass

    return False, f"not-found:{name}"

def main():
    uploaded = []
    skipped = []
    errors = []

    print("Uploading Blog.image fields...")
    for b in Blog.objects.all():
        ok, info = upload_field(b, "image")
        if ok:
            uploaded.append((b.pk, info))
            print("UPLOADED Blog", b.pk, info)
        else:
            skipped.append((b.pk, info))
    print("Uploading BlogImage.image fields...")
    for bi in BlogImage.objects.all():
        ok, info = upload_field(bi, "image")
        if ok:
            uploaded.append((f"BI:{bi.pk}", info))
            print("UPLOADED BlogImage", bi.pk, info)
        else:
            errors.append((bi.pk, info))
            print("SKIP/ERR BlogImage", bi.pk, info)

    print("Done. Uploaded:", len(uploaded), "Errors:", len(errors))

if __name__ == "__main__":
    main()
