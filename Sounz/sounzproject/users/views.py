from django.shortcuts import render,redirect,HttpResponse
from .models import * 
from .forms import RegistrationForm
from users.models import profiledatadb
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userr=authenticate(request,username=username,password=password)
        if userr is not None:
            login(request,userr)
            return redirect('profile',username=username)
        invalid="Invalid Credentials"
        return render(request,'accounttest.html')

    return render(request,'accounttest.html')

def reg2(request):

         
        if request.method == 'POST':

            uname = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password1=request.POST.get('confirmPassword')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phonenumber')
            bio = request.POST.get('bio')
            print(uname,email,password,first_name,last_name,bio)
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid(): 
                user = form.save(commit=False)
                user.save()
                profile_picture = request.FILES.get('profile_picture')
            if password == password1:
                if User.objects.filter(email=email).exists():
                     prompt_message = "Email taken"
                     return render(request,'reg2.html',{'prompt_message': prompt_message})
                elif User.objects.filter(username=uname).exists():
                     prompt_message = "Username taken"
                     return render(request,'reg2.html',{'prompt_message': prompt_message})
                else:
                    newins=profiledatadb(username=uname,password=password,firstname=first_name,lastname=last_name,email=email,profile_picture=profile_picture,user_bio=bio)
                    newins.save()
                    new_user = User.objects.create_user(username=uname, password=password, email=email, first_name=first_name, last_name=last_name)
                    new_user.save()
                    return redirect('profile',username=uname)    
            else:
                prompt_message = "Passwords do not match. Please try again."
                return render(request,'reg2.html',{'prompt_message': prompt_message})
            
            
            
            
            if new_user is not None:
                login(request,new_user)
                return redirect('/')
            return redirect('/')
    


        

            
        return render(request,"reg2.html")

def homeCheck(request):
    users = profiledatadb.objects.all()
    return render(request, 'homepage_test.html', {'allusers': users})

def profile_fpv(request):
    return render(request, 'profile-fpv.html')

def profile_tpv(request):
    return render(request, 'profile-tpv.html')

def homepage(request):
    return render(request, 'home.html')

def upload(request):
    return render(request, 'upload_form.html')

def profile(request,username):
    try:
        user = profiledatadb.objects.get(username=username)
    except profiledatadb.DoesNotExist:
        user = None
    return render(request, 'profile-fpv.html', {'user': user})    

def nav_saved(request):
    return render(request, 'saved.html')