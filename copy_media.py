
import shutil
import os

# ------------------------------
# Paths
# ------------------------------

# Local media folder
local_media = os.path.join(os.getcwd(), "project", "media")

# Railway volume folder
railway_media = "/app/media"

# ------------------------------
# Copy function
# ------------------------------
def copy_media(src, dst):
    if not os.path.exists(src):
        print(f"❌ Source folder does not exist: {src}")
        return
    os.makedirs(dst, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"✅ Media files copied from {src} to {dst}")

# ------------------------------
# Execute
# ------------------------------
copy_media(local_media, railway_media)
