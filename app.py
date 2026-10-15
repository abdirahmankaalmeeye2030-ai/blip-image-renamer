import os
import re
import shutil
import tempfile
import zipfile
import gradio as gr
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def caption_and_rename(files):
    if not files:
        return [], None
    out_dir = tempfile.mkdtemp()
    rows = []
    for file_path in files:
        with Image.open(file_path) as img:
            raw_image = img.convert("RGB")
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(out[0], skip_special_tokens=True)
        caption = caption.replace("araffe ", "").replace("arafed ", "")

        safe = re.sub(r'[\\/:*?"<>|]', "", caption).strip().replace(" ", "_")
        ext = os.path.splitext(file_path)[1].lower()
        new_path = os.path.join(out_dir, safe + ext)
        counter = 1
        while os.path.exists(new_path):
            new_path = os.path.join(out_dir, f"{safe}_{counter}{ext}")
            counter += 1
        shutil.copy(file_path, new_path)
        rows.append([os.path.basename(file_path), caption, os.path.basename(new_path)])

    zip_path = os.path.join(tempfile.mkdtemp(), "renamed_images.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for name in os.listdir(out_dir):
            z.write(os.path.join(out_dir, name), name)
    return rows, zip_path

demo = gr.Interface(
    fn=caption_and_rename,
    inputs=gr.File(file_count="multiple", file_types=["image"], label="Upload images"),
    outputs=[
        gr.Dataframe(headers=["Original name", "Caption", "New name"], label="Results"),
        gr.File(label="Download renamed images (ZIP)"),
    ],
    title="📸 BLIP Image Renamer",
    description="Upload images, get AI captions, and download them renamed by what they show.",
)

demo.launch()