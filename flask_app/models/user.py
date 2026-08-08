from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = "stargaze_db"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Formato de email inválido.", "register")
            is_valid = False
        else:
            if User.get_by_email({"email": user['email']}):
                flash("El email ya está registrado.", "register")
                is_valid = False
        if len(user['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Las contraseñas no coinciden.", "register")
            is_valid = False
        return is_valid
