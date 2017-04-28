from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import os, binascii, bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateUser(self, postData):
        errorStr = []
        timeError = 0

        if len(postData['name']) < 3:
            errorStr.append("First name can't be less than 3 characters")
        if len(postData['email']) < 1:
            errorStr.append("Email can't be empty")
        if User.objects.filter(email=postData['email']):
            errorStr.append("Email is already registered")
        if not EMAIL_REGEX.match(postData['email']):
            errorStr.append("Invalid email")
        if len(postData["password"]) < 8:
            errorStr.append("Password must be at least 8 characters")
        if postData["password"] != postData["pw_confirm"]:
            errorStr.append("Password didn't match confirmation.")
        if len(postData['date_of_birth']) < 1:
            errorStr.append("Date of birth can't be empty")
            timeError += 1
        
        if timeError == 0:
            birth_date = datetime.strptime(postData["date_of_birth"], "%Y-%m-%d").date()
            if birth_date > date.today():
                errorStr.append("Birthdate start must be in the past")

        # create hashing
        encrypted_pw = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())

        response_to_views = {}
        
        if errorStr:
            response_to_views['status'] = False
            response_to_views['errorStr'] = errorStr
        else:
            user = self.create(name = postData["name"], email = postData["email"], password = encrypted_pw, date_of_birth = postData["date_of_birth"])
            response_to_views['status'] = True
            response_to_views['userobj'] = user
        return response_to_views

    def loginUser(self, postData):
        errorStr = []
        
        user = User.objects.filter(email=postData['email'])
        if not user:
            errorStr.append("Invalid email")
        else: 
            if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) != user[0].password:
                errorStr.append("Password is incorrect.")
        response_to_views = {}
        if errorStr:
            response_to_views['status'] = False
            response_to_views['errorStr'] = errorStr
        else: 
            response_to_views['status'] = True
            response_to_views['userobj'] = user[0]
        return response_to_views

class User(models.Model):
  name = models.TextField(max_length=100)
  email = models.TextField(max_length=100)
  date_of_birth = models.DateField(blank=True, null=True)
  password = models.TextField(max_length=100)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  objects = UserManager()
  def __str__(self):
    return self.name

