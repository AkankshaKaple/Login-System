from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__, template_folder='template', static_folder='style')

client = MongoClient()
db = client.Userdata


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')


@app.route("/show-login-page")
def show_login_page():
    return render_template('login.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    is_logged_in = False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.user_info.find({})

        for document in cursor:
            if document['email'] == email and document['password'] == password:
                is_logged_in = True
                print('username is matched n password is matched')
                break
            else:
                is_logged_in = False

    if not is_logged_in:
        print('failed to log in')
        return render_template('index.html')
    else:
        print('logged in')
        return render_template('welcome.html')


@app.route('/registration')
def show_registration_page():
    return render_template('registration.html')


@app.route("/register-user", methods=['GET', 'POST'])
def registration():
    is_user_registered = False
    if request.method == 'POST':
        cursor = db.user_info.find({})
        for document in cursor:
            if request.form['email'] in document['email']:
                is_user_registered = True
                break
            else:
                is_user_registered = False

    if not is_user_registered:
        user_info = {'first_name': request.form['firstName'], "last_name": request.form['lastName'],
                     'email': request.form['email'], 'password': request.form['password']}
        db.user_info.insert(user_info)
        return render_template('index.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
