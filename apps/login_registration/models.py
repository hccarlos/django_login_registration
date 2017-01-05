from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]{2,}')
PASSWORD_REGEX = re.compile(r'.{8,}')
# Create your models here.

class UserManager(models.Manager):
    def validate_name(self, name):
        return bool(NAME_REGEX.match(name))
    def validate_email_duplicates(self, email):
        try:
            one_user = User.objects.get(email=email)
            return True # means duplicates
        except User.DoesNotExist:
            return False
    def validate_email(self, email):
        return bool(EMAIL_REGEX.match(email))
    def validate_password_confirmation(self, password, password_confirmation):
        return password == password_confirmation
    def validate_password(self, password):
        return bool(PASSWORD_REGEX.match(password))
    def save_user(self, user_info):
        User.objects.create(
            first_name = user_info['first_name'],
            last_name = user_info['last_name'],
            email = user_info['email'],
            hashed_pass = bcrypt.hashpw(user_info['password'].encode(), bcrypt.gensalt())
            )
        return {'success': 'User registered'}
    def validate_login(self, email, password):
        try:
            one_user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode(), one_user.hashed_pass.encode()) == one_user.hashed_pass:
                return (True, one_user)
            else:
                return (False, "Incorrect password")
        except User.DoesNotExist:
            return (False, "User with such email does not exist")

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    hashed_pass = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
