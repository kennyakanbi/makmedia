# fix_images.py
# Safe script to ensure DB-referenced blog image filenames exist under static/media/blog_images/
# Run: python fix_images.py

import os
import shutil
import django

# --- configure Django environment (change if your settings module name differs) ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
# -------------------------------------------------------------------------------

from django.conf import settings
from myapp.models import Blog

BASE_DIR = settings.BASE_DIR
static_dir = os.path.join(BASE_DIR, "static", "media", "blog_images")
media_dir = os.path.join(BASE_DIR, "media", "blog_images")

os.makedirs(static_dir, exist_ok=True)

def try_copy(src, dst):
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print("  ERROR copying", src, "->", dst, ":", e)
        return False

copied = []
missing = []

for blog in Blog.objects.all():
    names = []
    # featured image (if present)
    img_obj = getattr(blog, "image", None)
    if img_obj and getattr(img_obj, "name", None):
        names.append(img_obj.name)
    # extra images
    try:
        names += [ei.image.name for ei in blog.extra_images.all() if getattr(ei.image, "name", None)]
    except Exception:
        pass

    for full in [n for n in names if n]:
        fname = os.path.basename(full)               # e.g. "web_dev_2_yFW062L.png"
        target = os.path.join(static_dir, fname)
        if os.path.exists(target):
            continue  # already present

        print("Need file:", fname, "for post:", blog.slug)

        # 1) try find candidate in static_dir that shares a base before first underscore
        base = fname.split("_")[0]
        candidates = [f for f in os.listdir(static_dir) if f.split(".")[0].startswith(base)]
        if candidates:
            src = os.path.join(static_dir, candidates[0])
            if try_copy(src, target):
                copied.append((candidates[0], fname, blog.slug))
                print("  Copied candidate from static:", candidates[0], "->", fname)
                continue

        # 2) try exact file in media_dir
        media_exact = os.path.join(media_dir, fname)
        if os.path.exists(media_exact):
            if try_copy(media_exact, target):
                copied.append((os.path.basename(media_exact), fname, blog.slug))
                print("  Copied exact from media:", os.path.basename(media_exact), "->", fname)
                continue

        # 3) try base match in media_dir
        if os.path.exists(media_dir):
            c2 = [f for f in os.listdir(media_dir) if f.split(".")[0].startswith(base)]
            if c2:
                src = os.path.join(media_dir, c2[0])
                if try_copy(src, target):
                    copied.append((c2[0], fname, blog.slug))
                    print("  Copied candidate from media:", c2[0], "->", fname)
                    continue

        # nothing found
        missing.append((fname, blog.slug))
        print("  MISSING: could not find any file to satisfy", fname)

# Summary
print("\nSummary:")
print("Copied files:", len(copied))
for s,t,slug in copied[:200]:
    print("  ", s, "->", t, "for", slug)
print("Missing files:", len(missing))
for name,slug in missing[:200]:
    print("  ", name, "for", slug)
