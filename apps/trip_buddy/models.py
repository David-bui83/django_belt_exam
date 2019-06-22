from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
  
  def basic_validator(self, postData):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
    if len(postData['first_name']) < 2:
      errors['first_name'] = 'First name must have at least two characters'
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = 'Email needs to be in the correct format'
    if len(postData['last_name']) < 2:
      errors['last_name'] = 'Last name must have at least two characters'
    if len(postData['password']) < 8:
      errors['password'] = 'Password must be at least eight characters long'
    if postData['password'] != postData['confirm']:
      errors['confirm'] = 'Confirm password does not match password'
    return errors

# Create your models here.
class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __repr__(self):
    return f'{self.first_name} {self.last_name}'

class TripManager(models.Manager):
  def trip_validator(self, postData):
    errors = {} 
    today = datetime.now()
    
    if len(postData['destination']) < 3:
      errors['destination'] = 'Destination must be at least 3 characters'
    if datetime.strptime(postData['start_date'],'%Y-%m-%d') < today:
      errors['date'] = 'Start date needs to be in the future'
    if postData['start_date'] > postData['end_date']:
      errors['destination'] = 'Invalid start and end date'
    if len(postData['plan']) < 3:
      errors['plan'] = 'Plan needs to be at least 3 characters'
    return errors

class Trip(models.Model):
  destination = models.CharField(max_length=255)
  user_creates = models.ForeignKey(User, related_name="create_trips")
  user_travels = models.ManyToManyField(User, related_name='travel_trips')
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  plan = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = TripManager()

  def __repr__(self):
    return f'{self.destination}'