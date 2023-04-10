from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import cv2

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# database
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/VehicleEnumerationSystem")
db = mongodb_client.db

# streaming 
camera = cv2.VideoCapture("rtsp://192.168.1.178:554/VESTest")


def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()
