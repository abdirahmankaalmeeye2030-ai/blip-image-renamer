import glob
import os
import re
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

image_dir = r"D:\demo_photos"
image_exts = ["jpg", "jpeg", "png"]

# Collect all images FIRST, so renaming doesn't confuse the loop
all_images = []
for ext in image_exts:
    all_images += glob.glob(os.path.join(image_dir, f"*.{ext}"))

with open("captions.txt", "w", encoding="utf-8") as f:
    for img_path in all_images:
        try:
            # 'with' closes the image, so Windows lets us rename it
            with Image.open(img_path) as img:
                raw_image = img.convert("RGB")

            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)

            caption = caption.replace("araffe ", "").replace("arafed ", "")

            # Make a safe filename: remove bad characters, spaces -> _
            safe = re.sub(r'[\\/:*?"<>|]', "", caption).strip().replace(" ", "_")
            ext_part = os.path.splitext(img_path)[1].lower()

            # If the name already exists, add _1, _2 ...
            new_path = os.path.join(image_dir, safe + ext_part)
            counter = 1

            if os.path.abspath(new_path) == os.path.abspath(img_path):
                print(f"{os.path.basename(img_path)} already named, skipping")
                continue

            while os.path.exists(new_path):
                new_path = os.path.join(image_dir, f"{safe}_{counter}{ext_part}")
                counter += 1

            old_name = os.path.basename(img_path)
            os.rename(img_path, new_path)
            new_name = os.path.basename(new_path)

            f.write(f"{old_name} -> {new_name}\n")
            print(f"{old_name} -> {new_name}")
        except Exception as e:
            print(f"Error with {img_path}: {e}")