from flask import Flask, render_template, jsonify, request
import os
from flask_cors import CORS,cross_origin
from src.chicken_disease_classification.utils.common import decodeImage
from src.chicken_disease_classification.pipeline.prediction import PredictionPipeline

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app= Flask(__name__)
CORS(app)

class clientApp():
    def __init__(self):
        self.image_file='imagefile.jpg'
        self.classifier= PredictionPipeline()

clApp= clientApp()

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    return "Training done successfully!"

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.image_file)
    result = clApp.classifier.predict(clApp.image_file)
    return jsonify(result)


if __name__ == "__main__":
    # clApp = ClientApp()
    # app.run(host='0.0.0.0', port=8080) #local host
    # app.run(host='0.0.0.0', port=8080) #for AWS
    app.run(host='0.0.0.0', port=80) #for AZURE
