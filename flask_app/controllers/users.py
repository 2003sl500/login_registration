from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.registration import Register
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def base_route():

    return render_template('/index.html')

@app.route('/index/register_form')
def registration():
    return render_template("registration.html")

@app.route('/index/register', methods = ['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    if not Register.validate(request.form):
        print("********** registration not valid")
        return redirect('/index/register_form')
    else:
        print("********** registration valid")
        user_info = Register.create(data)
        session['id'] = user_info
        session['current_user_id'] = user_info
        return redirect('/index/login/conf')

@app.route('/index/registration_conf')
def registration_conf():
    reg_info = Register.show_some(session['id'])
    session['id'] = ""
    return render_template("registration_conf.html", reg_info = reg_info)

@app.route('/index/login')
def login():
    session['current_user_id'] = ""
    return render_template('login.html')

@app.route('/index/login/form', methods = ['POST'])
def login_form():
    data = {
        "email": request.form['email'], 
    }
    user_found = Register.find_email(request.form['email'])
    if not user_found:
        flash("Invalid Email/Password")
        return redirect('/index/register_form')
    if not bcrypt.check_password_hash(user_found[0]['password'], request.form['password']):
        print("*********** Invalid password")
        flash("Invalid Email/Password")
        return redirect('/index/login')
    session['current_user_id'] = user_found[0]['id']
    print("************* session['current_user_id]: ", session['current_user_id'])
    return redirect('/index/login/conf')

@app.route('/index/login/conf')
def login_conf():
    if session['current_user_id'] == "":
        return redirect('/index/register_form')
    return render_template('login_conf.html')