# import libraries
import cv2
import numpy as np
from pytesseract import image_to_string
import os
os.environ['TESSDATA_PREFIX'] = r'/app/scripts'

# config settings
RESIZE_WIDTH = 712
RESIZE_HEIGHT = 512
CONFIG = '--psm 7'
LANG = 'ara_number'

def extract_nationalId(file):
    """
        Extracts a 14-digit national ID from the input image file.

        Parameters:
            file (file): Input image file.

        Returns:
            str: Extracted 14-digit national ID.
    """

    # Read the image
    gray_img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    # Pre-Processing Image
    resized_img = cv2.resize(gray_img, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_AREA)
    cropped_img = resized_img[resized_img.shape[0]*-7//24:resized_img.shape[0]*-1//10, resized_img.shape[1]*3//-5:]
    removed_bg_img = cv2.adaptiveThreshold(cropped_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 16)

    # Extract nationalId from image
    string = image_to_string(removed_bg_img, lang=LANG, config=CONFIG)

    # Extract digits
    nationalId = ''.join(n for n in string if n.isdigit())

    return nationalId[:14]

# testing post request with commends 
# curl -X POST -F "file=@\"D:\WORK Space\Tutorials\Extracting User Info From National ID\dataset\0.JPG\"" http://localhost:5000/extract_nationalId