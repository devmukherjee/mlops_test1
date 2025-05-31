from flask import Flask, render_template, jsonify, request
import os
from flask_cors import CORS,cross_origin
from src.chicken_disease_classification.utils.common import decodeImage
from src.chicken_disease_classification.pipeline.prediction import Prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app= Flask(__name__)
CORS(app)

class clientApp():
    def __init__(self):
        self.image_file='imagefile.jpg'
        self.classifier= Prediction()

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    return "Training done successfully!"
