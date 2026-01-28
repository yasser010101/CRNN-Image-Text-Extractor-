import os
import ssl
import cv2
import numpy as np
import easyocr
import re

# 1. SSL Bypass for downloading models (if needed)
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def refine_results(text_list):
    """
    Applies 'Fine-Tuning' logic using common patterns found
    in your specific images.
    """
    raw_text = "\n".join(text_list)

    # Dictionary of common monitor-reading errors
    #Add mistaking word that may come up after running the program
    corrections = {

        "exxamp1e": "example",
        "NName": "Name",
        "Wlindows": "Windows",
        "Verston": "Version",
        "14 Dro": "11 Pro",
        "Intel(R)": "Intel(R)",
        "3.1OGHz": "3.10GHz",
        "Accive": "Active"

    }

    for error, fixed in corrections.items():
        raw_text = raw_text.replace(error, fixed)

    # Advanced: Fixes IP addresses where dots are read as spaces/commas
    raw_text = re.sub(r'(\d{1,3})[\s,]+(\d{1,3})', r'\1.\2', raw_text)

    return raw_text


def run_advanced_ocr(image_path):
    # Initialize EasyOCR (CPU mode)
    #No GPU in PC -> False
    #If there a GPU in PC -> True
    reader = easyocr.Reader(['en'], gpu=False)

    # 2. IMAGE PRE-PROCESSING (Optimized for Green-on-Black screens)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not find image at {image_path}")
        return

    # Upscale 2x for better character definition
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Use only the Green channel (most detail on terminal screens)
    b, g, r = cv2.split(img)

    # Thresholding to make text pure white and background pure black
    _, thresh = cv2.threshold(g, 100, 255, cv2.THRESH_BINARY)

    print("Reading image and applying corrections...")

    # 3. RUN OCR
    results = reader.readtext(thresh, detail=0)

    # 4. POST-PROCESS
    final_output = refine_results(results)

    print("\n" + "=" * 30)
    print("      POLISHED RESULTS")
    print("=" * 30)
    print(final_output)


# Update this path to your desktop
file_path = r"your/image/path"

if __name__ == "__main__":
    run_advanced_ocr(file_path)