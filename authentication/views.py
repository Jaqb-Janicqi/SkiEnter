from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login


# from django.core.mail import EmailMessage, send_mail
# from geeksforgeeks import settings
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_text
# from django.contrib.auth import authenticate, login, logout
#from . tokens import generate_token

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
        profi= request.POST['fnaprofime']
        passw1= request.POST['passw1']
        passw2= request.POST['passw2']

        #TO THE DATABASE!!!! CURRENTLY USES DJANGO
        myuser = User.object.create_user(username, email, passw1)
        myuser.first_name=fname
        myuser.last_name=sname
        myuser.phone_number=pnumber
        myuser.birth_date=bdate
        myuser.proficiency=profi
        
        myuser.save()
        messages.success(request, "Your account has been successfully created")

        return redirect('signin')
        
    return render(request, "authentification\signup.html")



def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        passw1 = request.POST['passw1']

        user = authenticate(username= username, password=passw1)

        if user is not None:
            login(request, user)
            #check / or \
            return render(request, "authentication\index.html", {'fname': fname} )
        else:
            messages.error(request, "Bad creentials!")
            return redirect('home')

    return render(request, "authentification\signin.html")


def signout(request):
    
    pass