from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string
from django.utils import timezone



# Create your models here.
class profiledatadb(models.Model):
    username=models.CharField(primary_key=True,max_length=25,unique=True)
    password = models.CharField(max_length=15)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='media/Profiles')
    user_bio=models.TextField()
    phone=models.IntegerField(null=True)
    timestamp=models.DateTimeField(auto_now_add=True,null=True)
    insta=models.URLField(max_length=200,blank=True,null=True)
    yout=models.URLField(max_length=200,blank=True,null=True)
    twit=models.URLField(max_length=200, blank=True,null=True)

    def __str__(self):
        return str(self.username) 

class postdb(models.Model):
    pid=models.UUIDField(primary_key=True,max_length=10,default=uuid.uuid4)
    username=models.ForeignKey(to=profiledatadb,on_delete=models.CASCADE)
    media=models.FileField(upload_to='media/Posts')
    media_thumbnail=models.FileField(upload_to='media/Thumbnails',default=None,blank=True,null=True)
    caption=models.CharField(max_length=30)
    descr=models.TextField()
    langu=models.CharField(max_length=15,default="English")
    mediatype=models.CharField(max_length=15)
    location=models.CharField(max_length=15)
    likes=models.IntegerField(default=0)
    media_format=models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    collaborated_owners = models.ManyToManyField(User, through="collaborators")
    isCollaborated = models.BooleanField(default=False)
    collaboration = models.UUIDField(default=None,blank=True,null=True)
    
    def __str__(self):
        return str(self.pid)
    
class collaborators(models.Model):
    post_id = models.ForeignKey(postdb, on_delete=models.CASCADE)
    collab_members = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post_id', 'collab_members')

    def __str__(self):
        return f"{self.collab_members.username} in {self.post_id.caption}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(postdb, on_delete=models.CASCADE, related_name='likes_relation')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ( 'user', 'post' )

    def __str__(self):
        return f"{self.user.username} liked {self.post.pid}"

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(postdb, on_delete=models.CASCADE, related_name='save_relation')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ( 'user', 'post' )

    def __str__(self):
        return f"{self.user.username} saved {self.post.pid}"

class saveddb(models.Model):
    username=models.ForeignKey(to=profiledatadb,on_delete=models.CASCADE)
    pid=models.ForeignKey(to=postdb,on_delete=models.CASCADE)

# class postdatabase(models.Model):
#     username=models.ForeignKey(to=profiledatadb,on_delete=models.CASCADE,default=0)
#     media_address = models.CharField(max_length=256)
#     likes_count = models.IntegerField(default=0)
#     tags = models.CharField(max_length=32, null=True)
#     media_type = models.CharField(max_length=20)
#     title = models.CharField(max_length=200)
#     descr = models.TextField()
#     lang = models.CharField(max_length=15)
#     timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pid)     
    
class Collab_Information(models.Model):
    collaboration_Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_post_id = models.ForeignKey(postdb, on_delete=models.CASCADE, related_name="collab_base_posts")
    request_status = models.CharField(max_length=20, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)
    collaboration_title = models.CharField(max_length=50, default="Untitled collaboration test")
    collaborated_members = models.ManyToManyField(User, through="Member_Information")
    base_plan = models.CharField(max_length=200,default=None)
    collab_requestor = models.CharField(max_length=25,default=None)
    collab_end = models.BooleanField(default=False)
    owner_count = models.IntegerField(default=1)
    accept_count = models.IntegerField(default=0)
    endPost = models.ForeignKey(postdb, on_delete=models.CASCADE,null=True, related_name="collab_end_posts")
    temp_thumbnail = models.FileField(upload_to='media/Thumbnails',default=None,blank=True,null=True)
    temp_caption = models.CharField(max_length=30,default=None,blank=True,null=True)
    temp_descr = models.TextField(default=None,blank=True,null=True)
    temp_mediaType = models.CharField(max_length=15,default=None,blank=True,null=True)
    chat_history = models.JSONField(default=list)  

    def add_message(self, username, message):
        """ Append a new message to chat history and save """
        self.chat_history.append({"username": username, "message": message})
        self.save()

    def __str__(self):
        return self.collaboration_title
    
class Member_Information(models.Model):
    collaboration = models.ForeignKey(Collab_Information, on_delete=models.CASCADE)
    post_member = models.ForeignKey(User, on_delete=models.CASCADE)
    isOwner = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('collaboration', 'post_member')

    def __str__(self):
        return f"{self.post_member.username} in {self.collaboration.collaboration_title}"
    
def generate_audio_name():
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))  # Generates 3 uppercase letters
    return f"Audio_{random_letters}"

class syncAudios(models.Model):
    collaboration = models.ForeignKey(Collab_Information, on_delete=models.CASCADE)
    syncId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    syncMedia = models.FileField(upload_to='media/syncAudios')
    timestamp = models.DateTimeField(auto_now_add=True)
    syncedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    audioName = models.CharField(max_length=50, default=generate_audio_name)
    
    def __str__(self):
        return f"{self.collaboration.collaboration_Id} in {self.syncId}"
