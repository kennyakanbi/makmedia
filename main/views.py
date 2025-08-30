from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        get_email = request.POST.get('email')  # Fix case
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')
        if get_password != get_confirm_password:
            messages.info(request, 'Password do not match')
            return render('/auth/signup/')
        try:
            if User.objects.get(username=get_email):
                messages.warning(request, "Email is already taken")
                return redirect('/auth/signup/')  # Redirect instead of render
        except Exception as indentifier:
            pass
        # Correct user creation and saving
        myuser = User.objects.create_user(username=get_email, email=get_email, password=get_password) 
        myuser.save()
        myuser= authenticate(username=get_email, password= get_password)
        messages.success(request, "User created & Login Success")  
        return redirect("/auth/login/")
    return render(request, 'signup.html')
    

def handleLogin(request):
    if request.method == "POST":
        get_email = request.POST.get('email')  
        get_password = request.POST.get('pass1')
        myuser = authenticate(username=get_email, password=get_password)  
        
        if myuser is not None:
            login(request, myuser) 
            messages.success(request, "Login Successful") 
            return redirect('/intern')  
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "login.html") 



def handleLogout(request):
    logout(request)
    messages.success(request, "Logout successfully ")
    return render(request, "login.html")