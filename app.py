from flask import Flask, request, render_template
from predict import get_prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/predict')
def predict():
    return render_template('predict.html', breed = '', perc = '')

@app.route('/prediction', methods = ['POST', 'GET'])
def prediction():
    if request.method == 'POST':
        f = request.files['file']
        fpath = f'static/files/{f.filename}'
        f.save(fpath)

        prediction = get_prediction(fpath)
        return render_template('predict.html', breed = prediction['breed'], perc = prediction['perc'])
