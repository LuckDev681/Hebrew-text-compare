from flask import Flask, request,jsonify
from flask_cors import CORS
import base64
import cv2
import pytesseract
import numpy as np

app = Flask(__name__)
CORS(app)
@app.route('/api/similarity', methods=['POST'])
def result():
    image1_data = request.json['image1']
    image2_data = request.json['image2']    
    image1_data = base64.b64decode(image1_data.split(',')[1])
    image2_data = base64.b64decode(image2_data.split(',')[1])
    image1 = cv2.imdecode(np.frombuffer(image1_data, np.uint8), cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imdecode(np.frombuffer(image2_data, np.uint8), cv2.IMREAD_GRAYSCALE)

    newwidth = 1600
    newheight = 600

    reimage1=cv2.resize(image1, (newwidth, newheight))
    reimage2=cv2.resize(image2, (newwidth, newheight))
    # Apply thresholding to segment the text from the background
    _, thresh1 = cv2.threshold(reimage1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    _, thresh2 = cv2.threshold(reimage2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    text1 = pytesseract.image_to_string(thresh1, lang='heb')
    text2 = pytesseract.image_to_string(thresh2, lang='heb')
    # Calculate font size
    font_size1 = len(text1) / (thresh1.shape[0] * thresh1.shape[1])
    font_size2 = len(text2) / (thresh2.shape[0] * thresh2.shape[1])

    # Calculate font weight
    font_weight1 = np.mean(np.abs(np.diff(np.diff(thresh1))))
    font_weight2 = np.mean(np.abs(np.diff(np.diff(thresh2))))

    # Calculate letterform width
    letterform_width1 = np.mean(np.diff(np.diff(thresh1)))
    letterform_width2 = np.mean(np.diff(np.diff(thresh2)))

    # Calculate spacing between letters
    spacing1 = np.mean(np.diff(np.diff(thresh1)))
    spacing2 = np.mean(np.diff(np.diff(thresh2)))

    # Calculate stroke width
    stroke_width1 = np.mean(np.abs(np.diff(thresh1)))
    stroke_width2 = np.mean(np.abs(np.diff(thresh2)))

    # Calculate ascender and descender lengths
    ascender1 = np.mean(np.diff(thresh1))
    ascender2 = np.mean(np.diff(thresh2))
    descender1 = np.mean(np.diff(thresh1))
    descender2 = np.mean(np.diff(thresh2))

    # Calculate the similarity between the typefaces
    similarity = np.mean(np.abs(font_size1 - font_size2) +
                        np.abs(font_weight1 - font_weight2) +
                        np.abs(letterform_width1 - letterform_width2) +
                        np.abs(spacing1 - spacing2) +
                        np.abs(stroke_width1 - stroke_width2) +
                        np.abs(ascender1 - ascender2) +
                        np.abs(descender1 - descender2))
    result = 100-round(similarity*10)
    
    if result>=90: summary="Same Author"
    elif 0<result<90: summary="Different Author"
    elif result<0: result=0; summary="Different Author"
    return jsonify({'result': result, 'summary': summary})
if __name__ == '__main__':
    app.run()