from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.registration import Register
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def base_route():
    session['current_user_id'] = ""
    session["first_name"] = ""
    session["last_name"] = ""
    session["email"] = ""
    session["email_address"] = ""
    return render_template('/index.html')

@app.route('/index/register_form')
def registration():
    return render_template("login_registration.html")

@app.route('/index/register', methods = ['POST'])
def register():
    if request.form['password'] == "":
        return redirect('/index/register_form')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    if not Register.validate(request.form):
        print("********** registration not valid")
        
        session["first_name"] = request.form['first_name']
        session["last_name"] = request.form['last_name']
        session["email"] = request.form['email']

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
    session["current_user_id"] = ""
    session["first_name"] = ""
    session["last_name"] = ""
    session["email"] = ""
    session["email_address"] = ""
    return render_template('login_registration.html')

@app.route('/index/login/form', methods = ['POST'])
def login_form():
    data = {
        "email": request.form['email'], 
    }
    session["email_address"] = request.form['email']
    user_found = Register.find_email(request.form['email'])
    if not user_found:
        flash("Invalid Email/Password", "email_address")
        return redirect('/index/register_form')
    if not bcrypt.check_password_hash(user_found[0]['password'], request.form['password']):
        print("*********** Invalid password")
        flash("Invalid Email/Password", "password_login")
        return redirect('/index/login')
    session['current_user_id'] = user_found[0]['id']
    print("************* session['current_user_id]: ", session['current_user_id'])
    return redirect('/index/login/conf')

@app.route('/index/login/conf')
def login_conf():
    if session['current_user_id'] == "":
        return redirect('/index/register_form')
    return render_template('login_conf.html')

@app.route('/index/logout')
def logout():
    session['current_user_id'] = ""
    session["first_name"] = ""
    session["last_name"] = ""
    session["email"] = ""
    session["email_address"] = ""
    return redirect('/')

@app.route('/index/review')
def review():

    all_info = Register.get_all()
    return render_template("read_all.html", all_info = all_info)

@app.route('/index/delete/<int:id>')
def delete(id):
    Register.delete(id)
    all_info = Register.get_all()
    return render_template("read_all.html", all_info = all_info)

@app.route('/index/update/<int:id>')
def update(id):
    some_info = Register.show_some(id)
    session['current_user_id'] = id
    return render_template("update.html", some_info = some_info)

@app.route('/index/update/user/<int:id>', methods=['POST'])
def update_db(id):
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
        "conf_password": request.form['conf_password']
    }
    if not Register.validate(request.form):
        print("********** did not validate, cannot update files")
        return redirect('/index/update/{{id}}')
    user_id = Register.update(data, id)
    all_info = Register.get_all()
    session['current_user_id'] = ""
    return redirect('/index/review')

@app.route('/index/find/<int:id>')
def find_one(id):
    some_info = Register.show_some(id)
    return render_template("find_one.html", some_info = some_info)