import cv2
import pytesseract
import pandas as pd

def extract_text_from_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image (optional)
    # You can apply various image preprocessing techniques here
    # For example, resizing, denoising, thresholding, etc.

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    # Split the text into lines
    lines = text.split('\n')

    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    return lines

# Provide the path to your image containing the ticket
image_path = 'tickets/ticket1.jpg'

# Extract text from the image
#result = extract_text_from_image(image_path)

df_test = pd.DataFrame()
print(df_test)

# Print the extracted lines
#for line in result:
#    print(line)
