from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

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
        print("************* RESULTS: ", results)
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
        print("************* show_some(), results: ", results)
        information = []
        for info in results:
            information.append( cls(info) )
        return information

    @classmethod
    def create(cls, data):
        query = f'INSERT INTO {TABLE1}( first_name, last_name, email, password, updated_at ) VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW() );'
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_i]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if (form_data['first_name'] == "") or (len(form_data['first_name']) < 3):
            print("********** registration.py, line 50")
            flash("First name must be at least 3 characters")
            is_valid = False
        if (form_data['last_name'] == "") or (len(form_data['last_name']) < 3):
            print("********** registration.py, line 54")
            flash("Last name must be at least 3 characters")
            is_valid = False
        if (form_data['email'] == ""):
            print("********** registration.py, line 58")
            flash("Email is required")
            is_valid = False
        elif (EMAIL_REGEX.match(form_data['email'])):
            print("********** registration.py, line 61")
            return is_valid
        else:
            print("********** registration.py, line 64")
            is_valid = False
            return is_valid

        return
