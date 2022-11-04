from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL("users_schema").query_db(query)
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        return connectToMySQL("users_schema").query_db(query, data)
    
    @staticmethod
    def validate(data):
        email_query = "SELECT email FROM users WHERE email = %(email)s"
        is_there = connectToMySQL("users_schema").query_db(email_query, data)
        is_valid = True
        if is_there:
            flash("Email is already in use")
            is_valid = False
        if len(data['first_name']) < 1:
            flash("First name must be at least 1 characters")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name must be at least 1 characters")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is in the wrong format")
            is_valid = False
        return is_valid