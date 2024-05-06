from django.shortcuts import render,redirect,HttpResponse
from .models import * 
from .forms import RegistrationForm,EditProfileForm,Uploadform
from users.models import profiledatadb,postdb
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
            return redirect('profile')
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
                    return redirect('profile')    
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
    user=request.user.username
    return render(request, 'profile-fpv.html',{'user':user})

def profile_tpv(request):
    return render(request, 'profile-tpv.html')

def homepage(request):
    return render(request, 'home.html')

def upload(request):
    username=request.user.username
    userobj=profiledatadb.objects.get(username=username)
    if request.method=='POST':
        caption=request.POST.get('title')
        desc=request.POST.get('post_description')
        typ=request.POST.get('tags')
        lan=request.POST.get('language')
        loc=request.POST.get('location')
        form=Uploadform(request.POST,request.GET)
        if form.is_valid(): 
                file=request.FILES.get('post')
        pos=postdb(username=userobj,caption=caption,descr=desc,langu=lan,mediatype=typ,location=loc,media=file)
        pos.save()
        prompt_message = "Post Uploaded"
        return render(request,'upload_form.html',{'prompt_message': prompt_message})

    return render(request, 'upload_form.html',{'user':userobj})

def profile(request):
    try:
        user=request.user.username
        user = profiledatadb.objects.get(username=user)
    except profiledatadb.DoesNotExist:
        user = None
    return render(request, 'profile-fpv.html', {'user': user})    

def nav_saved(request):
    username=request.user.username
    user = profiledatadb.objects.get(username=username)
    return render(request, 'profile-fpv-saved.html',{'user':user})   

def editprofile(request):
    
        username=request.user.username
        user = profiledatadb.objects.get(username=username)
        userauth=User.objects.get(username=username)
        



        if request.method == 'POST':
                if request.POST.get('first_name'):
                    user.firstname = request.POST.get('first_name')
                    userauth.first_name = request.POST.get('first_name')
                if request.POST.get('last_name'):       
                    user.lastname = request.POST.get('last_name')
                    userauth.last_name = request.POST.get('last_name')
                if request.FILES.get('profile_picture'):    
                   user.profile_picture = request.FILES.get('profile_picture')
                if request.POST.get('email'):   
                   user.email=request.POST.get('email')
                   userauth.email=request.POST.get('email')
                if request.POST.get('bio'):   
                   user.user_bio = request.POST.get('bio')
                if request.POST.get('insta'):   
                   user.insta = request.POST.get('insta') 
                if request.POST.get('yout'):   
                   user.yout = request.POST.get('yout')
                if request.POST.get('twit'):   
                   user.twit = request.POST.get('twit')        
                user.save()
                userauth.save()
                return render(request, 'profile-fpv.html', {'user': user})
                
            

        else:
            form = EditProfileForm(instance=user)
        return render(request,'editprofile.html',{'user':user}) 

def signout(request):
    logout(request)
    return redirect('signin')

def media(request):
    return render(request,'media.html')

def mailtemplate(request):
    return render(request, 'mail-template.html')