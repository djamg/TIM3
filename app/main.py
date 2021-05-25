import datetime
import pytz
import json
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
import time


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


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == "POST":
        data = request.form.to_dict()
        data["request_source"] = "web"
        data["time_end"] = int(time.mktime(time.strptime(
            data["time_end"], "%m/%d/%Y %I:%M %p")))
        # Decode bytes to dict
        # print(json.loads(data_str))
        payload_collection.add(data)
        return render_template('submit.html')


@app.route('/api/delete')
def delete():
    seconds = int(datetime.datetime.now(tz=pytz.utc).timestamp())

    def delete_collection(coll_ref=payload_collection, batch_size=1):
        docs = coll_ref.where(u'time_end', u'>=', seconds).order_by(
            u"time_end", direction=firestore.Query.ASCENDING).limit(batch_size).stream()
        deleted = 0

        for doc in docs:
            print(f'Deleting doc {doc.id} => {doc.to_dict()}')
            doc.reference.delete()
            deleted = deleted + 1
    delete_collection(coll_ref=payload_collection, batch_size=1)
    return "Succesfully Deleted"


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80, debug=True)
    app.run()
