import os
import datetime
import pytz
import math
import json
import ast
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('cred.json')
default_app = initialize_app(cred)
db = firestore.client()
payload_collection = db.collection('payload')


@app.route("/api/store", methods=['POST'])
def create():
    try:
        data = request.get_data()
        # Decode bytes to dict
        data_str = data.decode("UTF-8")
        # print(json.loads(data_str))
        payload_collection.add(json.loads(data_str))
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/api/list', methods=['GET'])
def read():
    try:
        seconds = int(datetime.datetime.now(tz=pytz.utc).timestamp())
        query = payload_collection.where(u'time_end', u'>=', seconds).order_by(
            u"time_end", direction=firestore.Query.ASCENDING).limit(1).stream()
        for doc in query:
            f'{doc.id} => {doc.to_dict()}'
            updated_doc = doc.to_dict()
            updated_doc["timestamp"] = seconds
        return updated_doc
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
