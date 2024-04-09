import cv2
import pytesseract
import pandas as pd
import imutils
from imutils.perspective import four_point_transform


def apply_preprocessing_image(orig):
    image2 = orig.copy()
    image2 = imutils.resize(image2, width=500)
    ratio = orig.shape[1] / float(image2.shape[1])

    # convert the image to grayscale, blur it slightly, and then apply
    # edge detection
    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)
   
    
    # find contours in the edge map and sort them by size in descending
# order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    print(cnts)

    # initialize a contour that corresponds to the receipt outline
    receiptCnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we can
        # assume we have found the outline of the receipt
        if len(approx) == 4:
            print("Contour found")
            receiptCnt = approx
            break
    # if the receipt contour is empty then our script could not find the
    # outline and we should be notified
    if receiptCnt is None:
        raise Exception(("Could not find receipt outline. "
            "Try debugging your edge detection and contour steps."))

  
    # apply a four-point perspective transform to the *original* image to
    # obtain a top-down bird's-eye view of the receipt
    receipt = four_point_transform(orig, receiptCnt.reshape(4, 2) * ratio)
    # show transformed image
    cv2.imshow("Receipt Transform", imutils.resize(receipt, width=500))
    cv2.waitKey(0)
    return receipt

def extract_text_from_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image (optional)
    # You can apply various image preprocessing techniques here
    # For example, resizing, denoising, thresholding, etc.
    procesed_image = apply_preprocessing_image(image)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(procesed_image)

    # Split the text into lines
    lines = text.split('\n')

    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    return lines

# Provide the path to your image containing the ticket
image_path = 'tickets/ticket1.jpg' #doesn't work
image_path = 'tickets/20231001_163618.jpg' # works
#image_path = 'tickets/20230703_213912.jpg'

# Extract text from the image
result = extract_text_from_image(image_path)

df_test = pd.DataFrame(columns=['Num_items','item','euro/kg','total price'])
print(df_test)

# Print the extracted lines
for line in result:
    print(line)