from flask import Flask, jsonify, request, render_template, session, url_for, redirect
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
    if 'username' in session:
        return render_template("homepage.html")
    else:
        return render_template("index.html")


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/logout')
def logoutUser():
    session.pop('username', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('gender', None)
    return redirect(url_for('indexPage'))


@app.route('/home')
def gotoHomePage():
    if 'username' in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for('indexPage'))


@app.route('/login')
def loginPage():
    if 'username' in session:
        return redirect(url_for('gotoHomePage'))
    else:
        return render_template('login.html')


@app.route('/userlogin', methods=['POST'])
def verifyLogin():
    _name = request.form['username']
    _password = request.form['password']

    if request.method == 'POST' and mongo.db.student.find({"username": _name}).count() > 0:
        passval = mongo.db.student.find({"username": _name})
        for val in passval:
            pval = val["password"]
            session['firstname'] = val['firstname']
            session['lastname'] = val['lastname']
            session['username'] = val['username']
            if val['gender'] == "male":
                session['greet'] = "Mr"
            elif val['gender'] == "female":
                session['greet'] = "Miss"

        if check_password_hash(pval, _password):
            return render_template('homepage.html')
        else:
            return not_found()
    else:
        return not_found()


@app.route('/signup.html')
def signupPage():
    if 'username' in session:
        return redirect(url_for('gotoHomePage'))
    else:
        return render_template('signup.html')


@app.route('/maths')
def mathsPage():
    if 'username' in session:
        return render_template('maths.html')
    else:
        return render_template('login.html')


@app.route('/adduser', methods=['POST'])
def addStudent():
    _fname = request.form['fname']
    _lname = request.form['lname']
    _username = request.form['username']
    _password = request.form['password']
    _email = request.form['email']
    _phone = request.form['phone']
    _gender = request.form['gender']
    if request.method == 'POST':

        _hased_pwd = generate_password_hash(_password)
        id = mongo.db.student.insert({'username': _username, 'password': _hased_pwd,
                                      'firstname': _fname, 'lastname': _lname, 'email': _email, 'gender': _gender, 'phone': _phone})
        user = mongo.db.student.find({'username': _username})
        resp = jsonify("user added succefully")
        resp.status_code = 200
        if id:
            for val in user:
                session['firstname'] = val['firstname']
                session['lastname'] = val['lastname']
                session['username'] = val['username']
                if val['gender'] == "male":
                    session['greet'] = "Mr"
                elif val['gender'] == "female":
                    session['greet'] = "Miss"

                return render_template('homepage.html')
        else:
            return not_found()
    else:
        return not_found()


@app.route('/subjects')
def subjectPage():
    if 'username' in session:
        return render_template('subjects.html')
    else:
        return redirect(url_for('loginPage'))


if __name__ == "__main__":
    app.run(debug=True)
