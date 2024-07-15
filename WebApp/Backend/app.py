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

if __name__ == '__main__':
    app.run(debug=True)
