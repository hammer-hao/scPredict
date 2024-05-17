import os
from flask import Flask, flash, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from scpredict import mlp_predict

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'sc2replay'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key_here'

def response(message):
    resp = make_response(message)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return response(f'No file part: parts available: {request.files}')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return response('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #print(path)
            file.save(path)
            out = str(mlp_predict(path))
            os.remove(path)
            return response(out)
    return response('suck my dick')

if __name__ == "__main__":
    app.run(host='0.0.0.0')