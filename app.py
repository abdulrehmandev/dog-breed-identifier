from flask import Flask, request, render_template
from predict import get_prediction

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', pred = {'breed': '', 'perc': ''})


@app.route('/predict', methods = ['POST'])
def predict():
    print(request.form.values())
    if request.method == 'POST':
        f = request.files['file']
        fpath = f'static/files/{f.filename}'
        f.save(fpath)
        prediction = get_prediction(fpath)
        return render_template('index.html', pred = prediction)