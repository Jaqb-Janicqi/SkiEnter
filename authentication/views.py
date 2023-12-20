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

# def signin(request):
    
#     if request.method == "POST":
#         username = request.POST['username']
#         passw1 = request.POST['passw1']

#         conn = sqlite3.connect('SkiEnter_database.db')
#         c = conn.cursor()
#         c.execute(
#             """
#             SELECT * FROM user WHERE login=? 
#             """,(username,)
#         )
#         conn.commit()
#         user=c.fetchall()

#         messages.success(request, "Logged out successgully")

#         if  len(user) != 0:
#              #check / or \
#              return render(request, "authentification\index.html", {'fname': user[0][5]} )
#         else:
#              messages.success(request, "Bad creentials!")

#              return redirect('home')    
        

#     return render(request, "authentification\signin.html")

# def signin(request):
    
#     if request.method == "POST":
#         username = request.POST['username']
#         passw1 = request.POST['passw1']

#         user = authenticate(username= username, password=passw1)

#         if user is not None:
#             login(request, user)
#             #check / or \
#             return render(request, "authentication\index.html", {'fname': fname} )
#         else:
#             messages.error(request, "Bad creentials!")
#             return redirect('home')

#     return render(request, "authentification\signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successgully")
    return redirect("home")


def success(request):
    return render(request, "authentification\success.html")