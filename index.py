# Description: This script is used to organize screenshots on an Android phone based on the content of the screenshot. It uses pytesseract to extract text from the screenshot and then categorizes the screenshot based on keywords in the text. The screenshots are then moved to folders on the phone based on their category. The script uses ADB to interact with the Android phone and requires pytesseract to be installed.

import os
import pytesseract
from PIL import Image
import subprocess

# Define Categories & Keywords
CATEGORIES = {
    "AI": ["machine learning", "artificial intelligence", "neural network", "AI"],
    "Design": ["figma", "photoshop", "illustrator", "UI", "UX", "icons", "designs"],
    "Finance": ["stocks", "crypto", "investment", "finance", "money"],
    "Programming": ["JavaScript", "Python", "React", "Node.js", "programming", "code"],
    "Manga and Fun": ["Manga", "Anime", "memes", "funny", "wholesome", "cute"],
    "Other": [""]
}

# Path to screenshots folder on Android
PHONE_SCREENSHOTS_PATH = "SOURCE_PATH"


# Function to extract text from image
import os

def extract_text(image_path):
    local_path = f"./temp/{os.path.basename(image_path)}"
    os.makedirs("temp", exist_ok=True)

    # Pull image from phone
    subprocess.run(["adb", "pull", image_path, local_path], shell=True)

    # Process image
    img = Image.open(local_path)
    text = pytesseract.image_to_string(img).lower()

    # Delete temp image after processing
    os.remove(local_path)

    return text


# Function to categorize image based on keywords
def categorize_image(image_path):
    text = extract_text(image_path)
    
    for category, keywords in CATEGORIES.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Other"

# Function to move file on phone using ADB
def move_file_on_phone(source_path, category):
    destination_path = f"SOURCE_TO_LOCATION/{category}"

    
    # Create folder if it doesn't exist
    subprocess.run(["adb", "shell", f"mkdir -p '{destination_path}'"], shell=True)

    # Move file
    subprocess.run(["adb", "shell", f"mv '{source_path}' '{destination_path}/'"], shell=True)
    print(f"Moved {source_path} → {destination_path}/")

# Function to process and organize images
def organize_images():
    # Get list of screenshot files on phone
    result = subprocess.run(["adb", "shell", f"ls {PHONE_SCREENSHOTS_PATH}"], capture_output=True, text=True, shell=True)
    files = result.stdout.split("\n")

    for filename in files:
        if filename.endswith((".png", ".jpg", ".jpeg")):
            img_path = f"{PHONE_SCREENSHOTS_PATH}/{filename}"
            category = categorize_image(img_path)
            move_file_on_phone(img_path, category)

# Run the organization process
organize_images()
