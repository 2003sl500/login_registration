from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.controllers.users import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

DATABASE = 'reg'
TABLE1 = 'personal_info'

class Register:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'SELECT * FROM {TABLE1};'
        results = connectToMySQL(DATABASE).query_db(query)
        information = []
        for info in results:
            information.append( cls(info) )
        return information

    @classmethod
    def show_some(cls,id):
        query = f'SELECT * FROM {TABLE1} WHERE id = %(id)s;'
        data = {
            'id': id
        }
        results = connectToMySQL(DATABASE).query_db(query, data)
        information = []
        for info in results:
            information.append( cls(info) )
        return information

    @classmethod
    def create(cls, data):
        # pw = bcrypt.generate_password_hash(data['password'])
        query = f'INSERT INTO {TABLE1}( first_name, last_name, email, password, updated_at ) VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW() );'
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def find_email(cls, email):
        query = f'SELECT id, password FROM {TABLE1} WHERE email = %(email)s;'
        data = {
            'email': email
        }
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_i]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if (form_data['first_name'] == "") or (len(form_data['first_name']) < 3):
            print("********** registration.py, line 59")
            flash("First name must be at least 3 characters")
            is_valid = False
        if (form_data['last_name'] == "") or (len(form_data['last_name']) < 3):
            print("********** registration.py, line 63")
            flash("Last name must be at least 3 characters")
            is_valid = False
        if (form_data['email'] == ""):
            print("********** registration.py, line 67")
            flash("Email is required")
            is_valid = False
        if Register.find_email(form_data['email']):
            flash("You are already registered")
            is_valid = False
            return is_valid
        elif not (EMAIL_REGEX.match(form_data['email'])):
            print("********** registration.py, line 75")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long")
            print("************* password length: ", len(form_data['password']))
            is_valid = False
        elif (form_data['password']) != (form_data['conf_password']):
            print("********** password does not match conf_password")
            flash("Password does not match Confirm Password")
            is_valid = False

        return is_valid
