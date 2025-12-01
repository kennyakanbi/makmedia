import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")

def optimize_image(path):
    try:
        img = Image.open(path)
        img.save(path, optimize=True, quality=70)
        print(f"Optimized: {path}")
    except Exception as e:
        print(f"Error optimizing {path}: {e}")

def walk_static():
    for root, dirs, files in os.walk(STATIC_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                optimize_image(os.path.join(root, file))

if __name__ == "__main__":
    print("Optimizing static images...")
    walk_static()
    print("Done.")
