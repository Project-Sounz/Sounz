from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class profiledatadb(models.Model):
    username=models.CharField(primary_key=True,max_length=15,unique=True)
    password = models.CharField(max_length=15)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='Media/', blank=True, null=True, default='media/default_profile_picture.jpg')
    user_bio=models.TextField()
    phone=models.IntegerField(null=True)
    timestamp=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.username) 

   


class postdatabase(models.Model):
    username=models.ForeignKey(to=profiledatadb,on_delete=models.CASCADE,default=0)
    media_address = models.CharField(max_length=256)
    likes_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=32, null=True)
    media_type = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    descr = models.TextField()
    lang = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pid)     


class postdatadb(models.Model):
    username=models.ForeignKey(to=profiledatadb,on_delete=models.CASCADE,default=0)
    media_address = models.CharField(max_length=256)
    likes_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=32, null=True)
    media_type = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    descr = models.TextField()
    lang = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pid)      
    
      
        


