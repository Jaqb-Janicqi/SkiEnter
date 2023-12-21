from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import sqlite3
from django.contrib.auth.decorators import login_required

from base_classes import SkiPreference, User
from recommendation_engine import Engine

# Create your views here.


def home(request):
    return render(request, "authentification\index.html")


def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST['fname']
        sname = request.POST['sname']
        pnumber = request.POST['pnumber']
        email = request.POST['email']
        bdate = request.POST['bdate']
        profi = request.POST['profi']
        passw1 = request.POST['passw1']
        passw2 = request.POST['passw2']

        if passw1 != passw2:
            messages.error(request, "Password didn't match")

        conn = sqlite3.connect('SkiEnter_database.db')
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO user (name, surname ,phone_number,email,login, password,date_of_birth,proficiency)
            VALUES (?, ?, ?, ?, ?, ?,?,?);
            """,
            (fname, sname, pnumber,
             email, username, passw1, bdate, profi)
        )
        conn.commit()
        messages.success(request, "Your account has been successfully created")

        return redirect('signin')

    return render(request, "authentification\signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        passw1 = request.POST['passw1']

        conn = sqlite3.connect('SkiEnter_database.db')
        cursor = conn.cursor()

        # Use fetchone() instead of fetchall()
        cursor.execute(
            """
            SELECT * FROM user WHERE login = ? AND password = ?;
            """,
            (username, passw1)
        )
        user = cursor.fetchone()
        conn.close()

        if user is not None:
            fname = user[5]
            request.session['user_fname'] = fname
            return render(request, "authentification\success.html", {'fname': fname})

        else:
            # User does not exist or credentials are incorrect
            messages.error(request, "Bad credentials!")
            return redirect('home')

    return render(request, "authentification\signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successgully")
    return redirect("home")


def success(request):
    return render(request, "authentification\success.html")


def fav(request):
    return redirect("fav")


def lease(request):
    if request.method == "POST":
        weight = request.POST['weight']
        height = request.POST['height']
        stiffness = request.POST['stiffness']
        width = request.POST['width']
        fname=request.POST['fname']

        request.session['user_fname'] = fname

        conn = sqlite3.connect('SkiEnter_database.db')
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM user WHERE login = ? ;
            """, (request.session['user_fname'],)
        )
        user_data = cursor.fetchone()  # Use fetchone() to get a single row

        conn.close()

        user = User(user_data[1], user_data[2], 0, 'tmp',
                    'tmp', int(weight), int(height), int(user_data[8]))
        ski_preference = SkiPreference(user, int(stiffness), int(width))
        recommendation_engine = Engine()
        skis = recommendation_engine.generate_recommendation(
            user, ski_preference, 10)

        #xd = str(skis)
    
        return render(request, "authentification/lease.html", {'userID': user_data[0], 'skis': skis, 'weight': weight, 'height': height, 'stiffness': stiffness, 'width': width})
    # Render the form page if it's a GET request
    return render(request, "authentification/lease.html")

def rent_ski(request):
    if request.method == "POST":
        user_id=request.POST['userID']
        ski_id=request.POST['chosen_ski_id']

    # lease the skis 
    recommendation_engine = Engine()
    recommendation_engine.select_ski(user_id, ski_id)
    return render(request, "authentification/rent.html")
