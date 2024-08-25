import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from scpredict.scpredict import Predictor
import traceback
from loguru import logger

logger.add("file_{time}.log")

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
                winrates, name_1, name_2 = predictor.predict(path)
                winrates = list(winrates)
                print("Predicted win rates:", winrates)
                return jsonify({
                    'winrates': winrates,
                    'player_1_name': str(name_1),
                    'player_2_name': str(name_2),
                    'filename': filename
                })
            except Exception as e:
                print("Prediction error:", str(e))
                return jsonify({'error': 'Prediction failed'}), 500
        
        return jsonify({'error': 'Invalid file format'}), 400


class PCAHandler(Resource):

    def post(self):
        if 'filename' not in request.form:
            return jsonify({'error': 'No filename provided'}), 400
        if 'timestamp' not in request.form:
            return jsonify({'error': 'No timestamp provided'}), 400
        
        filename = request.form.get("filename")
        timestamp = request.form.get("timestamp")
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        logger.debug(f'filename: {filename}, timstamp: {timestamp}, path: {path}')

        if os.path.exists(path):
            try:
                file_names, timestamps = predictor.get_pca(path, timestamp=int(timestamp), N=20)
                logger.debug('pca results retrieved')
                logger.debug(str(file_names))
                logger.debug(str(timestamps))
                return jsonify({'file_names':file_names,
                                'timestamps':timestamps})
            except Exception as e:
                logger.debug("PCA error:", str(e))
                logger.exception("")
                return jsonify({'error': 'PCA analysis failed'}), 500
        else:
            return jsonify({'error': 'File not found'}), 400


api.add_resource(ReplayHandler, "/")
api.add_resource(PCAHandler, "/pca")

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', debug=True)
