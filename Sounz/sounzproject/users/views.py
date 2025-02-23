from django.shortcuts import render,redirect, get_object_or_404
from .models import * 
from django.http import Http404
from django.http import HttpResponseRedirect
from .forms import RegistrationForm,EditProfileForm,Uploadform
from django.core.exceptions import ValidationError
from users.models import profiledatadb,postdb,Collab_Information, Member_Information
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
import threading
from django.urls import reverse

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
            profile_picture = request.FILES.get('profile_picture')
            if not profile_picture:
                profile_picture = 'default/user.png'

            print(uname,email,password,first_name,last_name,bio,profile_picture)
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid(): 
                user = form.save(commit=False)
                user.save()

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
    userBioCollect = profiledatadb.objects.get(username=user)
    post=postdb.objects.filter(username=user)
    saved = Save.objects.filter(user=request.user).values_list('post', flat=True)
    savedposts = postdb.objects.filter(pid__in=saved)
    context={
        'user': userBioCollect,
        'post':post,
        'saved': savedposts,

    }
    return render(request, 'profile-fpv-saved.html',context)

def profile_new(request):
    try:
        user = request.user.username
        userBioCollect = profiledatadb.objects.get(username=user)
        post = postdb.objects.filter(username=user)
        saved = Save.objects.filter(user=request.user).values_list('post', flat=True)
        savedposts = postdb.objects.filter(pid__in=saved)
        context = {
            'user': userBioCollect,
            'post': post,
            'saved': savedposts,
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
                
                return redirect('my-profile')



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

# def media(request):
#     username=request.user.username
#     user = profiledatadb.objects.get(username=username)
#     pid = request.GET.get('pid')
#     post=postdb.objects.get(pid=pid)
#     ps=post.username
#     puser=profiledatadb.objects.get(username=ps)
#     user_liked = Like.objects.filter(user=user, post=post).exists()
#     context={
#         "puser":puser,
#         "post":post,
#         "user":user,
#         "user_liked": user_liked
#     }
#     return render(request,'media.html',context)

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

@login_required
def toggle_save(request):
    if request.method == 'POST':
        try:
            print("hello")
            data = json.loads(request.body)
            post_id = data.get('post_id')

            # Log post_id for debugging
            print(f"Received post_id: {post_id}")

            # Fetch the post
            post = get_object_or_404(postdb, pid=post_id)

            # Check if the user already liked the post
            user = request.user
            save = Save.objects.filter(user=user, post=post).first()

            if save:
                # Remove like
                save.delete()
                saved = False
            else:
                # Add like
                Save.objects.create(user=user, post=post)
                saved = True

            post.save()
            print("success")
            return JsonResponse({
                'success': True,
                'saved': saved,
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
    user_saved = Save.objects.filter(user=request.user, post=post).exists()

    ps = post.username
    puser = profiledatadb.objects.get(username=ps)
    context = {
        "puser": puser,
        "post": post,
        "user": user,
        "user_liked": user_liked,
        "user_saved": user_saved

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


def editpost(request):
    username = request.user.username
    userobj = profiledatadb.objects.get(username=username)
    post_id = request.GET.get('post_id')
    try:
        pos = postdb.objects.get(pid=post_id)
    except postdb.DoesNotExist:
        prompt_message = "Post not found."
        return render(request, 'edit-post.html', {'user': userobj, 'prompt_message': prompt_message})
    
    if request.method == 'POST':
        caption = request.POST.get('title')
        desc = request.POST.get('post_description')
        typ = request.POST.get('tags')
        media_type = request.POST.get('media_type')
        lan = request.POST.get('language')
        loc = request.POST.get('location')
        form = Uploadform(request.POST, request.GET)

        if form.is_valid():
            # Update only the specified post fields
            pos.caption = caption
            pos.descr = desc
            pos.langu = lan
            pos.mediatype = typ
            pos.location = loc
            pos.media_format = media_type
            pos.save()

            prompt_message = "Post successfully updated!"
            ps = pos.username
            puser = profiledatadb.objects.get(username=ps)
            user_liked = Like.objects.filter(user=request.user, post=pos).exists()
            user_saved = Save.objects.filter(user=request.user, post=pos).exists()
            context = {
                "puser": puser,
                "post": pos,
                "user": userobj,
                "user_liked": user_liked,
                "user_saved": user_saved

            }

            return render(request, 'media.html', context)
    
    return render(request, 'edit-post.html', {'user': userobj, 'post': pos})

def save_collab(request):

    if request.method == "POST":
        post_id = request.POST.get("post_id_pass")
        post=postdb.objects.get(pid=post_id)
        post_user=profiledatadb.objects.get(username=post.username)
        base_plan = request.POST.get("base-plan")
        username = request.user.username
        post_name = postdb.objects.get(pid=post_id).caption

        if post_id and base_plan:
            post = get_object_or_404(postdb, pid=post_id)

            # Create collaboration record
            collab = Collab_Information.objects.create(
                base_post_id=post,
                base_plan=base_plan,
                collab_requestor=username
            )
            
            post_owner_user = User.objects.get(username=post_user.username)

            Member_Information.objects.create(
                collaboration=collab,
                post_owner=post_owner_user
            )

            print(f"Collaboration Created: {collab.collaboration_Id}")

            # Send email
            receiver_email = "appus8403@gmail.com" 
            print(post_user.email)
            requester_username = username
            requester_users_name = request.user.first_name
            decision_link = request.build_absolute_uri(reverse("collab_request", args=[collab.collaboration_Id]))
            print(decision_link)
            receiver_username = post_user.firstname
            send_collab_email(receiver_email, receiver_username, requester_username, decision_link, post_name, requester_users_name)

            return JsonResponse({"message": "Collaboration created and email sent successfully."})
        
        return JsonResponse({"error": "Missing post ID or base plan."})

    return JsonResponse({"error": "Invalid request method."})

def send_collab_email(receiver_email, receiver_username, requester_username, decision_link, post_name,requester_users_name):
    subject = "New Collaboration Request"
    print("Initializing automated mail.")
    html_message = f"""
    
      <html>
        <head>
          <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
          <style>
            body {{
              font-family: "Inter", sans-serif;
              font-optical-sizing: auto;
              font-weight: normal;
              font-style: normal;
              font-variation-settings:"slnt" 0;
              font-size:16px;
              color:#3e3e3e;
              background-color:#eee;
            }}
            .main-container{{
              margin:auto;
              padding:20px;
              max-width:80%;
              background-color:#fff
            }}
            #heading{{
              font-size:24px;
              font-weight:600;
              color:#969696;
            }}
            #link_button{{
              padding: 15px 25px; 
              background-color: #000; 
              color: #fff; 
              font-weight:400;
              border-radius:5px;
              text-decoration: none;
              margin:20px 0px;
            }}
            #hr_line{{
              color:#d6d6d6;
              width:75%;
              margin-top:70px;
            }}
          </style>
        </head>
        <body>
        <div class="main-container">
            <br>
                <img src="cid:sounz_logo" alt="Sounz Logo" style="height: 40px;">
            <br><br>
            <h1 id="heading">New Collaboration Request!</h1><br>
            <p>Hello { receiver_username },</p>
            <p><strong>{requester_users_name} (@{requester_username})</strong> would like to collaborate with your post <strong>"{ post_name  }"</strong> by incorporating their ideas. To know more details, approve or reject this request, click the review button below.
            </p><br><br>
            <a id="link_button" href="{decision_link}">Review Collaboration</a><br><br><br>
            <p>The Sounz Team</p>
            <hr id="hr_line">
            <div style="text-align: center;">
                <img src="cid:sounz_footer" alt="Sounz Footer" style="height: 30px; margin:20px 0;">
                <p style="font-size: 12px; color: #a6a6a6;">Create, Collaborate, Connect</p>
            </div>
          </div>
      </body>
      </html>
 
    """
    print("Contents fetched.")
    # Create EmailMessage object
    def send_email():
        email = EmailMessage(subject, html_message, "sounz@gmail.com", [receiver_email])
        email.content_subtype = "html"
        print("Contents inserted.")
        # Attach logo and footer as CID
        with open("static/images/main_mail_logo.png", "rb") as logo:
            logo_image = MIMEImage(logo.read(), _subtype="png")
            logo_image.add_header("Content-ID", "<sounz_logo>")
            logo_image.add_header("Content-Disposition", "inline")
            email.attach(logo_image)
        
        with open("static/images/main_footer_logo.png", "rb") as footer:
            footer_image = MIMEImage(footer.read(), _subtype="png")
            footer_image.add_header("Content-ID", "<sounz_footer>")
            footer_image.add_header("Content-Disposition", "inline")
            email.attach(footer_image)
        print("All files attached.") 
        # Send email
        email.send()
    email_thread = threading.Thread(target=send_email)
    email_thread.start()
    print("Mail Sent!") 

def collaboration_request(request, collab_id):
    collab = get_object_or_404(Collab_Information, collaboration_Id=collab_id)
    post_name = postdb.objects.get(pid=collab.base_post_id.pid).caption
    requestor = profiledatadb.objects.get(username=collab.collab_requestor).firstname
    if profiledatadb.objects.get(username=collab.collab_requestor).firstname:
        requestor_l = profiledatadb.objects.get(username=collab.collab_requestor).lastname
        requestor = requestor + " " +requestor_l
    context = {
        "post_name": post_name,
        "base_plan": collab.base_plan,
        "requestor": requestor,
        "requestor_usern": collab.collab_requestor,
        "request_date": collab.timestamp.strftime("%B %d, %Y"),
        "status": collab.request_status,
        "collaboration_id": collab.collaboration_Id,
    }
    return render(request, "collab-request-review.html", context)

@csrf_exempt
def update_collab_status(request, collab_id):
    collab_id = str(collab_id).replace("-", "")
    try:
        data = json.loads(request.body)
        decision = data.get("decision")
        collab = Collab_Information.objects.get(collaboration_Id=collab_id)
        print("data fetched")
        collab.request_status = decision
        collab.save()
        print("collab status updated")

        reciever_data = profiledatadb.objects.get(username = collab.collab_requestor)
        reciever_mail = "appus8403@gmail.com"
        print(reciever_data.email)
        reciever_name = reciever_data.firstname
        post_name = postdb.objects.get(pid=collab.base_post_id.pid).caption
        send_decision_email(reciever_mail,reciever_name,post_name,decision)
    except Collab_Information.DoesNotExist:
        print("Collab does not exist")
    return JsonResponse({"message": "Status Updated."})

def send_decision_email(receiver_email, receiver_username, post_name,decision):
    subject = "Collaboration request accepted!" if decision == "accepted" else f"Collaboration Request Update for '{post_name}'"
    print("Initializing automated mail.")
    html_message = f"""
    
      <html>
        <head>
          <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
          <style>
            body {{
              font-family: "Inter", sans-serif;
              font-optical-sizing: auto;
              font-weight: normal;
              font-style: normal;
              font-variation-settings:"slnt" 0;
              font-size:16px;
              color:#3e3e3e;
              background-color:#eee;
            }}
            .main-container{{
              margin:auto;
              padding:20px;
              max-width:80%;
              background-color:#fff
            }}
            #heading{{
              font-size:24px;
              font-weight:600;
              color:#969696;
            }}
            #link_button{{
              padding: 15px 25px; 
              background-color: #000; 
              color: #fff; 
              font-weight:400;
              border-radius:5px;
              text-decoration: none;
              margin:20px 0px;
            }}
            #hr_line{{
              color:#d6d6d6;
              width:75%;
              margin-top:70px;
            }}
          </style>
        </head>
        <body>
        <div class="main-container">
            <br>
                <img src="cid:sounz_logo" alt="Sounz Logo" style="height: 40px;">
            <br><br>
            <h1 id="heading">{"Collaboration Accepted!" if decision == "accepted" else "Collaboration Request Update"}</h1><br>
            <p>Hello { receiver_username },</p>
            <p>We wanted to inform you that your collaboration request for the post titled <strong>"{post_name}"</strong> has been reviewed.</p>
            { "🎉 Congratulations! The post owner has accepted your request. You can now proceed with the collaboration in the collaborations tab." 
             if decision == "accepted" 
             else "Unfortunately, the post owner has declined the request. Feel free to explore other projects and collaborations." }

            <p>The Sounz Team</p>
            <hr id="hr_line">
            <div style="text-align: center;">
                <img src="cid:sounz_footer" alt="Sounz Footer" style="height: 30px; margin:20px 0;">
                <p style="font-size: 12px; color: #a6a6a6;">Create, Collaborate, Connect</p>
            </div>
          </div>
      </body>
      </html>
 
    """
    print("Contents fetched.")
    # Create EmailMessage object
    def send_email():
        email = EmailMessage(subject, html_message, "sounz@gmail.com", [receiver_email])
        email.content_subtype = "html"
        print("Contents inserted.")
        # Attach logo and footer as CID
        with open("static/images/main_mail_logo.png", "rb") as logo:
            logo_image = MIMEImage(logo.read(), _subtype="png")
            logo_image.add_header("Content-ID", "<sounz_logo>")
            logo_image.add_header("Content-Disposition", "inline")
            email.attach(logo_image)
        
        with open("static/images/main_footer_logo.png", "rb") as footer:
            footer_image = MIMEImage(footer.read(), _subtype="png")
            footer_image.add_header("Content-ID", "<sounz_footer>")
            footer_image.add_header("Content-Disposition", "inline")
            email.attach(footer_image)
        print("All files attached.") 
        # Send email
        email.send()
    email_thread = threading.Thread(target=send_email)
    email_thread.start()
    print("Mail Sent!") 