from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import sqlite3
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "authentification\index.html")


def signup(request):

    if request.method =="POST":
        username = request.POST.get('username')
        fname = request.POST['fname']
        sname = request.POST['sname']
        pnumber = request.POST['pnumber']
        email= request.POST['email']
        bdate= request.POST['bdate']
        profi= request.POST['profi']
        passw1= request.POST['passw1']
        passw2= request.POST['passw2']

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
             email, username,passw1,bdate,profi)
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
        
        # Fetch the first matching user
        user = cursor.fetchone()

        conn.close()

        if user is not None:
            # User exists, perform login operation
            # Extract information about the user if needed
            fname = user[5]  

            # Store user information in the session
            request.session['user_fname'] = fname

            # Redirect to the home page or wherever you want
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
    # username = request.POST('username')
    # #connect to the db
    # conn = sqlite3.connect('SkiEnter_database.db')
    # cursor = conn.cursor()

    # # Use fetchone() instead of fetchall()
    # cursor.execute(
    #     """
    #     SELECT * FROM user WHERE login = ? ;
    #     """,
    #     (username)
    # )
    
    # # Fetch the first matching user
    # userid = cursor.fetchone()[0]
    # cursor.execute(
    #     f"""
    #     select *
    #     from skis
    #     join preference_on on preference_on.ski_id = skis.ski_number
    #     where profile_id = {userid};
    #     """)
    # favorite_skis = cursor.fetchall()

    # conn.close()
    return render(request, "authentification\success.html")

def fav(request):
    return redirect("fav")

def lease(request):
    if request.method == "POST":
        weight = request.POST['weight']
        height = request.POST['height']
        stiffness = request.POST['stiffness']
        width = request.POST['width']

        

    # Render the form page if it's a GET request
    return render(request, "authentification/lease.html", {'weight': weight, 'height': height, 'stiffness':stiffness, 'width':width})