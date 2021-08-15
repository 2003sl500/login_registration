from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.registration import Register

@app.route('/')
def base_route():

    return render_template('/index.html')

@app.route('/index/register_form')
def registration():
    return render_template("registration.html")

@app.route('/index/register', methods = ['POST'])
def register():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password']
    }
    if not Register.validate(request.form):
        return redirect('/index/register_form')
    
    user_info = Register.create(data)
    print("************* user_info, controller, line 23, users id: ", user_info)
    session['id'] = user_info
    return redirect('/index/registration_conf')

@app.route('/index/registration_conf')
def registration_conf():
    reg_info = Register.show_some(session['id'])
    return render_template("registration_conf.html", reg_info = reg_info)

@app.route('/index/login')
def login():
    return render_template("login.html")