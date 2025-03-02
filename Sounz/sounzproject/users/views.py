from django.shortcuts import render,redirect, get_object_or_404
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
import os
# from .utils import compare_audio
from django.utils.timezone import now

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
    try:
        current_user = request.user.username
        uname = request.GET.get('uname')

        if uname == current_user:
            return redirect('my-profile')

        pname = profiledatadb.objects.get(username=uname)
        userBioCollect = profiledatadb.objects.get(username=current_user)
        post = postdb.objects.filter(username=pname)

        # Correct way to check if the user is a follower
        is_following = pname.followers.filter(id=request.user.id).exists()

        context = {
            'pname': pname,
            'user': userBioCollect,
            'posters': post,
            'is_following': is_following,  # Pass this correctly
        }
        return render(request, 'profile-tpv.html', context)

    except profiledatadb.DoesNotExist:
        return render(request, '404.html', status=404)


def homepage(request):
    all_users = profiledatadb.objects.all()
    username = request.user.username
    user = profiledatadb.objects.get(username=username)
    sliced= profiledatadb.objects.all()[:4]
    topart=profiledatadb.objects.all()
    random_profiles = random.sample(list(topart), min(len(topart), 4))
    # Fetch posts of the current user
    user_posts = postdb.objects.filter(flagged=0).order_by('-timestamp')
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
        is_private = request.POST.get('media_visibility_control') == 'on'
        form = Uploadform(request.POST, request.GET)

        if form.is_valid(): 
            file = request.FILES.get('post')
            gotthumbnail = request.FILES.get('thumbnail')

            # Validate file type
            if file and not file.content_type.startswith(('video/', 'audio/')):
                prompt_message = "Invalid file type. Only video and audio files are allowed."
                return render(request, 'upload_form.html', {'user': userobj, 'prompt_message': prompt_message})

            pos = postdb(username=userobj, caption=caption, descr=desc, langu=lan, mediatype=typ, location=loc, media=file, media_format=media_type, media_thumbnail=gotthumbnail, is_private=is_private)
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

@login_required
def toggle_like(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')

            print(f"🔍 Received post_id: {post_id}")  # Debugging Log

            # Fetch the post
            post = get_object_or_404(postdb, pid=post_id)
            print(f"✅ Post Found: {post.caption} by {post.username.username}")  # Debugging Log

            # Get the current user
            user = request.user
            print(f"👤 Current User: {user.username}")  # Debugging Log

            # Get the post owner (Convert profiledatadb → User)
            try:
                post_owner = User.objects.get(username=post.username.username)  
                print(f"🎯 Post Owner Found: {post_owner.username}")  # Debugging Log
            except User.DoesNotExist:
                print(f"❌ Error: User not found for post {post_id}")
                return JsonResponse({'success': False, 'error': 'Post owner not found'})

            # Check if the user has already liked the post
            like, created = Like.objects.get_or_create(user=user, post=post)

            if created:
                # User liked the post
                liked = True
                post.likes += 1
                print(f"👍 Like Added! New Count: {post.likes}")  # Debugging Log

                # Ensure the user is not liking their own post
                if user != post_owner:
                    Notification.objects.create(
                        recipient=post_owner,  # FIX: Now using the correct User instance
                        sender=user,
                        post=post,
                        notification_type="like",
                        message=f"{user.username} liked your post: {post.caption}"
                    )
                    print(f"✅ Notification Created: {user.username} → {post_owner.username}")  # Debugging Log

            else:
                # User unliked the post (delete the like)
                like.delete()
                liked = False
                post.likes = max(0, post.likes - 1)  # Prevents negative values
                print(f"👎 Like Removed! New Count: {post.likes}")  # Debugging Log

                # Delete like notification when unliking
                Notification.objects.filter(
                    recipient=post_owner,  # FIX: Now using the correct User instance
                    sender=user,
                    post=post,
                    notification_type="like"
                ).delete()
                print(f"🗑️ Notification Deleted: {user.username} → {post_owner.username}")  # Debugging Log

            # Save the updated post like count
            post.save()

            return JsonResponse({
                'success': True,
                'liked': liked,
                'like_count': post.likes
            })

        except Exception as e:
            print(f"❌ Error in toggle_like: {e}")  # Debugging log
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@login_required
def notifications(request):
    """ Display all notifications for the logged-in user """
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    reported_posts = {notif.post for notif in user_notifications if notif.post}

    # ✅ Only update if the `status` field exists
    if hasattr(Notification, 'status'):
        user_notifications.update(status="read")

    return render(request, 'notifications.html', {'notifications': user_notifications,'reported_posts': reported_posts})



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
    
    post_list = list(postdb.objects.filter(flagged=0).order_by('-timestamp'))
    post_index = next((i for i, p in enumerate(post_list) if p.pid == post.pid), None)
    # Get the next post (loops back to first if at the end)
    next_post = post_list[post_index + 1] if post_index is not None and post_index + 1 < len(post_list) else None

# Get the previous post (loops back to last if at the beginning)
    previous_post = post_list[post_index - 1] if post_index is not None and post_index > 0 else None



    


    
    
    

    user_liked = Like.objects.filter(user=request.user, post=post).exists()
    user_saved = Save.objects.filter(user=request.user, post=post).exists()

    ps = post.username
    puser = profiledatadb.objects.get(username=ps)
    context = {
        "puser": puser,
        "post": post,
        "user": user,
        "user_liked": user_liked,
        "user_saved": user_saved,
        "next_post": next_post,
        "previous_post": previous_post,
        

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
            ).filter(flagged=0)   
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
        is_private = request.POST.get('media_visibility_control') == 'on'
        form = Uploadform(request.POST, request.GET)

        if form.is_valid():
            # Update only the specified post fields
            pos.caption = caption
            pos.descr = desc
            pos.langu = lan
            pos.mediatype = typ
            pos.location = loc
            pos.media_format = media_type
            pos.is_private = is_private
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

#delete post
def delete_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(postdb, pid=post_id)
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
@login_required
def report_copyright(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    reported_post_id = request.GET.get("reported_pid")
    user_post_id = request.GET.get("user_pid")

    if not reported_post_id or not user_post_id:
        return JsonResponse({"error": "Missing post IDs"}, status=400)

    reported_post = get_object_or_404(postdb, pid=reported_post_id)
    user_post = get_object_or_404(postdb, pid=user_post_id)

    print(f"🔍 Comparing User Post {user_post_id} with Reported Post {reported_post_id}")

    # Compare the two posts
    result = compare_audio(user_post.media.path, reported_post.media.path)

    if result:
        reported_timestamp = reported_post.timestamp
        user_timestamp = user_post.timestamp
        print(f"🕒 User Post Timestamp: {user_timestamp}, Reported Post Timestamp: {reported_timestamp}")

        if reported_timestamp > user_timestamp:
            print(f"🚩 Flagging Reported Post ID: {reported_post_id}")
            reported_post.flagged = 1  # Set flagged bit to 1
            reported_post.save()

            try:
                recipient_user = User.objects.get(username=reported_post.username.username) 
                # Create a notification for the flagged post
                Notification.objects.create(
                    recipient=recipient_user,
                    sender=request.user,
                    post=reported_post,
                    message="Your post has been flagged for copyright infringement.",
                    notification_type="flagged",
                    timestamp=now()
                )
                print("✅ Notification created successfully.")
            except Exception as e:
                print(f"⚠️ Error creating notification: {e}")

            return JsonResponse({
                "match": True,
                "flagged": True,
                "message": "✅ Copyright violation detected! The post has been flagged."
            })

        return JsonResponse({
            "match": True,
            "flagged": False,
            "message": "⚠️ Match found, but original post is newer."
        })

    return JsonResponse({
        "match": False,
        "flagged": False,
        "message": "❌ No copyright violation detected."
    })


@login_required
def get_user_posts(request):
    """Fetch all posts by the logged-in user for copyright reporting."""
    user_posts = postdb.objects.filter(username=request.user.username,flagged=0).values("pid", "caption", "timestamp")

    # Debugging log
    print(f"📥 Fetching posts for user: {request.user.username}")
    print(f"📋 User Posts: {list(user_posts)}")

    return JsonResponse({"posts": list(user_posts)})

@csrf_exempt
@login_required
def report_offensive(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    post_id = request.GET.get("post_id")
    if not post_id:
        return JsonResponse({"error": "Missing post ID"}, status=400)

    post = get_object_or_404(postdb, pid=post_id)

    # Check if the user has already reported this post
    if post.reported_users.filter(id=request.user.id).exists():
        return JsonResponse({"error": "You have already reported this post."}, status=400)

    # Increment the flag counter and add user to reported_users
    post.flag_counter += 1
    post.reported_users.add(request.user)

    # Flag the post if it has been reported more than 5 times
    if post.flag_counter >= 5:
        post.flagged = True
        post.save()
        recipient_user = User.objects.get(username=post.username.username) 
        # Create a notification for the flagged post
        Notification.objects.create(
            recipient=recipient_user,  # Ensure `username` links to `User`
            sender=request.user,
            post=post,
            message="Your post has been flagged for offensive/explicit content.",
            notification_type="flagged",
            timestamp=now()
        )
        return JsonResponse({"success": True, "flagged": True, "message": "Post has been flagged for offensive content."})

    post.save()
    return JsonResponse({"success": True, "flagged": False, "message": "Report submitted. "})



@login_required
def toggle_follow(request):
    if request.method == "POST":
        username = request.POST.get("username")
        profile = get_object_or_404(profiledatadb, username=username)

        # Ensure the user is retrieved correctly
        user = request.user

        if profile.followers.filter(id=user.id).exists():
            profile.followers.remove(user)  # Remove follower
            followed = False
        else:
            profile.followers.add(user)  # Add follower
            followed = True
        
        # Save changes explicitly
        profile.save()

        return JsonResponse({"followed": followed, "follower_count": profile.followers.count()})