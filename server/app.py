from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import cv2
import base64
from tracker import *

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

# =========== Vehicle Detection =============
# Create tracker object
tracker = EuclideanDistTracker()

# streaming 
camera = cv2.VideoCapture("rtsp://192.168.1.178")
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=40)


@app.route('/video_feed')
def video_feed():
    success, frame = camera.read()
    if not success:
        return jsonify({'success': False})
    
    jpeg_quality = 90
    ret, buffer = cv2.imencode('.jpg', frame,  [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    if ret:
        frame_base64 = base64.b64encode(buffer.tobytes(), altchars=None).decode('utf-8')
        return jsonify({'success': True, 'frame': frame_base64})
    else:
        return jsonify({'success': False, 'error': 'Failed to encode the camera frame'})


if __name__ == '__main__':
    app.run()
