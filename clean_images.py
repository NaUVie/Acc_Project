import os

base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'frontend', 'src')
seed_file = os.path.join(base_dir, 'backend', 'app', 'seed.py')
img_dir = os.path.join(base_dir, 'frontend', 'public', 'images')

code_text = ""
if os.path.exists(seed_file):
    with open(seed_file, 'r', encoding='utf-8', errors='ignore') as f:
        code_text += f.read() + "\n"

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith(('.vue', '.js', '.css', '.json')):
            full_p = os.path.join(root, f)
            with open(full_p, 'r', encoding='utf-8', errors='ignore') as fc:
                code_text += fc.read() + "\n"

images = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
deleted_count = 0
freed_bytes = 0

for img in images:
    if img not in code_text:
        img_path = os.path.join(img_dir, img)
        freed_bytes += os.path.getsize(img_path)
        os.remove(img_path)
        deleted_count += 1

print(f"Cleanup finished! Deleted {deleted_count} unused images.")
print(f"Freed space: {round(freed_bytes / (1024 * 1024), 2)} MB")
