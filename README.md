# 📸 BLIP Image Renamer

An AI tool that automatically captions images and renames them based on what they show, using Salesforce's BLIP model from Hugging Face.

**Before:** `IMG_4521.png`
**After:** `a_glass_of_iced_coffee_on_a_table.png`

## ✨ Features
- Captions every image in a folder (jpg, jpeg, png)
- Renames each file from its caption
- Removes characters Windows doesn't allow in filenames
- Avoids overwriting files that get the same caption (adds `_1`, `_2`)
- Logs old and new names to `captions.txt`

## 🛠️ Tech Stack
Python · Hugging Face Transformers · BLIP (`blip-image-captioning-large`) · PyTorch · Pillow

## 🚀 How to Run
```bash
python -m venv my_env
my_env\Scripts\activate
pip install -r requirements.txt
```
Set `image_dir` in `caption_folder.py` to your images folder, then run:
```bash
python caption_folder.py
```
> ⚠️ The script renames files, so test it on copies of your images first.

## 💡 What I Learned
- How image-to-text models work: convert the image, process it, generate a caption, and decode it.
- The base model gives short captions, while the large model gives more detail.
- BLIP describes photos well but can't read text in posters. OCR (reading text from images) is the next upgrade.

## 🎓 Context
Built while taking IBM's *Building Generative AI-Powered Applications with Python* course.