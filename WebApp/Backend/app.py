from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pickle
import os
from numpy.linalg import norm
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

app = Flask(__name__)
CORS(app)

# Load model and data
model = load_model('model.h5')
feature_list = np.array(pickle.load(open('embedding.pkl', 'rb')))
filenames = pickle.load(open('filenames.pkl', 'rb'))

neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
neighbors.fit(feature_list)

def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

@app.route('/recommend', methods=['POST'])
def recommend():
    file = request.files['file']
    img_path = os.path.join('./static/images', file.filename)
    file.save(img_path)

    features = extract_features(img_path, model)
    distances, indices = neighbors.kneighbors([features])

    recommended_files = [filenames[idx] for idx in indices[0][1:6]]
    return jsonify(recommended_files)

@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory('static/images', filename)

# Paths and constants
shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Ensure button images are loaded correctly
if imgButtonRight is None:
    raise ValueError("Button image could not be loaded from 'Resources/button.png'. Check the file path.")
if imgButtonLeft is None:
    raise ValueError("Button image could not be loaded from 'Resources/button.png'. Check the file path.")

@app.route('/tryon', methods=['GET'])
def try_on():
    detector = PoseDetector()
    cap = cv2.VideoCapture(0)

    # Set the desired resolution for the webcam
    desired_width = 1280
    desired_height = 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera.")
            break

        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if lmList:
            lm11 = lmList[11][1:3]
            lm12 = lmList[12][1:3]
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

            if imgShirt is None:
                print(f"Shirt image could not be loaded from {os.path.join(shirtFolderPath, listShirts[imageNumber])}. Skipping this shirt.")
                continue

            # Calculate shirt width and resize
            widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
            heightOfShirt = int(widthOfShirt * shirtRatioHeightWidth)
            if widthOfShirt > 0 and heightOfShirt > 0:
                imgShirt = cv2.resize(imgShirt, (widthOfShirt, heightOfShirt))
            else:
                print("Invalid dimensions for resizing. Skipping resize operation.")
                continue

            currentScale = (lm11[0] - lm12[0]) / 190
            offsetX = int(44 * currentScale)
            offsetY = int(48 * currentScale)

            shirt_position_x = int(lm12[0] - offsetX)
            shirt_position_y = int(lm12[1] - offsetY - heightOfShirt // 2)  # Adjusted to center the shirt vertically

            try:
                img = cvzone.overlayPNG(img, imgShirt, (shirt_position_x, shirt_position_y))
            except Exception as e:
                print(f"Error overlaying shirt image: {e}")

            img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
            img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

            if lmList[16][1] < 300:
                counterRight += 1
                cv2.ellipse(img, (139, 360), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if imageNumber < len(listShirts) - 1:
                        imageNumber += 1
            elif lmList[15][1] > 900:
                counterLeft += 1
                cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    if imageNumber > 0:
                        imageNumber -= 1
            else:
                counterRight = 0
                counterLeft = 0

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == 27:  # Exit loop if 'ESC' is pressed
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)
