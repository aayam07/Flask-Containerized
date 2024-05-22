from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://mongodb:27017/')
db = client['mydatabase']
collection = db['mycollection']

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({"message": "Data created successfully"})

@app.route('/read', methods=['GET'])
def read():
    data = list(collection.find())
     # Convert ObjectId to string for serialization
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    # Convert string ID back to ObjectId
    obj_id = ObjectId(id)
    collection.update_one({"_id": obj_id}, {"$set": data})
    return jsonify({"message": "Data updated successfully"})

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    # Convert string ID back to ObjectId
    obj_id = ObjectId(id)
    collection.delete_one({"_id": obj_id})
    return jsonify({"message": "Data deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
