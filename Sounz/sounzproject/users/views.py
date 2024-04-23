from django.shortcuts import render
from .models import * 
# Create your views here.
def log(request):
    return render(request,'accounttest.html')

def reg2(request):
    return render(request,"reg2.html")

def homeCheck(request):
    users = userdata.objects.all()
    return render(request, 'homepage_test.html', {'allusers': users})