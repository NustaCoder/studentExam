from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/name"
mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _password = _json['pwd']

    if _name and _password and request.method == 'POST':

        _hased_pwd = generate_password_hash(_password)
        id = mongo.db.password.insert({'name': _name, 'password': _hased_pwd})

        resp = jsonify("user added succefully")
        resp.status_code = 200

        return resp

    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/users')
def get_users():
    users = mongo.db.password.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def get_user(id):
    resp = ""
    user = mongo.db.password.find_one({"_id": ObjectId(id)})
    resp = jsonify(user['name'])
    return resp


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.password.delete_one({"_id": ObjectId(id)})
    resp = jsonify("user deleted successfully")
    resp.status_code = 200

    return resp


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _password = _json['pwd']

    if _name and _password and _id and request.method == 'PUT':
        _hased_pwd = generate_password_hash(_password)

        mongo.db.password.update_one({"_id": ObjectId(_id)}, {
                                     "$set": {"name": _name, "password": _hased_pwd}})

        resp = jsonify('user updated succefully')
        resp.status_code = 200

        return resp
    else:
        return not_found()


if '__name__' == '__name__':
    app.run(debug=True)
