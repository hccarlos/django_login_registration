from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "login_registration/index.html")
def register(request):
    all_ok = True
    user_info = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'password_confirmation': request.POST['password_confirmation']
    }
    if not User.objects.validate_name(user_info['first_name']):
        all_ok = False
        messages.add_message(request, messages.ERROR, 'First name must contain only alphabetic characters, and at least 2 characters long')
    if not User.objects.validate_name(user_info['last_name']):
        all_ok = False
        messages.add_message(request, messages.ERROR, 'Last name must contain only alphabetic characters, and at least 2 characters long')
    if not User.objects.validate_email(user_info['email']):
        all_ok = False
        messages.add_message(request, messages.ERROR, 'Invalid email format')
    if User.objects.validate_email_duplicates(user_info['email']):
        all_ok = False
        messages.add_message(request, messages.ERROR, 'Email already exists in system')
    if not User.objects.validate_password_confirmation(user_info['password'], user_info['password_confirmation']):
        all_ok = False
        messages.add_message(request, messages.ERROR, 'Password needs to match password confirmation')
    if not User.objects.validate_password(user_info['password']):
        all_ok = False
        messages.add_message(request, messages.ERROR, 'Password must have at least 8 characters')
    if all_ok:
        # save user
        User.objects.save_user(user_info)
        messages.add_message(request, messages.SUCCESS, 'User registered successfully')
        return redirect("/success")
    else:
        return redirect("/")

def login(request):
    result = User.objects.validate_login(request.POST['email'], request.POST['password'])
    if result[0] == True:
        # means log in successful
        messages.add_message(request, messages.SUCCESS, 'Welcome, ' + result[1].first_name)
        return redirect("/success")
    elif result[0] == False:
        # could mean no user or incorrect password
        messages.add_message(request, messages.ERROR, result[1])
        return redirect("/")
def success(request):
    return render(request, "login_registration/success.html")
