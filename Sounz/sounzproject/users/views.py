from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import * 
from django.http import Http404
from django.http import HttpResponseRedirect
from .forms import RegistrationForm,EditProfileForm,Uploadform
from django.core.exceptions import ValidationError
from users.models import profiledatadb,postdb
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json

# Create your views here.
def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userr=authenticate(request,username=username,password=password)
        if userr is not None:
            login(request,userr)
            return redirect('my-profile')
        invalid="Invalid Credentials"
        return render(request,'accounttest.html')

    return render(request,'accounttest.html')

def log_new(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userr = authenticate(request, username=username, password=password)
        if userr is not None:
            login(request, userr)
            return redirect('my-profile')
        else:
            prompt_message = "Incorrect username or password"
            return render(request, 'log-new.html', {'prompt_message': prompt_message})

    return render(request, 'log-new.html')

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
                     prompt_message = "Mail already taken!"
                     return render(request,'reg2.html',{'prompt_message': prompt_message})
                elif User.objects.filter(username=uname).exists():
                     prompt_message = "Username taken!"
                     return render(request,'reg2.html',{'prompt_message': prompt_message})
                else:
                    newins=profiledatadb(username=uname,password=password,firstname=first_name,lastname=last_name,email=email,profile_picture=profile_picture,user_bio=bio)
                    newins.save()
                    new_user = User.objects.create_user(username=uname, password=password, email=email, first_name=first_name, last_name=last_name)
                    new_user.save()
                    return redirect('signin')    
            else:
                prompt_message = "Passwords do not match. Please try again."
                return render(request,'reg2.html',{'prompt_message': prompt_message})
            
            
            
            
            if new_user is not None:
                login(request,new_user)
                return redirect('/')
            return redirect('/')
    


        

            
        return render(request,"reg2.html")


def registration_new(request):

         
        if request.method == 'POST':

            uname = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password1=request.POST.get('confirmPassword')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            bio = request.POST.get('bio')
            print(uname,email,password,first_name,last_name,bio)
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid(): 
                user = form.save(commit=False)
                user.save()
                profile_picture = request.FILES.get('profile_picture')
            if password == password1:
                if User.objects.filter(email=email).exists():
                     prompt_message = "Mail already taken!"
                     return render(request,'register-new.html',{'prompt_message': prompt_message})
                elif User.objects.filter(username=uname).exists():
                     prompt_message = "Username taken!"
                     return render(request,'register-new.html',{'prompt_message': prompt_message})
                else:
                    newins=profiledatadb(username=uname,password=password,firstname=first_name,lastname=last_name,email=email,profile_picture=profile_picture,user_bio=bio)
                    newins.save()
                    new_user = User.objects.create_user(username=uname, password=password, email=email, first_name=first_name, last_name=last_name)
                    new_user.save()
                    return redirect('log-in')    
            else:
                prompt_message = "Passwords do not match. Please try again."
                return render(request,'register-new.html',{'prompt_message': prompt_message})
        return render(request,"register-new.html")

def homeCheck(request):
    return render(request, 'homepage_test.html')

def profile_fpv(request):
    try:
        user=request.user.username
        userBioCollect = profiledatadb.objects.get(username=user)
        post=postdb.objects.filter(username=user)
        context={
            'user': userBioCollect,
            'post':post,

        }
        
    except profiledatadb.DoesNotExist:
        user = None
    return render(request, 'profile-fpv.html',context)  

def nav_saved(request):
    # username=request.user.username
    # user = profiledatadb.objects.get(username=username)
    # return render(request, 'profile-fpv-saved.html',{'user':user})   


    user=request.user.username
    test = 'nn'
    userBioCollect = profiledatadb.objects.get(username=user)
    post=postdb.objects.filter(username=test)
    context={
        'user': userBioCollect,
        'post':post,

    }
    return render(request, 'profile-fpv-saved.html',context)

def profile_new(request):
    try:
        user = request.user.username
        userBioCollect = profiledatadb.objects.get(username=user)
        post = postdb.objects.filter(username=user)
        test = 'Stephen'
        saved = postdb.objects.filter(username=test)
        context = {
            'user': userBioCollect,
            'post': post,
            'saved': saved,
        }
        
    except profiledatadb.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'profile-new.html', context)



def profile_tpv(request):
    uname=request.GET.get('uname')
    pname=profiledatadb.objects.get(username=uname)
    user=request.user.username
    userBioCollect = profiledatadb.objects.get(username=user)
    post=postdb.objects.filter(username=pname)
    context={
        'pname':pname,
        'user':userBioCollect,
        'posters':post,
    }
    return render(request, 'profile-tpv.html',context)

def homepage(request):
    all_users = profiledatadb.objects.all()
    username = request.user.username
    user = profiledatadb.objects.get(username=username)
    sliced= profiledatadb.objects.all()[:4]
    topart=profiledatadb.objects.all()
    random_profiles = random.sample(list(topart), min(len(topart), 4))
    # Fetch posts of the current user
    user_posts = postdb.objects.all().order_by('-timestamp')
    context = {
        'all_users': all_users,
        'user': user,
        'user_posts': user_posts,
        'sliced':sliced,
        'topart':random_profiles
    }
    return render(request, 'home.html',context)

def upload(request):
    username = request.user.username
    userobj = profiledatadb.objects.get(username=username)
    
    if request.method == 'POST':
        caption = request.POST.get('title')
        desc = request.POST.get('post_description')
        typ = request.POST.get('tags')
        media_type = request.POST.get('media_type')
        lan = request.POST.get('language')
        loc = request.POST.get('location')
        form = Uploadform(request.POST, request.GET)

        if form.is_valid(): 
            file = request.FILES.get('post')
            gotthumbnail = request.FILES.get('thumbnail')

            # Validate file type
            if file and not file.content_type.startswith(('video/', 'audio/')):
                prompt_message = "Invalid file type. Only video and audio files are allowed."
                return render(request, 'upload_form.html', {'user': userobj, 'prompt_message': prompt_message})

            pos = postdb(username=userobj, caption=caption, descr=desc, langu=lan, mediatype=typ, location=loc, media=file, media_format=media_type, media_thumbnail=gotthumbnail)
            pos.save()

            prompt_message = "Post successfully uploaded!"
            return render(request, 'upload_form.html', {'user': userobj, 'prompt_message': prompt_message})

    return render(request, 'upload_form.html', {'user': userobj})


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
    response = HttpResponseRedirect('/')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def media(request):
    username=request.user.username
    user = profiledatadb.objects.get(username=username)
    pid = request.GET.get('pid')
    post=postdb.objects.get(pid=pid)
    ps=post.username
    puser=profiledatadb.objects.get(username=ps)
    user_liked = Like.objects.filter(user=user, post=post).exists()
    context={
        "puser":puser,
        "post":post,
        "user":user,
        "user_liked": user_liked
    }
    return render(request,'media.html',context)

def media_controll(request):
    username=request.user.username
    user = profiledatadb.objects.get(username=username)
    pid = request.GET.get('pid')
    post=postdb.objects.get(pid=pid)
    ps=post.username
    puser=profiledatadb.objects.get(username=ps)
    context={
        "puser":puser,
        "post":post,
        "user":user
    }
    return render(request,'media-controll.html',context)

def mailtemplate(request):
    return render(request, 'mail-template.html')

def sendemail(request):
    send_mail(
        "Collab Request",
        """Hi {{ post_owner }}
            {{ collaborator_name }} has expressed interest in collaborating on your post.
            You can reach out to them at {{ collaborator_email }}.
            Regards,
            Team Sounz""",
        "asishchandra82@gmail.com",
        ["21rt199@vjcet.org"],
        fail_silently=False,
    )

    return render(request,'media.html')



#like and unlike
@login_required
def toggle_like(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')

            # Log post_id for debugging
            print(f"Received post_id: {post_id}")

            # Fetch the post
            post = get_object_or_404(postdb, pid=post_id)

            # Check if the user already liked the post
            user = request.user
            like = Like.objects.filter(user=user, post=post).first()

            if like:
                # Remove like
                like.delete()
                post.likes -= 1
                liked = False
            else:
                # Add like
                Like.objects.create(user=user, post=post)
                post.likes += 1
                liked = True

            post.save()

            return JsonResponse({
                'success': True,
                'liked': liked,
                'like_count': post.likes
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def media(request):
    username = request.user.username
    user = profiledatadb.objects.get(username=username)
    pid = request.GET.get('pid')
    post = postdb.objects.get(pid=pid)

    user_liked = Like.objects.filter(user=request.user, post=post).exists()

    ps = post.username
    puser = profiledatadb.objects.get(username=ps)
    context = {
        "puser": puser,
        "post": post,
        "user": user,
        "user_liked": user_liked
    }

    return render(request, 'media.html', context)
def custom_404(request, exception):
    print("Custom 404 handler called")
    return render(request, '404.html', status=404)

def search(request):
    if request.method == 'POST':
        if request.POST.get("search-input1"):
            input_value = request.POST.get("search-input1")
            posts = postdb.objects.filter(
            Q(mediatype__icontains=input_value) | Q(username=input_value) | Q(caption__icontains=input_value)
            )
            all_users = profiledatadb.objects.all()
            username = request.user.username
            user = profiledatadb.objects.get(username=username)
            sliced= profiledatadb.objects.all()[:4]
            topart=profiledatadb.objects.all()
            random_profiles = random.sample(list(topart), min(len(topart), 4))
            context = {
            'all_users': all_users,
            'user': user,
            'user_posts': posts,
            'sliced':sliced,
            'topart':random_profiles
            }
            return render(request,'search.html',context)

            
    all_users = profiledatadb.objects.all()
    username = request.user.username
    user = profiledatadb.objects.get(username=username)
    sliced= profiledatadb.objects.all()[:4]
    topart=profiledatadb.objects.all()
    random_profiles = random.sample(list(topart), min(len(topart), 4))
    # Fetch posts of the current user
    user_posts = postdb.objects.all().order_by('-timestamp')
    context = {
        'all_users': all_users,
        'user': user,
        'user_posts': user_posts,
        'sliced':sliced,
        'topart':random_profiles
    }

    return render(request,'search.html',context)
    