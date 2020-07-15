from flask import Flask, jsonify, request, render_template
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['MONGO_URI'] = "mongodb://nusta_coder:shadow7431@cluster0-shard-00-00-kwsyr.mongodb.net:27017,cluster0-shard-00-01-kwsyr.mongodb.net:27017,cluster0-shard-00-02-kwsyr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def indexPage():
    return render_template("index.html")


@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/userlogin', methods=['POST'])
def verifyLogin():
    _name = request.form['username']
    _password = request.form['password']
    res = jsonify("yes")
    pes = jsonify("fail")

    if request.method == 'POST' and mongo.db.student.find({"name": _name}).count() > 0:
        passval = mongo.db.student.find({"name": _name}, {"password": 1})
        for val in passval:
            pval = val["password"]
        if check_password_hash(pval, _password):
            return res
        else:
            return pes
    else:
        return pes


@app.route('/signup.html')
def signupPage():
    return render_template('signup.html')


@app.route('/adduser', methods=['POST'])
def addStudent():
    _fname = request.form['fname']
    _lname = request.form['lname']
    _username = request.form['username']
    _password = request.form['password']
    _email = request.form['email']
    _phone = request.form['phone']

    if request.method == 'POST':

        _hased_pwd = generate_password_hash(_password)
        id = mongo.db.student.insert({'username': _username, 'password': _hased_pwd,
                                      'firstname': _fname, 'lastname': _lname, 'email': _email, 'phone': _phone})
        resp = jsonify("user added succefully")
        resp.status_code = 200

        return resp


if __name__ == "__main__":
    app.run(debug=True)
