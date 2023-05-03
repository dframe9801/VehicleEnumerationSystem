from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import cv2
import base64
from tracker import *
import time
import schedule
from datetime import datetime

# configuration
DEBUG = True

# =========== Intantiate app ===============
app = Flask(__name__)
app.config.from_object(__name__)
app.config["MONGO_URI"] = "mongodb+srv://wals9256:kQTHJidEp4igvXlF@vehicleenumerationsyste.bb2lcf9.mongodb.net/EnumerationData?retryWrites=true&w=majority"

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# =========== Database =====================
mongo = PyMongo(app)
db = mongo.db

collection_name = "Count"
carCount = db[collection_name]
test_doc = {"name": "Test Document", "value": 42}
result = carCount.insert_one(test_doc)

# =========== Vehicle Detection =============
# Create tracker object
tracker = EuclideanDistTracker()

# streaming 
# camera = cv2.VideoCapture("rtsp://192.168.1.178")
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# test video
camera = cv2.VideoCapture("highway.mp4")

# Counter
counter_global = 0
counter_tenmin = 0
db_id=0

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=40)



@app.route('/video_feed')
def video_feed():
    success, frame = camera.read()
    if not success:
        return jsonify({'success': False})
    
    # ret, buffer = cv2.imencode('.jpg', frame,  [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

    height, width, _ = frame.shape

    # Extract Region of interest
    roi = frame[500: 720, 500: 800]

    # 1. Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 120:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        global counter_global
        counter_global = id + 1
        
    # cv2.imshow("roi", roi)
    # cv2.imshow("Frame", frame)
    # cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        pass

    jpeg_quality = 90
    ret, buffer = cv2.imencode('.jpg', frame,  [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

    frame_base64 = base64.b64encode(buffer.tobytes(), altchars=None).decode('utf-8')
    return jsonify({'success': True, 'frame': frame_base64})



@app.route("/add_one")
def add_one():
    def count_record():
        global counter_tenmin
        global db_id
        db_id = 9
        counter_tenmin = counter_global - counter_tenmin
        current_date = datetime.now()
        post = {"_id": db_id,"Vehicle Count":counter_global,"date":current_date.strftime("%m/%d/%Y, %H:%M")}
        db_id =+1
        return post
    db.carCount.insert_one(count_record())
    return jsonify(message="success")

@app .route("/get_count/<int:countId>")
def get_count(countId):
    ret_count = db.carCount.find_one({"_id":countId})
    return ret_count

@app.route("/counter")
def counter():
    return jsonify(countG=counter_global)

if __name__ == '__main__':
    app.run()
