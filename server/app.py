from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/VehicleEnumerationSystem")
db = mongodb_client.db

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()
