from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone




# Create your models here.
class profiledatadb(models.Model):
    username=models.CharField(primary_key=True,max_length=15,unique=True)
    password = models.CharField(max_length=15)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='Media/',default='default/user.png')
    user_bio=models.TextField()
    phone=models.IntegerField(null=True)
    timestamp=models.DateTimeField(auto_now_add=True,null=True)
    insta=models.URLField(max_length=200,blank=True,null=True)
    yout=models.URLField(max_length=200,blank=True,null=True)
    twit=models.URLField(max_length=200, blank=True,null=True)
    followers = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return str(self.username) 

class postdb(models.Model):
    pid=models.UUIDField(primary_key=True,max_length=10,default=uuid.uuid4)
    username=models.ForeignKey(to=profiledatadb,on_delete=models.CASCADE)
    media=models.FileField(upload_to='media/Posts')
    media_thumbnail=models.FileField(upload_to='media/Thumbnails',default=None,blank=True,null=True)
    caption=models.CharField(max_length=30)
    descr=models.TextField()
    langu=models.CharField(max_length=15)
    mediatype=models.CharField(max_length=15)
    location=models.CharField(max_length=15)
    likes=models.IntegerField(default=0)
    media_format=models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now=True  )
    # New fields for flagging system
    flagged = models.BooleanField(default=False)  # 0 = Not Flagged, 1 = Flagged
    flag_counter = models.IntegerField(default=0)  # Tracks offensive/explicit content reports
    reported_users = models.ManyToManyField(User, blank=True, related_name="reported_posts")
    #media visibility
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.pid)
    

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

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('collab', 'Collaboration Request'),
        ('flagged', 'Post Flagged'),
    )
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('postdb', on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')

    class Meta:
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.message}"       
    
      
        


