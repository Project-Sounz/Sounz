from django.shortcuts import render,redirect,HttpResponse
from .models import * 
from .forms import RegistrationForm
from users.models import Profile,profiledatadb
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userr=authenticate(request,username=username,password=password)
        if userr is not None:
            login(request,userr)
            return HttpResponse("Logged in")
        invalid="Invalid Credentials"
        return render(request,'accounttest.html')

    return render(request,'accounttest.html')

def reg2(request):

         
        if request.method == 'POST':

            uname = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_picture = request.POST.get('profile_picture')

            phone_number = request.POST.get('phonenumber')
            bio = request.POST.get('bio')
            print(uname,email,password,first_name,last_name,bio)
            newins=profiledatadb(username=uname,password=password,firstname=first_name,lastname=last_name,email=email,profile_picture=profile_picture,user_bio=bio)
            newins.save()
            new_user = User.objects.create_user(username=uname, password=password, email=email, first_name=first_name, last_name=last_name)
            new_user.save()
            
            
            return HttpResponse("user has been created")
            if new_user is not None:
                login(request,new_user)
                return redirect('/')
            return redirect('/')
    


        

            
        return render(request,"reg2.html")

def homeCheck(request):
    users = Profile.objects.all()
    return render(request, 'homepage_test.html', {'allusers': users})

def profile(request):
    return render(request, 'profile-posts.html')

def saved(request):
    return render(request, 'profile-saved.html')