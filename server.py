import os
from flask import Flask, request, jsonify
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
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files.get("file")
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            
            try:
                winrates = list(predictor.predict(path))
                print("Predicted win rates:", winrates)
                os.remove(path)
                return jsonify({'winrates': winrates})
            except Exception as e:
                print("Prediction error:", str(e))
                return jsonify({'error': 'Prediction failed'}), 500
        
        return jsonify({'error': 'Invalid file format'}), 400

api.add_resource(ReplayHandler, "/")

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', debug=True)
