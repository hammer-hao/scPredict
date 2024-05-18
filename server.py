import os
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from scpredict.scpredict import Predictor

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'sc2replay'}

predictor = Predictor()

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class ReplayHandler(Resource):

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def post(self):
        # Get Text type fields
        form = request.form.to_dict()
        print(form)

        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files.get("file")
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            out = list(predictor.predict(path))
            os.remove(path)
            return {'winrates': out}

api.add_resource(ReplayHandler, "/")

if __name__ == "__main__":
    app.run(host='0.0.0.0')