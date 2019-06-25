from django.shortcuts import render, HttpResponse, redirect
from apps.trip_buddy.models import User, Trip
from django.contrib import messages
from datetime import datetime
import bcrypt

# Create your views here.
def index(request):
  return render(request, 'trip_buddy/index.html')

# Register
def register(request):

  errors = User.objects.basic_validator(request.POST)
  print(errors)
  exist = User.objects.filter(email=request.POST['email'])

  if exist:
    messages.error(request, 'Email is unavaliable')
    return redirect('/')
    
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:
    hashed_pass = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
    User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hashed_pass)

    success = User.objects.last()
    request.session['user_id'] = success.id
    return redirect('/dashboard')

# Dashboard
def dashboard(request):
  # Checking to see if is signed in
  if not 'user_id' in request.session:
    return redirect('/')
  print(Trip.objects.filter(user_creates=request.session['user_id']))
  # Display trips on dashboard
  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'trips': Trip.objects.filter(user_creates=request.session['user_id']),
    'joins': Trip.objects.filter(user_travels=request.session['user_id']),
    'others': Trip.objects.all().exclude(user_travels=request.session['user_id']).exclude(user_creates=request.session['user_id'])
  }

  return render(request, 'trip_buddy/dashboard.html', context)

# log in requirements
def login(request):

  try:
    User.objects.get(email=request.POST['lge'])
  except:
    messages.error(request, 'Invalid user')
    return redirect('/')
  user_pw = User.objects.get(email=request.POST['lge'])
  if bcrypt.checkpw(request.POST['login-pw'].encode(), user_pw.password.encode()):
    request.session['user_id'] = user_pw.id
    return redirect('/dashboard')
  else:
    messages.error(request, 'Incorrect password')
    return redirect('/')

# New trip page
def trip_new(request):
  context = {
    'user': User.objects.get(id=request.session['user_id'])
  }
  return render(request, 'trip_buddy/trip_new.html',context)

# Create trip
def trip_create(request):
  
  if not request.POST['start_date']:
    messages.error(request, 'Need to have a start date')
    return redirect('/trips/new')
  if not request.POST['end_date']:
    messages.error(request, 'Need to have an end date')
    return redirect('/trips/new')
  errors = Trip.objects.trip_validator(request.POST)
  print(errors)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/trips/new')
  else:
    
    new_trip = Trip.objects.create(destination=request.POST['destination'],user_creates=User.objects.get(id=request.session['user_id']),start_date=request.POST['start_date'],end_date=request.POST['end_date'],plan=request.POST['plan'])
    
    return redirect('/dashboard')

# Edit page
def trip_edit(request, id):
  # Prevent non-owner trip from making edit
  trip = Trip.objects.get(id=id)
  if trip.user_creates.id != request.session['user_id']:
    return redirect('/dashboard')

  start = Trip.objects.get(id=id)
  context ={
    'trip': Trip.objects.get(id=id),
    'start_date': start.start_date.strftime('%Y-%m-%d'),
    'end_date': start.end_date.strftime('%Y-%m-%d')
  }

  return render(request, 'trip_buddy/trip_edit.html', context)

# Make edit to trip
def make_edit(request, id):

  # Prevent non-owner trip from making edit
  trip = Trip.objects.get(id=id)
  if trip.user_creates.id != request.session['user_id']:
    return redirect('/dashboard')

  errors = Trip.objects.trip_validator(request.POST)

  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/trips/edit/'+ str(id))
  else:
    trip = Trip.objects.get(id=id)
    trip.destination = request.POST['destination']
    trip.start_date = request.POST['start_date']
    trip.end_date = request.POST['end_date']
    trip.plan = request.POST['plan']
    trip.save()
    return redirect('/dashboard')

# View Trip
def view_trip(request, id):
  trip = Trip.objects.get(id=id)
  trip_creator = trip.user_creates
  travelers = trip.user_travels
  
 
  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'trip': Trip.objects.get(id=id),
    'sd': trip.start_date.date(),
    'ed': trip.end_date.date(),
    'joins': travelers.exclude(travel_trips__id=trip_creator.id)
  }
  return render(request, 'trip_buddy/view_trip.html',context)

# Join a trip
def join_trip(request, id):
 
  trip = Trip.objects.get(id=id)
  user = User.objects.get(id=request.session['user_id'])
  trip.user_travels.add(user)
  print(trip)
  return redirect('/dashboard')

# Unjoin a trip
def remove_trip(request, id):
  trip = Trip.objects.get(id=id)
  trip.user_travels.remove(User.objects.get(id=request.session['user_id']))
  return redirect('/dashboard')

# Delete a trip
def delete_trip(request, id):
  trip = Trip.objects.get(id=id)
  trip.delete()
  return redirect('/dashboard')

# Logout - clear session
def logout(request):
  del request.session['user_id']
  return redirect('/')