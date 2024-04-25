from django.shortcuts import render,redirect,HttpResponse
from .models import * 
from .forms import RegistrationForm
from users.models import userdata
# Create your views here.
def log(request):
    return render(request,'accounttest.html')

def reg2(request):
    if request.method == 'POST':

            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_picture = request.POST.get('profile_picture')

            phone_number = request.POST.get('phonenumber')
            bio = request.POST.get('bio')
            print(username,email,password,first_name,last_name,bio)
            new_user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            new_user.save()
            ins=userdata(username=username,password=password,firstname=first_name,lastname=last_name,email=email,phone=phone_number,profile_picture=profile_picture,user_bio=bio)
            ins.save()
            return HttpResponse("user has been created")
        

            
    return render(request,"reg2.html")

def homeCheck(request):
    users = userdata.objects.all()
    return render(request, 'homepage_test.html', {'allusers': users})