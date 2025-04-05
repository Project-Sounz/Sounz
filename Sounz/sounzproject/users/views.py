from django.shortcuts import render,redirect, get_object_or_404
import os
from .models import * 
from django.conf import settings
from django.http import Http404
from django.http import HttpResponseRedirect
from .forms import RegistrationForm,EditProfileForm,Uploadform
from django.core.exceptions import ValidationError
from users.models import profiledatadb,postdb,Collab_Information_tabledb, Member_Information
from django.contrib.auth import authenticate,login,logout
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from .utils import compare_audio
from django.utils.timezone import now
import threading
from django.urls import reverse
from django.db.models import Count

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
                    print("user created")
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
        collabedPostIds = collaborators_table.objects.filter(collab_members=request.user).values_list("post_id", flat=True)
        collabedPosts = postdb.objects.filter(pid__in=collabedPostIds)
        allPosts = post.union(collabedPosts).order_by('-timestamp')
        collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
            collaboration__collab_end=False,
            collaboration__request_status="accepted"
        )
        combined_collab_list = [member.collaboration for member in collab_member_list]
        follower_users = userBioCollect.followers.all()
        follower_profiles = profiledatadb.objects.filter(username__in=[user.username for user in follower_users])
        context = {
            'user': userBioCollect,
            'post': allPosts,
            'saved': savedposts,
            'collab_list': combined_collab_list,
            'follower_profiles': follower_profiles
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
        post = postdb.objects.filter(username=pname,is_private=0,flagged=0)
        collab_pid = collaborators_table.objects.filter(collab_members = User.objects.get(username=pname)).values_list("post_id",flat=True)
        collab_list = postdb.objects.filter(pid__in = collab_pid)
        allPosts = post.union(collab_list).order_by('-timestamp')

        is_following = pname.followers.filter(id=request.user.id).exists()

        context = {
            'pname': pname,
            'user': userBioCollect,
            'posters': allPosts,
            'is_following': is_following,
        }
        return render(request, 'profile-tpv.html', context)

    except profiledatadb.DoesNotExist:
        return render(request, '404.html', status=404)


@login_required
def homepage(request):
    # Get current user profile
    user_profile = profiledatadb.objects.get(username=request.user.username)

    # Get the users that the current user follows (reverse ManyToMany lookup)
    following_users = profiledatadb.objects.filter(followers=request.user)

    # Fetch posts from the followed users
    following_posts = postdb.objects.filter(username__in=following_users, flagged=0, is_private=0).order_by('-timestamp')

    # Fill up to 15 posts with random posts if needed
    num_needed = 15 - following_posts.count()
    num_needed = max(0, num_needed)
    
    random_posts = postdb.objects.filter(flagged=0, is_private=0).exclude(username__in=following_users).order_by('?')[:num_needed]

    # Suggested profiles (excluding the current user and followed users)
    suggested_profiles = profiledatadb.objects.exclude(username=user_profile).exclude(username__in=following_users).order_by('?')[:6]
    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
            collaboration__collab_end=False,
            collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]
    context = {
        'user': user_profile,
        'following_posts': following_posts,  # Posts from followed users
        'random_posts': random_posts,  # Filler random posts
        'suggested_profiles': suggested_profiles,
        'collab_list': combined_collab_list,
    }
    return render(request, 'home.html', context)

def upload(request):
    username = request.user.username
    userobj = profiledatadb.objects.get(username=username)

    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
    collaboration__collab_end=False,
    collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]   
    context = {
            "user": userobj,
            'collab_list': combined_collab_list,
        }
    if request.method == 'POST':
        caption = request.POST.get('title')
        desc = request.POST.get('post_description')
        typ = request.POST.get('tags')
        media_type = request.POST.get('media_type')
        lan = request.POST.get('language')
        loc = request.POST.get('location')
        is_private = request.POST.get('media_visibility_private') == 'on'
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
            return redirect('my-profile')

    return render(request, 'upload_form.html', context)


def editprofile(request):

        username=request.user.username
        user = profiledatadb.objects.get(username=username)
        userauth=User.objects.get(username=username)
    
        collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
        collaboration__collab_end=False,
        collaboration__request_status="accepted"
        )
        combined_collab_list = [member.collaboration for member in collab_member_list]   
        context = {
            "user": user,
            'collab_list': combined_collab_list,
        }



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
                if request.POST.get('youtube'):   
                   user.yout = request.POST.get('youtube')
                if request.POST.get('xcom'):   
                   user.twit = request.POST.get('xcom')        
                user.save()
                userauth.save()
                
                return redirect('my-profile')



        else:
            form = EditProfileForm(instance=user)
        return render(request,'editprofile.html',context) 

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

            print(f"Received post_id: {post_id}")  # Debugging Log

            # Fetch the post
            post = get_object_or_404(postdb, pid=post_id)
            print(f"Post Found: {post.caption} by {post.username.username}")  # Debugging Log

            # Get the current user
            user = request.user
            print(f"Current User: {user.username}")  # Debugging Log

            # Get the post owner (Convert profiledatadb → User)
            try:
                post_owner = User.objects.get(username=post.username.username)  
                print(f"Post Owner Found: {post_owner.username}")  # Debugging Log
            except User.DoesNotExist:
                print(f"Error: User not found for post {post_id}")
                return JsonResponse({'success': False, 'error': 'Post owner not found'})

            # Check if the user has already liked the post
            like, created = Like.objects.get_or_create(user=user, post=post)

            if created:
                # User liked the post
                liked = True
                post.likes += 1
                print(f"Like Added! New Count: {post.likes}")  # Debugging Log

                # Ensure the user is not liking their own post
                if user != post_owner:
                    Notification.objects.create(
                        recipient=post_owner,  # FIX: Now using the correct User instance
                        sender=user,
                        post=post,
                        notification_type="like",
                        message=f"{user.username} killed your post: {post.caption}"
                    )
                    print(f"Notification Created: {user.username} → {post_owner.username}")  # Debugging Log

            else:
                # User unliked the post (delete the like)
                like.delete()
                liked = False
                post.likes = max(0, post.likes - 1)  # Prevents negative values
                print(f"Like Removed! New Count: {post.likes}")  # Debugging Log

                # Delete like notification when unliking
                Notification.objects.filter(
                    recipient=post_owner,  # FIX: Now using the correct User instance
                    sender=user,
                    post=post,
                    notification_type="like"
                ).delete()
                print(f"Notification Deleted: {user.username} → {post_owner.username}")  # Debugging Log

            # Save the updated post like count
            post.save()

            return JsonResponse({
                'success': True,
                'liked': liked,
                'like_count': post.likes
            })

        except Exception as e:
            print(f"Error in toggle_like: {e}")  # Debugging log
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@login_required
def notifications(request):
    """ Display all notifications for the logged-in user """
    username = request.user.username
    userobj = profiledatadb.objects.get(username=username)

    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
    collaboration__collab_end=False,
    collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]   
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    reported_posts = {notif.post for notif in user_notifications if notif.post}

    if hasattr(Notification, 'status'):
        user_notifications.update(status="read")
    context = {
            "user": userobj,
            'collab_list': combined_collab_list,
            'notifications': user_notifications,
            'reported_posts': reported_posts
        }
    return render(request, 'notifications.html', context)



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
    randomPost=postdb.objects.exclude(pid=pid).exclude(username=username)
    random_post = random.sample(list(randomPost), min(len(randomPost), 5))
    allCollabMembers=[]
    if(post.isCollaborated):
        each_member = collaborators_table.objects.filter(post_id=pid).values_list('collab_members', flat=True)
        allCollabMembers = profiledatadb.objects.filter(username__in=User.objects.filter(id__in=each_member).values_list('username', flat=True))

    # Get the next post (loops back to first if at the end)
    next_post = post_list[post_index + 1] if post_index is not None and post_index + 1 < len(post_list) else None

# Get the previous post (loops back to last if at the beginning)
    previous_post = post_list[post_index - 1] if post_index is not None and post_index > 0 else None
    user_liked = Like.objects.filter(user=request.user, post=post).exists()
    user_saved = Save.objects.filter(user=request.user, post=post).exists()

    ps = post.username
    puser = profiledatadb.objects.get(username=ps)
    
    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
        collaboration__collab_end=False,
        collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]   
    context = {
        "puser": puser,
        "post": post,
        "user": user,
        "user_liked": user_liked,
        "user_saved": user_saved,
        "next_post": next_post,
        "previous_post": previous_post,
        'collab_list': combined_collab_list,
        'collab_members': allCollabMembers,
        "random_post": random_post,
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
            ).filter(flagged=0,is_private=0)   
            search_profiles = profiledatadb.objects.filter(
                Q(username=input_value) | Q(firstname__icontains=input_value) | Q(lastname__icontains=input_value)
            )

            random_posts = postdb.objects.all().exclude(username=request.user.username).order_by('-timestamp')   
            all_users = profiledatadb.objects.all()
            username = request.user.username
            user = profiledatadb.objects.get(username=username)
            top_posts = postdb.objects.filter(is_private=False).order_by('-likes')[:4]
            top_profiles = profiledatadb.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')[:4]

            context = {
            'all_users': all_users,
            'user': user,
            'top_posts':top_posts,
            'result_posts': posts,
            'topart':top_profiles,
            'search_profiles': search_profiles,
            'search_value': input_value,
            'random_posts': random_posts,
            }
            return render(request,'search.html',context)

    random_posts = postdb.objects.all().exclude(username=request.user.username).order_by('-timestamp')
    all_users = profiledatadb.objects.all()
    username = request.user.username
    user = profiledatadb.objects.get(username=username)
    top_profiles = profiledatadb.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')[:4]
    # Fetch posts of the current user
    
    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
        collaboration__collab_end=False,
        collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]    
    user_posts = postdb.objects.filter(is_private=False).order_by('-likes')[:4]
    context = {
        'all_users': all_users,
        'user': user,
        'top_posts': user_posts,
        'topart':top_profiles,
        'collab_list': combined_collab_list,
        'random_posts': random_posts,
    }

    return render(request,'search.html',context)


def editpost(request):
    username = request.user.username
    userobj = profiledatadb.objects.get(username=username)
    post_id = request.GET.get('post_id')

    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
        collaboration__collab_end=False,
        collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]
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
        
        form = Uploadform(request.POST, request.FILES, instance=pos)  # Pre-fill form

        if form.is_valid():
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
                "user_saved": user_saved,
                'collab_list': combined_collab_list,
            }
            return render(request, 'media.html', context)

    else:
        # Pre-fill the form with existing post details
        form = Uploadform(instance=pos)

    return render(request, 'edit-post.html', {'user': userobj, 'post': pos, 'form': form})

def save_collab(request):
    owners_count=1
    if request.method == "POST":
        post_id = request.POST.get("post_id_pass")
        post=postdb.objects.get(pid=post_id)
        post_user=profiledatadb.objects.get(username=post.username)
        print("Response:post and user fetched")
        base_plan = request.POST.get("base-plan")
        print("Response:base plan fetched")
        cUsername = request.user
        print("Response:Username fetched")
        post_name = postdb.objects.get(pid=post_id).caption
        print("Response:postname fetched")
        if (post.isCollaborated):
            collab_owners = collaborators_table.objects.filter(post_id=post_id)
            collab_owners_user = User.objects.filter(id__in=collab_owners.values_list('collab_members', flat=True))
            print("Response:collab owners:", collab_owners)
            collab_members_list = list(collab_owners.values_list('collab_members__username', flat=True))
            print("Response: collab member list:", collab_members_list)
            collab_owners_mails = profiledatadb.objects.filter(username__in=collab_members_list)
            print("Response: collab owner mails:", collab_owners_mails)
            owners_count += len(collab_owners_user)
        else:
            owners_count += 1
        print("Post collaborated: ",post.isCollaborated)
        print("owner_count:",owners_count)
        print("Response:everything fetched")
        if post_id and base_plan:
            collab = Collab_Information_tabledb.objects.create(
                base_post_id=post,
                base_plan=base_plan,
                collab_requestor=cUsername,
                owner_count=owners_count,
            )
            print("collab id created:",collab)
            post_member_user = User.objects.get(username=post_user.username)
            print(post_member_user)
            # Add only if the user does not already exist
            Member_Information.objects.create(
                collaboration=collab,
                post_member=post_member_user,
                isOwner=True
            )
            print("Member info: post owner added")
            Member_Information.objects.create(
                collaboration=collab,
                post_member=request.user,
                isOwner=False
            )
            print("Member info: post current user added")
            if (post.isCollaborated):
                member_objects = []
                for each_owner in collab_owners_user:
                    # Prevent duplicates
                    if not Member_Information.objects.filter(collaboration=collab, post_member=each_owner).exists():
                        member_objects.append(
                            Member_Information(collaboration=collab, post_member=each_owner, isOwner=False)
                        )

                if member_objects:
                    Member_Information.objects.bulk_create(member_objects)
                    print("Member info: collaborators added")

            print(f"Collaboration Created: {collab.collaboration_Id}")

            receivers = [[post_user.email,post_user.username]]    
            if(post.isCollaborated):
                for each_email in collab_owners_mails:
                    receivers.append([each_email.email,each_email.firstname])
            # Send email
            print(post_user.email)
            print(receivers)
            requester_username = cUsername
            requester_users_name = request.user.first_name
            decision_link = request.build_absolute_uri(reverse("collab_request", args=[collab.collaboration_Id]))
            print(decision_link)
            for receiver in receivers:
                send_collab_email(receiver[0], receiver[1], requester_username, decision_link, post_name, requester_users_name)

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
    collab = get_object_or_404(Collab_Information_tabledb, collaboration_Id=collab_id)
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
        collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)
        print("data fetched")
        collab.request_status = decision
        collab.save()
        print("collab status updated")

        reciever_data = profiledatadb.objects.get(username = collab.collab_requestor)
        reciever_mail = reciever_data.email                                        
        print(reciever_data.email)
        reciever_name = reciever_data.firstname
        post_name = postdb.objects.get(pid=collab.base_post_id.pid).caption
        send_decision_email(reciever_mail,reciever_name,post_name,decision)
    except Collab_Information_tabledb.DoesNotExist:
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

def collab_workspace(request):
    username = request.user.username
    userobj = profiledatadb.objects.get(username=username)

    collab_member_list = Member_Information.objects.filter(post_member=request.user).select_related('collaboration').filter(
    collaboration__collab_end=False,
    collaboration__request_status="accepted"
    )
    combined_collab_list = [member.collaboration for member in collab_member_list]   
    collab_Id = request.GET.get('collab-id')
    if not collab_Id:
        return JsonResponse({'error': 'Missing collab-id'}, status=400) 
    print("collab Id:",collab_Id)
    try:
        collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_Id)
        collab_base_owners = Member_Information.objects.filter(collaboration_id=collab_Id)
        base_post = postdb.objects.get(pid=collab.base_post_id.pid)
        collaborator_images = [
        profiledatadb.objects.get(username=member.post_member).profile_picture.url
        for member in collab_base_owners if profiledatadb.objects.filter(username=member.post_member).exists()
    ]

        # collaborator_profiles = profiledatadb.objects.get()for user in collab_base_owners
    except Collab_Information_tabledb.DoesNotExist:
        return JsonResponse({'error': 'Collaboration not found'}, status=404)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        sync_audio_list = syncAudios_table.objects.filter(collaboration_id=collab_Id)
        audio_data = list(sync_audio_list.values("syncId", "timestamp", "syncMedia","syncedBy__username","audioName"))

        return JsonResponse({'audio_list': audio_data})

    context = {
        'collab': collab,
        'post_members': collab_base_owners,
        'post_base': base_post,
        'collab_id': collab_Id,
        'collaborator_images': collaborator_images,
        'user_id':request.user.username,
        "user": userobj,
        'collab_list': combined_collab_list,
    }
    return render(request, "collab.html", context)

@csrf_exempt
def upload_sync_audio(request):
    if request.method == "POST":
        if "syncMedia" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        if "syncMedia" in request.FILES:
            file = request.FILES["syncMedia"]
            print("Uploaded file size:", file.size)
        file = request.FILES["syncMedia"]
        collab_id = request.POST.get("collaboration_id")
        user = request.user
        if not collab_id:
            return JsonResponse({"error": "Missing collaboration ID"}, status=400)

        try:
            collaboration = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)
            instance = syncAudios_table(collaboration=collaboration, syncMedia=file, syncedBy = user)
            instance.save()
            
            return JsonResponse({"message": "File uploaded successfully!", "file_url": instance.syncMedia.url})

        except Collab_Information_tabledb.DoesNotExist:
            return JsonResponse({"error": "Invalid collaboration ID"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_protect 
@require_http_methods(["DELETE"])
def delete_audio(request):
    if request.method == "DELETE":
        syncId = request.GET.get('syncId')
        print(syncId)
        fetchedAudio = syncAudios_table.objects.get(syncId = syncId)
        file_path = os.path.join(settings.MEDIA_ROOT, str(fetchedAudio.syncMedia))
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}") 
        fetchedAudio.delete()
    return JsonResponse({"success": True})  

@login_required
@csrf_exempt  # Remove this if you handle CSRF properly
def send_chat_message(request, collab_id):
    if request.method == "POST":
        collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)
        data = json.loads(request.body)
        message = data.get("message")
        
        if message:
            collab.add_message(request.user.username, message)
            return JsonResponse({"status": "success", "message": message})

    return JsonResponse({"status": "error"}, status=400)

def get_chat_history(request, collab_id):
    """Fetch chat history along with user profile details, supporting incremental loading."""
    collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)
    chat_history = collab.chat_history

    # Get last loaded message ID from the request
    last_id = int(request.GET.get("last_id", 0))

    chat_data = []
    
    for i, chat in enumerate(chat_history):
        chat_id = i + 1  # Assign a unique ID based on index (since JSONField lacks DB IDs)

        if chat_id > last_id:  # Fetch only messages that are newly added
            username = chat.get("username", "")
            message = chat.get("message", "")

            # Fetch user profile details
            try:
                user_profile = profiledatadb.objects.get(username=username)
                profile_pic = user_profile.profile_picture.url if user_profile.profile_picture else "/static/default_profile.png"
            except profiledatadb.DoesNotExist:
                profile_pic = "/static/default_profile.png"  # Default pic if profile not found

            chat_data.append({
                "id": chat_id,  # Attach a unique ID for tracking
                "username": username,
                "message": message,
                "profile_pic": profile_pic
            })

    return JsonResponse({"chat_history": chat_data})



@require_http_methods(["PATCH"])
def approve_button(request):
    status = request.GET.get('status')
    collab_id = request.GET.get('cId')
    if not collab_id or not status:
        return JsonResponse({"error": "Missing required parameters"}, status=400)
    try:
        collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id) 
    except Collab_Information_tabledb.DoesNotExist:
        return JsonResponse({"error": "Invalid collaboration ID"}, status=404)

    try:
        memIn = Member_Information.objects.get(post_member=request.user, collaboration=collab)
        print(memIn.isApproved)
    except Member_Information.DoesNotExist:
        return JsonResponse({"error": "Member not found"}, status=404)

    if status == "approve":
        collab.accept_count = collab.accept_count+1
        memIn.isApproved = True
        print(collab.accept_count)
    elif status == "revoke":
        collab.accept_count = collab.accept_count-1
        memIn.isApproved = False
        print(collab.accept_count)
    else:
        return JsonResponse({"error": "Invalid status"}, status=400)

    collab.save()
    memIn.save()

    return JsonResponse({"message": f"Collaboration {status}d!"})

def get_approval_status(request):
    collab_id = request.GET.get("cId")
    print("Collab id: ",collab_id)
    collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)
    print("collab end?:",collab.collab_end)
    if (collab.request_status=="terminated"):
        print("collab terminated!")
        return JsonResponse({"redirect": "/home"})
    if (collab.collab_end==True):
        return redirect(f"/media?pid={collab.endPost.pid}")
    try:
        isApprove=Member_Information.objects.get(post_member_id=request.user,collaboration=collab_id).isApproved
        print(isApprove)
        return JsonResponse({
            "accept_count": collab.accept_count,
            "owner_count": collab.owner_count,
            "isApproved" : isApprove
        })
    except Collab_Information_tabledb.DoesNotExist:
        return JsonResponse({"error": "Collaboration not found"}, status=404)
   
    

def get_audio_files(request):
    collab_id = request.GET.get('collabId')

    if not collab_id:
        return JsonResponse({"error": "Missing collaboration ID"}, status=400)

    try:
        collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)  # Fetch collaboration info
        print(collab)

        # Get base audio file URL
        base_audio_url = request.build_absolute_uri(collab.base_post_id.media.url)
        print(base_audio_url)

        # Get synced audio files (ensure absolute URLs)
        synced_audio_files = syncAudios_table.objects.filter(collaboration=collab).values_list('syncMedia', flat=True)
        print(synced_audio_files)

        user_audio_urls = [request.build_absolute_uri(settings.MEDIA_URL + str(audio)) for audio in synced_audio_files]

        return JsonResponse({
            "base_audio": base_audio_url,
            "audio_urls": user_audio_urls
        })

    except Collab_Information_tabledb.DoesNotExist:
        return JsonResponse({"error": "Collaboration not found"}, status=404)
@csrf_exempt
def upload_mixed_audio(request):
    if request.method == "POST":
        collab_id = request.POST.get("collaboration_id")
        audio_file = request.FILES.get("mixed_audio")
        
        if not collab_id or not audio_file:
            return JsonResponse({"error": "Missing data"}, status=400)

        try:
            collab = Collab_Information_tabledb.objects.get(collaboration_Id=collab_id)
            print("collab:", collab)
            collaboratedMembers = Member_Information.objects.filter(collaboration=collab)
            print("collaborated members:", collaboratedMembers)
            username=Member_Information.objects.get(collaboration=collab,isOwner=True).post_member
            print("Post owner:", username)
            userobj = profiledatadb.objects.get(username=username)
            thumbnail = collab.temp_thumbnail if collab.temp_thumbnail else None
            caption = collab.temp_caption if collab.temp_caption else collab.collaboration_title
            collab_members = Member_Information.objects.filter(collaboration=collab, isOwner=False).values_list('post_member__first_name', flat=True)
            print("collab_members: ",collab_members)
            base_post_caption = Collab_Information_tabledb.objects.get(collaboration_Id=collab.collaboration_Id).base_post_id.caption

            description = (
                collab.temp_descr 
                if collab.temp_descr 
                else f"A collaboration with {username} ft. {', '.join(collab_members)} on {base_post_caption}"
            )
            mType = collab.temp_mediaType if collab.temp_mediaType else ""
            profile_instance = profiledatadb.objects.get(username=username.username)
            print("full data fetched")
            thePost = postdb.objects.create(
                # username=userobj,
                username = profile_instance,
                media=audio_file,
                media_thumbnail=thumbnail,
                # caption="test Caption",
                caption=caption,
                # descr="test description",
                descr=description,
                # mediatype="Violin Test",
                mediatype=mType,
                location="India",
                media_format="Audio",
                isCollaborated = True,
                collaboration=collab.collaboration_Id
            )
            print("post uploaded")
            for member in collaboratedMembers:
                collaborators_table.objects.create(
                    post_id=thePost,
                    collab_members=member.post_member
                )
            delete_sync_audios(collab_id)
            print("sync files deleted")
            collab.collab_end=True
            collab.endPost=thePost
            collab.save()
            print("collab ended")
            print(collab.collab_end)
            print(f"location: /media?pid={thePost.pid}")
            return JsonResponse({"redirect": f"/media?pid={thePost.pid}"})

        except Collab_Information_tabledb.DoesNotExist:
            return JsonResponse({"error": "Collaboration not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)

def delete_sync_audios(collab_id):
    audios = syncAudios_table.objects.filter(collaboration_id=collab_id)
    
    for audio in audios:
        file_path = os.path.join(settings.MEDIA_ROOT, str(audio.syncMedia))
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}") 
    audios.delete()
    print("Database entries deleted.")

def end_collab(request):
    if request.method == "DELETE":
        collabId = request.GET.get('collabId')
        print(collabId)
        theCollab = Collab_Information_tabledb.objects.get(collaboration_Id=collabId)
        theCollab.request_status="terminated"
        theCollab.save()
        return JsonResponse({"redirect_url": reverse('home')})
    
def update_collab_post(request):
    if request.method == "POST":
        collab_id = request.POST.get("collabId")  # Ensure this ID is available in your form
        caption = request.POST.get("caption")
        media_type = request.POST.get("mType")
        description = request.POST.get("description")
        thumbnail = request.FILES.get("post_picture")

        # Fetch the collab instance and update fields
        collab = get_object_or_404(Collab_Information_tabledb, collaboration_Id=collab_id)
        if caption:
            collab.temp_caption = caption
            collab.collaboration_title = caption
        if media_type:
            collab.temp_mediaType = media_type
        if description:
            collab.temp_descr = description
        if thumbnail:
            collab.temp_thumbnail = thumbnail

        collab.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

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

    print(f"Comparing User Post {user_post_id} with Reported Post {reported_post_id}")

    # Compare the two posts
    result = compare_audio(user_post.media.path, reported_post.media.path)

    if result:
        reported_timestamp = reported_post.timestamp
        user_timestamp = user_post.timestamp
        print(f"User Post Timestamp: {user_timestamp}, Reported Post Timestamp: {reported_timestamp}")

        if reported_timestamp > user_timestamp:
            print(f"Flagging Reported Post ID: {reported_post_id}")
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
                print("Notification created successfully.")
            except Exception as e:
                print(f"Error creating notification: {e}")

            return JsonResponse({
                "match": True,
                "flagged": True,
                "message": "Copyright violation detected! The post will be flagged."
            })

        return JsonResponse({
            "match": True,
            "flagged": False,
            "message": "Match found, but original post is newer."
        })

    return JsonResponse({
        "match": False,
        "flagged": False,
        "message": "No copyright violation detected. No actions will be taken!"
    })


@login_required
def get_user_posts(request):
    """Fetch all posts by the logged-in user for copyright reporting."""
    user_posts = postdb.objects.filter(username=request.user.username,flagged=0).values("pid", "caption", "timestamp")

    # Debugging log
    print(f"Fetching posts for user: {request.user.username}")
    print(f"User Posts: {list(user_posts)}")

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
    
def fetch_temp_data(request):
    collab_Id = request.GET.get('collabId')
    temp_data = Collab_Information_tabledb.objects.get(collaboration_Id=collab_Id)
    data = {
        'temp_thumbnail': temp_data.temp_thumbnail.url if temp_data.temp_thumbnail else None,
        'temp_caption': temp_data.temp_caption,
        'temp_descr': temp_data.temp_descr,
        'temp_mediaType': temp_data.temp_mediaType,
    }
    return JsonResponse(data)