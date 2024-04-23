from django.shortcuts import render

# Create your views here.
def log(request):
    return render(request,'accounttest.html')

def reg2(request):
    return render(request,"reg2.html")
