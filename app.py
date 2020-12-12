import os
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
from flask import Flask, render_template, request, flash, redirect, url_for
from classification import predict_image
import requests
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

warning_text = "유효하지 않는 URL 또는 Image파일(png, jpg, jpeg)입니다."

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_image_from_internet(url):
    try:
        request_headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
        Safari/537.36'), }
        response = requests.get(url, headers=request_headers)
        src = "./static/images/download.jpg"
        file = open(src, "wb")
        file.write(response.content)
        file.close()
    except Exception as ex:
        raise
    return src


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url', methods=['POST', 'GET'])
def download_url():
    try:
        if request.method == 'POST':
            url = request.form['url']
            if not url or not allowed_file(url):
                raise
            src = get_image_from_internet(url)
            result = predict_image(src)
            print(result)
            return render_template('index.html', filename=src, result=result)
    except Exception as ex:
        return render_template('index.html', warning_text=warning_text)


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if not file or not allowed_file(file.filename):
                raise
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            src = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            result = predict_image(src)
            print(result)
            return render_template('index.html', filename=src, result=result)
    except Exception as ex:
        return render_template('index.html', warning_text=warning_text)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run('0.0.0.0', 5000)
