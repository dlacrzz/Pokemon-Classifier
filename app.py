from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import json
import io
import os
from PIL import Image

model = load_model('model.h5')

with open('pokemonNames.json', 'r') as f:
    pokemonNames = json.load(f)

app = Flask(__name__)


# Running Locally
@app.route('/')
def index():
    return render_template('index.html')


# Hosting Publically
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']

    try:
        image = Image.open(io.BytesIO(file.read()))
        image = image.convert('RGB')
        image = image.resize((128, 128))
        imageArray = np.array(image) / 255.0
        imageArray = np.expand_dims(imageArray, axis=0)

        probabilities = model.predict(imageArray)[0]
        predictedIndex = int(np.argmax(probabilities))
        predictedPokemon = pokemonNames[predictedIndex]
        confidence = float(probabilities[predictedIndex])

        return jsonify({
            'index': predictedIndex,
            'name': predictedPokemon,
            'probability': round(confidence, 3)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
