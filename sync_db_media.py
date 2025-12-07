# sync_db_media.py
import os, shutil
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # <- change if your settings module differs
django.setup()

from myapp.models import Blog

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(BASE_DIR, "static", "media", "blog_images")
media_dir = os.path.join(BASE_DIR, "media", "blog_images")

os.makedirs(static_dir, exist_ok=True)

def list_static():
    try:
        return set(os.listdir(static_dir))
    except FileNotFoundError:
        return set()

static_files = list_static()
copied = []
missing = []

for b in Blog.objects.all():
    names = []
    if getattr(b, "image", None):
        names.append(os.path.basename(b.image.name))
    for ei in getattr(b, "extra_images").all():
        names.append(os.path.basename(ei.image.name))

    for fname in [n for n in names if n]:
        if fname in static_files:
            continue
        # try to find a candidate match in static_files
        base = fname.split("_")[0]
        candidates = [f for f in static_files if f.split(".")[0].startswith(base)]
        if candidates:
            src = os.path.join(static_dir, candidates[0])
            dst = os.path.join(static_dir, fname)
            try:
                shutil.copy2(src, dst)
                copied.append((candidates[0], fname, b.slug))
                static_files.add(fname)
                print(f"Copied candidate: {candidates[0]} -> {fname} for post {b.slug}")
                continue
            except Exception as e:
                print("Error copying", src, "->", dst, e)
        # try media folder exact
        media_exact = os.path.join(media_dir, fname)
        if os.path.exists(media_exact):
            dst = os.path.join(static_dir, fname)
            try:
                shutil.copy2(media_exact, dst)
                copied.append((os.path.basename(media_exact), fname, b.slug))
                static_files.add(fname)
                print(f"Copied from media: {os.path.basename(media_exact)} -> {fname} for post {b.slug}")
                continue
            except Exception as e:
                print("Error copying from media", media_exact, e)
        # if nothing
        missing.append((fname, b.slug))
        print(f"MISSING: {fname} for post {b.slug}")

print("\nSUMMARY:")
print("Copied:", len(copied))
for s,t,slug in copied:
    print(" ", s, "->", t, "for", slug)
print("Missing:", len(missing))
for n,slug in missing:
    print(" ", n, "for", slug)
